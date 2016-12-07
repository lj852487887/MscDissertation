<%@ Page Title="" Language="C#" MasterPageFile="~/Page.Master" AutoEventWireup="true"
    CodeBehind="Login.aspx.cs" Inherits="MainPortal.Login" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
    <script type="text/javascript">
        jQuery(function () {
            jQuery("#btnLogin").click(function () {
                if (jQuery("#uid").val() == "" || jQuery("#pwd").val() == "") {
                    alert("用户名或密码不能为空！");
                } else {
                    jQuery("#fmLogin").submit();
                }
            });
        });
    </script>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="Menu" runat="server">
    <li><a href="Index.aspx">猜你喜欢</a></li>
    <li><a href="History.aspx">最近浏览</a></li>
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="Replace" runat="server">
    <div class="title">
        <span class="title_icon">
            <img src="images/bullet1.gif" alt="" title="" /></span>我的账户</div>
    <div class="feat_prod_box_details">
        <div class="contact_form">
            <div class="form_subtitle">
                输入您的用户名和密码</div>
            <form name="login" id="fmLogin" action="Login.aspx" method="POST">
            <input type="hidden" name="action" value="1" />
            <div class="form_row">
                <label class="contact">
                    <strong>用户名:</strong></label>
                <input type="text" name="uid" id="uid" class="contact_input" />
            </div>
            <div class="form_row">
                <label class="contact">
                    <strong>密码:</strong></label>
                <input type="password" name="pwd" id="pwd" class="contact_input" />
            </div>
            <div class="form_row">
                <input type="button" id="btnLogin" class="register" value="登陆" />
            </div>
            </form>
        </div>
    </div>
</asp:Content>
