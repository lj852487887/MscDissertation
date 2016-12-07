using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;

namespace MainPortal
{
    public partial class Login : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(Request.Form["action"]))
            {
                string uid = Request.Form["uid"] ?? "";
                string pwd = Request.Form["pwd"] ?? "";
				//使用过滤器查找该用户
                string strFilter = string.Format("SingleColumnValueFilter('msg','uid',=,'substring:{0}') AND SingleColumnValueFilter('msg','pwd',=,'substring:{1}')", uid, pwd);
                List<byte[]> cols = new List<byte[]>();
				//用到的列
                cols.Add(Encoding.UTF8.GetBytes("msg:uid"));
                cols.Add(Encoding.UTF8.GetBytes("msg:pwd"));
                cols.Add(Encoding.UTF8.GetBytes("msg:recBooks"));
                HBaseHelper.Open();
				//返回的数据个数自定义
                List<TRowResult> resRow = HBaseHelper.GetByFilter("t_users", strFilter, cols,1);
                HBaseHelper.Close();
                if (resRow.Count == 1)
                {
                    User user = new User();
                    user.Id = Encoding.UTF8.GetString(resRow[0].Row);
					//遍历每一列取出起其中的值
                    foreach (var col in resRow[0].Columns)
                    {
                        switch (Encoding.UTF8.GetString(col.Key))
                        {
                            case "msg:uid":
                                user.Uid = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            case "msg:pwd":
                                user.Pwd = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            case "msg:recBooks":
                                user.RecBooks = Encoding.UTF8.GetString(col.Value.Value);
                                break;
                            default:
                                break;
                        }
                    }
                    Session["User"] = user;
                    Response.Redirect("Index.aspx");
                }
                else
                {
                    Response.Write("error!");
                }
            }
        }
    }
}