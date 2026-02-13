from django.urls import path

from .views import AddInvoiceView

urlpatterns = [
    path("add/", AddInvoiceView.as_view(), name="add_invoice"),
]