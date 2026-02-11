from django.conf import settings
from django.db import models
from django.db.models import Sum


class Partner(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.SlugField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class InternalUserProfile(models.Model):
    ROLE_MS = "ms"
    ROLE_DEV = "dev"
    ROLE_CHOICES = [
        (ROLE_MS, "MS User"),
        (ROLE_DEV, "Developer"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class PartnerUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.partner.code}"


class InventoryItem(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="items")
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("partner", "sku")
        ordering = ["sku"]

    def __str__(self):
        return f"{self.partner.code}:{self.sku}"


class Warehouse(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="warehouses")
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=200)

    class Meta:
        unique_together = ("partner", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.partner.code}:{self.name}"


class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stocks")
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("warehouse", "item")

    def __str__(self):
        return f"{self.warehouse} {self.item.sku}={self.quantity}"


class StockTransferOrder(models.Model):
    STATUS_PENDING = "pending"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_DONE, "Done"),
    ]

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="stos")
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="outgoing_stos")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="incoming_stos")
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"STO#{self.id} {self.item.sku} {self.from_warehouse}->{self.to_warehouse}"


def item_stock_summary(item: InventoryItem):
    per_warehouse = WarehouseStock.objects.filter(item=item).values(
        "warehouse__name", "warehouse__location", "quantity"
    )
    total = WarehouseStock.objects.filter(item=item).aggregate(total=Sum("quantity"))["total"] or 0
    return {
        "total": total,
        "warehouses": list(per_warehouse),
    }
