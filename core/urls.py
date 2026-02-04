# core/urls.py
from django.urls import path
from .views import product_ui, PartnerLoginView

urlpatterns = [
    path('product/', product_ui),
    path('login/', PartnerLoginView.as_view()),
]