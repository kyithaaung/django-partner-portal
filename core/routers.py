PARTNER_MODELS = {
    "partner",
    "partneruserprofile",
    "inventoryitem",
    "warehouse",
    "warehousestock",
    "stocktransferorder",
}


class PartnerDataRouter:
    """Routes partner-tenant data to partner MySQL instance."""

    def db_for_read(self, model, **hints):
        if model._meta.model_name in PARTNER_MODELS:
            return "partner"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.model_name in PARTNER_MODELS:
            return "partner"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label != "core":
            return db == "default"
        if model_name in PARTNER_MODELS:
            return db == "partner"
        return db == "default"
