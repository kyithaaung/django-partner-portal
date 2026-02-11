from django.contrib import admin

from .models import (
    InternalUserProfile,
    InventoryItem,
    Partner,
    PartnerUserProfile,
    StockTransferOrder,
    Warehouse,
    WarehouseStock,
)

admin.site.register(Partner)
admin.site.register(InternalUserProfile)
admin.site.register(PartnerUserProfile)
admin.site.register(InventoryItem)
admin.site.register(Warehouse)
admin.site.register(WarehouseStock)
admin.site.register(StockTransferOrder)
