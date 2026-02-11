from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from .forms import InventoryItemForm, StockTransferOrderForm, WarehouseForm
from .models import (
    InventoryItem,
    Partner,
    StockTransferOrder,
    Warehouse,
    WarehouseStock,
    item_stock_summary,
)


class PartnerLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True


def _is_internal(user):
    return hasattr(user, "internaluserprofile")


def _partner_for_user(user):
    if _is_internal(user):
        return None
    if hasattr(user, "partneruserprofile"):
        return user.partneruserprofile.partner
    raise Http404("No partner mapping found for user")


def _scoped_items(request_user):
    if _is_internal(request_user):
        return InventoryItem.objects.select_related("partner").all()
    return InventoryItem.objects.filter(partner=_partner_for_user(request_user)).select_related(
        "partner"
    )


def _scoped_warehouses(request_user):
    if _is_internal(request_user):
        return Warehouse.objects.select_related("partner").all()
    return Warehouse.objects.filter(partner=_partner_for_user(request_user)).select_related(
        "partner"
    )


class PortalHomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/portal_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "items": _scoped_items(self.request.user),
                "warehouses": _scoped_warehouses(self.request.user),
                "item_form": InventoryItemForm(),
                "warehouse_form": WarehouseForm(),
                "sto_form": StockTransferOrderForm(),
                "is_internal": _is_internal(self.request.user),
            }
        )
        return context


@login_required
@require_http_methods(["POST"])
def create_item(request):
    form = InventoryItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        if _is_internal(request.user):
            partner = get_object_or_404(Partner, id=request.POST.get("partner_id"))
        else:
            partner = _partner_for_user(request.user)
        item.partner = partner
        item.save()
    return redirect("portal-home")


@login_required
@require_http_methods(["POST"])
def create_warehouse(request):
    form = WarehouseForm(request.POST)
    if form.is_valid():
        warehouse = form.save(commit=False)
        if _is_internal(request.user):
            partner = get_object_or_404(Partner, id=request.POST.get("partner_id"))
        else:
            partner = _partner_for_user(request.user)
        warehouse.partner = partner
        warehouse.save()
    return redirect("portal-home")


@login_required
@require_http_methods(["POST"])
def create_sto(request):
    form = StockTransferOrderForm(request.POST)
    if form.is_valid():
        sto = form.save(commit=False)
        if _is_internal(request.user):
            partner = sto.item.partner
        else:
            partner = _partner_for_user(request.user)
            if sto.item.partner_id != partner.id:
                raise Http404("Cross-partner operation is forbidden")

        sto.partner = partner
        sto.created_by = request.user
        if sto.from_warehouse.partner_id != partner.id or sto.to_warehouse.partner_id != partner.id:
            raise Http404("Cross-partner warehouse operation is forbidden")

        with transaction.atomic():
            source = WarehouseStock.objects.select_for_update().get(
                warehouse=sto.from_warehouse,
                item=sto.item,
            )
            destination, _ = WarehouseStock.objects.select_for_update().get_or_create(
                warehouse=sto.to_warehouse,
                item=sto.item,
                defaults={"quantity": 0},
            )
            if source.quantity < sto.quantity:
                raise Http404("Insufficient stock")

            source.quantity -= sto.quantity
            destination.quantity += sto.quantity
            source.save(update_fields=["quantity"])
            destination.save(update_fields=["quantity"])
            sto.status = StockTransferOrder.STATUS_DONE
            sto.save()

    return redirect("portal-home")


@login_required
def item_query(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    if not _is_internal(request.user) and item.partner_id != _partner_for_user(request.user).id:
        raise Http404("Forbidden")

    return render(
        request,
        "core/item_query.html",
        {
            "item": item,
            "summary": item_stock_summary(item),
        },
    )
