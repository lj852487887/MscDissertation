using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;
using Thrift.Protocol;
using Thrift.Transport;

namespace MainPortal
{
    public partial class History : System.Web.UI.Page
    {
        protected string historyHtml = "";
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Session["User"] == null)
            {
                Response.Redirect("Login.aspx");
            }
            else
            {
                User user = (User)Session["User"];
                string strFilter = string.Format("SingleColumnValueFilter('msg','userId',=,'substring:{0}')", user.Id);
                List<byte[]> cols = new List<byte[]>();
                cols.Add(Encoding.UTF8.GetBytes("msg:userId"));
                cols.Add(Encoding.UTF8.GetBytes("msg:bookId"));
                cols.Add(Encoding.UTF8.GetBytes("msg:rating"));
                HBaseHelper.Open();
                List<TRowResult> resRow = HBaseHelper.GetByFilter("t_ratings", strFilter, cols, 30);
                Dictionary<string, string> booksAndRatings = new Dictionary<string, string>();
                foreach (var row in resRow)
                {
                    string bookId = "";
                    string rating = "";
                    foreach (var col in row.Columns)
                    {
                        switch (Encoding.UTF8.GetString(col.Key))
                        {
                            case "msg:bookId":
                                bookId = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            case "msg:rating":
                                rating = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            default:
                                break;
                        }
                    }
                    booksAndRatings.Add(bookId, rating);
                }

                Dictionary<Book, string> recBooks = new Dictionary<Book, string>();
                foreach (var bookAndRating in booksAndRatings)
                {
                    List<TRowResult> resBook = HBaseHelper.GetByRow("t_books", bookAndRating.Key);
                    Book book = new Book();
                    book.Id = bookAndRating.Key;
                    foreach (var col in resBook[0].Columns)
                    {
                        switch (Encoding.UTF8.GetString(col.Key))
                        {
                            case "msg:name":
                                book.Name = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            case "msg:info":
                                book.Info = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            case "msg:price":
                                book.Price = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            case "msg:image":
                                book.Image = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            default:
                                break;
                        }
                    }
                    recBooks.Add(book, bookAndRating.Value);
                }
                HBaseHelper.Close();
                StringBuilder sb1 = new StringBuilder();
                foreach (var history in recBooks)
                {
                    sb1.AppendFormat("<div class='new_prod_box'><span>评分：{0}</span>", history.Value);
                    sb1.AppendFormat("<a href='Vip_BookDetail.aspx?id={0}'>{1}</a>", history.Key.Id, history.Key.Name);
                    sb1.AppendFormat("<div class='new_prod_bg'>");
                    sb1.AppendFormat("<a href='Vip_BookDetail.aspx?id={0}'><img src='{1}' width='90px' height='110px' class='thumb' border='0' /></a>", history.Key.Id, history.Key.Image);
                    sb1.AppendFormat("</div>");
                    sb1.AppendFormat("</div>");
                }
                historyHtml = sb1.ToString();
            }
        }
    }
}