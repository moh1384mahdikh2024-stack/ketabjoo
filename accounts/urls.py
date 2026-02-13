from django.urls import path
from .views import LoginView, LogoutView, DashboardView, RegisterView, NewCategoryView, UpdateCategoryView, \
    NewAuthorView, UpdateAuthorView, NewBookView, UpdateBookView, CommentView,CartView,AddCartView,DeleteCartView,BoughtBookView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("category/", NewCategoryView.as_view(), name="category_admin"),
    path("category/<path:cat_slug>", UpdateCategoryView.as_view(), name="update_category_admin"),
    path("autor/", NewAuthorView.as_view(), name="author_admin"),
    path("author/<author_slug>", UpdateAuthorView.as_view(), name="update_author_admin"),
    path("book/", NewBookView.as_view(), name="book_admin"),
    path("book/<book_slug>", UpdateBookView.as_view(), name="update_book_admin"),
    path("review/new/", CommentView.as_view(), name="status_comment_admin"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<book_slug>", AddCartView.as_view(), name="add_cart"),
    path("cart/delete/<book_slug>", DeleteCartView.as_view(), name="delete_cart"),
    path("mybook/",BoughtBookView.as_view(), name="mybook"),
]
