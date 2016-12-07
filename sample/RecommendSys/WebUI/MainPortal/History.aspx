<%@ Page Title="" Language="C#" MasterPageFile="~/Page.Master" AutoEventWireup="true"
    CodeBehind="History.aspx.cs" Inherits="MainPortal.History" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="Menu" runat="server">
    <li><a href="Index.aspx">猜你喜欢</a></li>
    <li class="selected"><a href="History.aspx">最近浏览</a></li>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="Replace" runat="server">
    <%--<div class="title">
        <span class="title_icon">
            <img src="images/bullet1.gif" alt="" title="" /></span>最受欢迎</div>
    <%=discountBooksHtml%>--%>
    <!--最新上市开始-->
    <div class="title">
        <span class="title_icon">
            <img src="images/bullet2.gif" alt="" title="" /></span>最近的浏览记录
    </div>
    <div class="new_products">
        <!--6-->
        <%=historyHtml%>
        <!--6-->
    </div>
    <!--最新上市结束-->
</asp:Content>

