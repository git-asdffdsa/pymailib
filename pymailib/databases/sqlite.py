from .. import errors
from . import base

__author__ = 'asdffdsa'
import sqlite3


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
        #one sqlite copy can not be shared over threads, so recreate it
        return SqliteBase(self.name, self.args, self.kwargs)

    def setup(self):
        """ creates all the tables necessary
        """
        #create all the tables
        for tablename, tablecontent in base.DATABASE_STRUCTURE.items():
            try:
                self.cursor.execute('select * from ?', tablename)
            except sqlite3.OperationalError:
                pass
            else:
                #if it already exists, go to the next
                continue
            execution_string = 'create table ' + tablename + '('
            for field in tablecontent:
                #sqlite does not have booleans
                if field[1] == 'boolean':
                    execution_string += field[0] + ' ' + 'int'
                else:
                    execution_string += field[0] + ' ' + field[1]
                if 'primary' in field:  # this is the primary key
                    execution_string += ' primary key'
                execution_string += ', '
            execution_string = execution_string[:-2] + ')'  # remove the last comma and space
            self.cursor.execute(execution_string)


    def read_to_account(self, account, db_account):
        """ takes a row object and fills an account with it
        """
        if db_account is None:
             raise errors.account_not_found
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
        folder.json = db_folder['folderStructure']

    def search_folder_by_id(self, number):
        self.cursor.execute('select * from folders where id=?', (number,))
        return self.cursor.fetchone()

    def save_folder(self, folder):
        self.cursor.execute("select * from folders where id=?", (str(folder.id),))
        if self.cursor.fetchone() is None:
            self.cursor.execute('insert into folders values (?,?,?)', (str(folder.id), str(folder.number), folder.json))
        else:
            self.cursor.execute('update folders set id=?, number=?, folderStructure=? where id=?',
                                (str(folder.id), str(folder.number), folder.json, str(folder.id)))

    def save_mail(self, mail):
        fields = []
        set_field_string_1 = ''
        set_field_string_2 = '('
        for field in base.DATABASE_STRUCTURE['mails']:
            fields.append(str(getattr(mail, field[0])))
            set_field_string_1 += field[0] + '=?, '
            set_field_string_2 += '?, '
        # delete last comma and space
        set_field_string_1 = set_field_string_1[:-2]
        set_field_string_2 = set_field_string_2[:-2] + ')'
        self.cursor.execute("select * from mails where id=?", (str(mail.id),))
        if self.cursor.fetchone() is None:
            #element does not exist yet
            self.cursor.execute('insert into mails values ' + set_field_string_2, fields)
        else:
            fields.append(mail.id)
            self.cursor.execute('update mails set ' + set_field_string_1 + ' where id=?', fields)

        self.cursor.execute("select * from mails where id=?", (str(mail.id),))

    def search_mail_by_id(self, number):
        self.cursor.execute('select * from mails where id=?', (number,))
        return self.cursor.fetchone()

    def read_to_mail(self, mail, db_mail):
        for field in base.DATABASE_STRUCTURE['mails']:
            if field[1] == 'boolean':
                setattr(mail, field[0], (db_mail[field[0]] == 1))
            else:
                setattr(mail, field[0], db_mail[field[0]])
