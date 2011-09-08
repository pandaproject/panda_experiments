#!/usr/bin/env python

class HStorageRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'hstorage':
            return 'hstorage'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'hstorage':
            return 'hstorage'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
        if db == 'hstorage':
            return (model._meta.app_label == 'hstorage')
        elif model._meta.app_label == 'hstorage':
            return False
        return None
