from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    PartnerLoginView,
    PortalHomeView,
    create_item,
    create_sto,
    create_warehouse,
    item_query,
)

urlpatterns = [
    path("", PortalHomeView.as_view(), name="portal-home"),
    path("login/", PartnerLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("items/create/", create_item, name="create-item"),
    path("warehouses/create/", create_warehouse, name="create-warehouse"),
    path("sto/create/", create_sto, name="create-sto"),
    path("items/<int:item_id>/query/", item_query, name="item-query"),
]
