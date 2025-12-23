from django.urls import path

from .views import AddFavorite,RemoveFavorite

urlpatterns = [
    path("add/<book_slug>/", AddFavorite.as_view(), name="add_favorite"),
    path("delete/<book_slug>/",RemoveFavorite.as_view(), name="remove_favorite"),
]