__author__ = 'asdffdsa'

import errors
import json
import accounts
import settings

class Folder:
    """ holds a virtual folder
    self.accounts: |account1 :|--folder1
                   |          |--folder2
                   |          |--folder3
                   |
                   |account2 :|--folder1
                   |          |--folder2
                   etc        |--etc
    """
    def __init__(self, account=None, foldername=None, number=0, id=0):
        self.accounts = {}
        #an integer, frontends can use them for their own purpose
        self.number = number
        self.id = id
        if account is not None and foldername is not None:
            self.enrich(account, foldername)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def enrich(self, account, foldername):
        if hasattr(foldername, '__iter__'):
            #it is iterable
            for folder in foldername:
                self.enrich(account, foldername)
        #a string it is
        if not account in self.accounts:
            self.accounts[account] = []
        self.accounts[account].append(foldername)

    def __add__(self, other):
        new_folder = Folder()
        for account, folders in self.accounts.items():
            new_folder.enrich(account, folders)
        for account, folders in other.accounts.items():
            new_folder.enrich(account, folders)
        new_folder.id = max(self.id, other.id)
        new_folder.number = max(self.number, other.number)
        return new_folder

    def reload_accounts_db_all(self):
        for account in self.accounts:
            account.read_from_db(account.id)

    def reload_accounts_db_by_id(self, number):
        for account in self.accounts:
            if account.id == number:
                account.read_from_db(account.id)

    def substitute_by_account(self, account):
        found = None
        for local_account in self.accounts:
            if local_account.id == account.id:
                found = local_account
        if found is None:
            for local_account in self.accounts:
                if local_account.address == account.address:
                    found = local_account
        if found is None:
            raise errors.account_not_found
        found.__dict__ = account.__dict__

    def read_from_db(self, folder):
        if type(folder) is int:
            settings.database.read_to_folder(self, settings.database.search_folder_by_id(folder))
        else:
            settings.database.read_to_folder(self, folder)

    def __load_from_json__(self, string):
        structure_from_json = json.loads(string)
        for accountid, folderlist in structure_from_json:
            newaccount = accounts.Account()
            newaccount.id = accountid
            self.accounts[newaccount] = folderlist
        self.reload_accounts_db_all()

    def __generate_json__(self):
        #will be exactly the same as self.accounts, only that it holds only an id instead of a whole account
        structure_to_write = {}
        for account, folderlist in self.accounts:
            structure_to_write[account.id] = folderlist
        return json.dumps(structure_to_write)

    json = property(__generate_json__, __load_from_json__)
