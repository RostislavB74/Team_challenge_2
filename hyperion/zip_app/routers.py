class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "zip_app":
            return "zip_db"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "zip_app":
            return "zip_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == obj2._state.db:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "zip_app":
            return db == "zip_db"
        return db == "default"
