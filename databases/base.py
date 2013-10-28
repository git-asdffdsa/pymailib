__author__ = 'asdffdsa'
import errors


class DummyBase:
    def __init__(self, name):
        pass

    def copy(self):
        return self

    def setup(self):
        raise NotImplementedError

    def read_to_account(self, account, db_account):
        raise NotImplementedError

    def save_account(self, account):
        raise NotImplementedError

    def search_account_by_address(self, address):
        raise NotImplementedError

    def search_account_by_id(self, number):
        raise NotImplementedError

    def save_folder(self, folder):
        raise NotImplementedError

    def read_to_folder(self, folder, db_folder):
        raise NotImplementedError

    def search_folder_by_id(self, number):
        raise NotImplementedError

    def save_mail(self, mail):
        raise NotImplementedError

    def read_to_mail(self, mail, db_mail):
        raise NotImplementedError

    def search_mail_by_id(self, number):
        raise NotImplementedError


DATABASES = [
    'sqlite:SqliteBase'
]

DATABASE_STRUCTURE = {
    'accounts': [
        #no dicts, because we need ordering
        ['id', 'int', 'primary'],
        ['address', 'text'],
        ['short_name', 'text'],
        ['send_protocol', 'int'],
        ['send_authentication', 'int'],
        ['send_socket', 'int'],
        ['send_servername', 'text'],
        ['send_port', 'int'],
        ['send_username', 'text'],
        ['send_password', 'text'],
        ['get_protocol', 'int'],
        ['get_authentication', 'int'],
        ['get_socket', 'int'],
        ['get_servername', 'text'],
        ['get_port', 'int'],
        ['get_username', 'text'],
        ['get_password', 'text'],
    ],
    'folders': [
        ['id', 'int', 'primary'],
        ['number', 'int'],
        ['folderStructure', 'text']
    ],
    'mails': [
        ['id', 'int', 'primary'],
        ['server_id', 'int'],
        ['sender_account_id', 'int'],
        ['receiver_account_id', 'int'],
        ['receiver', 'text'],
        ['sender', 'text'],
        ['time_sent', 'int'],
        ['full_header', 'text'],
        ['flags_json', 'string'],
        ['folder', 'string'],
        ['seen', 'boolean'],
        ['subject', 'string'],
        ['answer_to', 'int'],
        ['cc_json', 'string'],
        ['bcc_json', 'string'],
        ['__content__', 'string'],
        ['__has_content__', 'boolean'],
        ['size', 'int']
    ]
}

#will be substituted by the above
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

MAIL_FIELDS = [
    'id,'
    'server_id',
    ''
]