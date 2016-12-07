using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;

namespace MainPortal
{
    public partial class Index : System.Web.UI.Page
    {
        protected string recBooksHtml = "";
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Session["User"] == null)
            {
                Response.Redirect("Login.aspx");
            }
            else
            {
                User user = (User)Session["User"];
                HBaseHelper.Open();
                List<TRowResult> resRow = HBaseHelper.GetByRow("t_users", user.Id);
                if (resRow.Count == 1)
                {
                    foreach (var col in resRow[0].Columns)
                    {
                        if (Encoding.UTF8.GetString(col.Key) == "msg:recBooks")
                        {
                            string[] recStrBooks = Encoding.UTF8.GetString(col.Value.Value).Split(',');
                            Dictionary<Book, string> dicBookAndRate = new Dictionary<Book, string>();
                            foreach (var bookAndRate in recStrBooks)
                            {
                                string[] str = bookAndRate.Split(':');
                                string bookId = str[0];
                                string rate = str[1];
                                List<TRowResult> resBook = HBaseHelper.GetByRow("t_books", bookId);
                                Book book = new Book();
                                book.Id = bookId;
                                foreach (var bookCol in resBook[0].Columns)
                                {
                                    switch (Encoding.UTF8.GetString(bookCol.Key))
                                    {
                                        case "msg:name":
                                            book.Name = Encoding.UTF8.GetString(bookCol.Value.Value);
                                            break;
                                        case "msg:info":
                                            book.Info = Encoding.UTF8.GetString(bookCol.Value.Value);
                                            break;
                                        case "msg:price":
                                            book.Price = Encoding.UTF8.GetString(bookCol.Value.Value);
                                            break;
                                        case "msg:image":
                                            book.Image = Encoding.UTF8.GetString(bookCol.Value.Value);
                                            break;
                                        default:
                                            break;
                                    }
                                }
                                dicBookAndRate.Add(book, rate);
                            }
                            StringBuilder sb2 = new StringBuilder(2048);
                            foreach (var goodBook in dicBookAndRate)
                            {
                                sb2.AppendFormat("<div class='feat_prod_box'>");
                                sb2.AppendFormat("<div class='prod_img'>");
                                sb2.AppendFormat("<a href='BookDetail.aspx?id={0}'>", goodBook.Key.Id);
                                sb2.AppendFormat("<img src='{0}' alt='' title='' border='0' /></a></div>", goodBook.Key.Image);
                                sb2.AppendFormat("<div class='prod_det_box'>");
                                sb2.AppendFormat("<div class='box_top'></div>");
                                sb2.AppendFormat("<div class='box_center'><div class='prod_title'>{0}</div>", goodBook.Key.Name);
                                sb2.AppendFormat("<p class='details' style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{0}</p>", goodBook.Key.Info);
                                sb2.AppendFormat("<a href='BookDetail.aspx?id={0}' class='more'>- 预测喜欢度：{1} -</a>", goodBook.Key.Id, goodBook.Value);
                                sb2.AppendFormat("<div class='clear'></div></div>");
                                sb2.AppendFormat("<div class='box_bottom'></div></div>");
                                sb2.AppendFormat("<div class='clear'></div></div>");
                            }
                            recBooksHtml = sb2.ToString();
                            HBaseHelper.Close();
                            break;
                        }
                    }
                }
            }
        }
    }
}