from rest_framework import serializers

from .models import InventoryItem, Warehouse, WarehouseStock


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ["id", "partner", "sku", "name", "description", "created_at"]


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "partner", "name", "location"]


class WarehouseStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseStock
        fields = ["id", "warehouse", "item", "quantity"]
