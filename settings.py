__author__ = 'asdffdsa'
from databases import base
import importlib
DATABASES_AVAILABLE = {}
for db in base.DATABASES:
    name = db.split(':')
    newImport = importlib.import_module('databases.' + name[0])
    newClass = getattr(newImport, name[1])
    DATABASES_AVAILABLE[name[0]] = newClass


database = base.DummyBase('DummyBase')

def set_database(databaseType, name, *args, **kwargs):
    global database
    database = DATABASES_AVAILABLE[databaseType](name, args, kwargs)