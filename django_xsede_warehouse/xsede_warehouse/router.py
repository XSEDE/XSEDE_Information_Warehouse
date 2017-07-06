import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('db_name',)
#import pdb

class ModelDatabaseRouter(object):
    """Allows each model to set its own target schema"""
    def db_for_read(self, model, **hints):
        try:
            db_name = model._meta.db_name
        except:
            db_name = 'default'
#       print 'db_for_read(model=%s) = %s' % (model, db_name)
        return db_name

    def db_for_write(self, model, **hints):
        try:
            db_name = model._meta.db_name
        except:
            db_name = 'default'
#       print 'db_for_write(model=%s) = %s' % (model, db_name)
        return db_name

    def allow_relation(self, model1, model2, **hints):
        try:
            db_name1 = model1._meta.db_name
        except:
            db_name1 = 'default'
        try:
            db_name2 = model2._meta.db_name
        except:
            db_name2 = 'default'
        return db_name1 == db_name2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        try:
            db_name = hints['model']._meta.db_name
        except:
            return False
        if app_label == 'outages':
#           pdb.set_trace()
#           print 'allow_migrate db=%s, app_label=%s, db_name=%s, model_name=%s -> %s' % \
                (db, app_label, db_name, model_name, db == db_name)
        return db == db_name
