from django import forms
from .models import InventoryItem, Warehouse, StockTransferOrder


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["sku", "name", "description"]


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "location"]


class StockTransferOrderForm(forms.ModelForm):
    class Meta:
        model = StockTransferOrder
        fields = ["item", "from_warehouse", "to_warehouse", "quantity"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("from_warehouse") == cleaned.get("to_warehouse"):
            self.add_error("to_warehouse", "Destination warehouse must be different.")
        return cleaned
