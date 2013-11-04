__author__ = 'asdffdsa'
import importlib

from .databases import base

__DATABASES_AVAILABLE__ = {}
#the database to use
database = base.DummyBase('DummyBase')
#from which path to load the account autoconfig xml files
LOCAL_AUTOCONFIG_PATH = ''


def __load_databases__():
    global __DATABASES_AVAILABLE__
    for db in base.DATABASES:
        name = db.split(':')
        __DATABASES_AVAILABLE__[name[0]] = name[1]


def set_database(database_type, name, *args, **kwargs):
    global database
    global __DATABASES_AVAILABLE__
    #check whether it is a available database
    if not database_type in __DATABASES_AVAILABLE__:
        raise ValueError
    new_import = importlib.import_module('.databases.' + database_type, 'pymailib')
    new_class = getattr(new_import, __DATABASES_AVAILABLE__[database_type])
    database = new_class(name, *args, **kwargs)


__load_databases__()