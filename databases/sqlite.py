__author__ = 'asdffdsa'
import sqlite3
from . import base


class SqliteBase(base.DummyBase):
    def __init__(self, name=':memory:', *args, **kwargs):
        self.connection = sqlite3.connect(name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.name = name
        self.args = args
        self.kwargs = kwargs
        base.DummyBase.__init__(self, name)

    def copy(self):
        return SqliteBase(self.name, self.args, self.kwargs)

    def setup(self):
        """ creates all the tables necessary
        """
        try:
            self.cursor.execute('select * from accounts')
        except sqlite3.OperationalError:
            self.cursor.execute('''create table accounts
              (id integer primary key, address text, short_name text, send_protocol integer,
              send_authentication integer, send_socket integer, send_servername text, send_port integer, send_username text,
              send_password text, get_protocol integer, get_authentication integer, get_socket integer, get_servername text,
              get_port integer, get_username text, get_password text)''')
        try:
            self.cursor.execute('select * from folders')
        except sqlite3.OperationalError:
            self.cursor.execute('''create table folders
              (id integer primary key, number integer, folderStructure json)''')

    def read_to_account(self, account, db_account):
        """ takes a row object and fills an account with it
        """
        for element in base.ACCOUNT_FIELDS:
            setattr(account, element, db_account[element])
        pass

    def search_account_by_address(self, address):
        """ finds an account with the given address and returns a row object
        """
        self.cursor.execute('select * from accounts where address=?', (address,))
        finding = self.cursor.fetchone()
        return finding

    def search_account_by_id(self, number):
        """ finds an account with the given id
        """
        self.cursor.execute('select * from accounts where id=?', (number,))
        finding = self.cursor.fetchone()
        return finding

    def save_account(self, account):
        self.cursor.execute("select * from accounts where id=?", (str(account.id),))
        fields = []
        fieldstring1 = ''
        fieldstring2 = '('
        for field in base.ACCOUNT_FIELDS:
            fields.append(str(getattr(account, field)))
            fieldstring1 += field + '=?,'
            fieldstring2 += '?,'
        fieldstring1 = fieldstring1[:-1]
        fieldstring2 = fieldstring2[:-1] + ')'
        if self.cursor.fetchone() is None:
            self.cursor.execute('insert into accounts values ' + fieldstring2, fields)
        else:
            fields.append(account.id)
            self.cursor.execute('update accounts set ' + fieldstring1 + ' where id=?', fields)

    def read_to_folder(self, folder, db_folder):
        folder.id = db_folder['id']
        folder.number = db_folder['number']
        folder.json = db_folder['json']

    def search_folder_by_id(self, number):
        self.cursor.execute('select * from folders where id=?', (number,))
        finding = self.cursor.fetchone()
        return finding

    def save_folder(self, folder):
        self.cursor.execute("select * from folders where id=?", (str(folder.id),))
        if self.cursor.fetchone() is None:
            self.cursor.execute('insert into folders values (?,?,?)', (str(folder.id), str(folder.number), folder.json))
        else:
            self.cursor.execute('update accounts set id=?, number=?, json=? where id=?',
                                (str(folder.id), str(folder.number), folder.json, str(folder.id)))