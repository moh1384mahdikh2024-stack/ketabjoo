from django.urls import path
from .views import CommentsView, AcceptCommentsView, RejectCommentsView

urlpatterns = [
    path('create/review/<book_slug>/',CommentsView.as_view(),name='create-review'),
    path('review/accept/<int:review_id>/',AcceptCommentsView.as_view(),name='accept-review'),
    path('review/reject/<int:review_id>/',RejectCommentsView.as_view(),name='reject-review'),
]