<%@ Page Title="" Language="C#" MasterPageFile="~/Page.Master" AutoEventWireup="true"
    CodeBehind="Index.aspx.cs" Inherits="MainPortal.Index" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="Menu" runat="server">
    <li class="selected"><a href="Index.aspx">猜你喜欢</a></li>
    <li><a href="History.aspx">最近浏览</a></li>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="Replace" runat="server">
    <div class="title">
        <span class="title_icon">
            <img src="images/bullet1.gif" alt="" title="" /></span>根据你的评分记录猜你喜欢这些图书：</div>
    <%=recBooksHtml %>
</asp:Content>

