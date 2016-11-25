# class AuthRouter(object):
#     """
#     A router to control all database operations on models in the
#     auth application.
#     """
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read auth models go to auth_db.
#         """
#         if model._meta.app_label == 'auth':
#             return 'common'
#         return None
#
#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write auth models go to auth_db.
#         """
#         if model._meta.app_label == 'auth':
#             return 'common'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the auth app is involved.
#         """
#         if obj1._meta.app_label == 'auth' or \
#            obj2._meta.app_label == 'auth':
#            return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the auth app only appears in the 'auth_db'
#         database.
#         """
#         if app_label == 'auth':
#             return db == 'common'
#         return None
#
# class ClientDbRouter(object):
#     """
#     A router to control all database operations on models in the
#     auth application.
#     """
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read auth models go to auth_db.
#         """
#         if model._meta.app_label == 'connect_client_db':
#             return 'common'
#         return None
#
#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write auth models go to auth_db.
#         """
#         if model._meta.app_label == 'connect_client_db':
#             return 'common'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the auth app is involved.
#         """
#         if obj1._meta.app_label == 'connect_client_db' or \
#            obj2._meta.app_label == 'connect_client_db':
#            return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the auth app only appears in the 'auth_db'
#         database.
#         """
#         if app_label == 'connect_client_db':
#             return db == 'common'
#         return None


class OtherRouter(object):
    default_db_apps = [
        'auth',
        'admin',
        'contenttypes',
        'sessions',
    ]
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in self.default_db_apps:
            return 'common'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in self.default_db_apps:
            return 'common'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in self.default_db_apps or \
           obj2._meta.app_label in self.default_db_apps:
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in self.default_db_apps:
            return db == 'common'
        return None


class DefaultRouter(object):
    default_db_apps = [
        'mapper',
        'connect_client_db',
    ]
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in self.default_db_apps:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in self.default_db_apps:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in self.default_db_apps or \
           obj2._meta.app_label in self.default_db_apps:
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in self.default_db_apps:
            return db == 'default'
        return None
