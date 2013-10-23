__author__ = 'asdffdsa'
import errors


class DummyBase:
    def __init__(self, name):
        pass

    def copy(self):
        return self

    def setup(self):
        raise errors.database_doesnt_support

    def read_to_account(self, account, db_account):
        raise errors.database_doesnt_support

    def save_account(self, account):
        raise errors.database_doesnt_support

    def search_account_by_address(self, address):
        raise errors.database_doesnt_support

    def search_account_by_id(self, number):
        raise errors.database_doesnt_support

    def save_folder(self, folder):
        raise errors.database_doesnt_support

    def read_to_folder(self, folder, db_folder):
        raise errors.database_doesnt_support

    def search_folder_by_id(self, number):
        raise errors.database_doesnt_support

DATABASES = [
    'sqlite:SqliteBase'
]


ACCOUNT_FIELDS = [
    'id',
    'address',
    'short_name',
    'send_protocol',
    'send_authentication',
    'send_socket',
    'send_servername',
    'send_port',
    'send_username',
    'send_password',
    'get_protocol',
    'get_authentication',
    'get_socket',
    'get_servername',
    'get_port',
    'get_username',
    'get_password'
]