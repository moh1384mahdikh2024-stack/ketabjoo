from django.urls import path
from .views import home, CreateCategory, UpdateCategory, CreateAuthor, UpdateAuthor, CreateBook, UpdateBook,BookDetailView, DeleteBook,ShopView

urlpatterns = [
    path("", home, name="home"),
    path("create/category/", CreateCategory.as_view(), name="create_category"),
    path("update/category/<path:cat_slug>/", UpdateCategory.as_view(), name="update_category"),
    path("create/author/", CreateAuthor.as_view(), name="create_author"),
    path("update/author/<author_slug>/", UpdateAuthor.as_view(), name="update_author"),
    path("create/book/", CreateBook.as_view(), name="create_book"),
    path("update/book/<book_slug>/", UpdateBook.as_view(), name="update_book"),
    path("delete/book/<book_slug>/", DeleteBook.as_view(), name="delete_book"),
    path("book/<book_slug>/",BookDetailView.as_view(), name="book_detail"),
    path("shop/",ShopView.as_view(), name="shop"),
]
