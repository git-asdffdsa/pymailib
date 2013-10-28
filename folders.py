__author__ = 'asdffdsa'

import errors
import json
import accounts
import settings


class Folder:
    """ holds a virtual folder
    self.folders --[id1]--|--account1
                    |     |
                    |     |--|-foldername1
                    |        |-foldername2
                    |        |-foldername3
                    |
                   [id2]--|--account2
                          |
                          |--|-foldername1
                             |-foldername2
                             |-foldername3
    """
    def __init__(self, account=None, foldername=None, number=0, id=0):
        #an integer, frontends can use them for their own purpose
        self.number = number
        self.id = id
        self.folders = {}
        if account is not None and foldername is not None:
            self.enrich(account, foldername)

    def enrich(self, account, foldername, overwrite=True):
        if account.id not in self.folders:
            self.folders[account.id] = [account, []]
        elif overwrite:
            self.folders[account.id][0] = account
        if foldername not in self.folders[account.id][1]:
            self.folders[account.id][1].append(foldername)

    def __eq__(self, other):
        #simply comparing __dict__ does not work, because the foldernames could have a different order
        #thats why we order them first
        if isinstance(other, self.__class__):
            for account_id, folderlist in self.folders.items():
                folderlist[1].sort()
            for account_id, folderlist in other.folders.items():
                folderlist[1].sort()
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        new_folder = Folder()
        for account_id, folderlist in self.folders.items():
            for foldername in folderlist[1]:
                new_folder.enrich(folderlist[0], foldername)
        for account_id, folderlist in other.folders.items():
            for foldername in folderlist[1]:
                new_folder.enrich(folderlist[0], foldername)
        new_folder.id = max(self.id, other.id)
        new_folder.number = max(self.number, other.number)
        return new_folder

    def reload_accounts_db_all(self):
        for account_id, folderlist in self.folders.items():
            folderlist[0].read_from_db(account_id)

    def reload_accounts_db_by_id(self, number):
        self.folders[number][0].read_from_db(number)

    def substitute_by_account(self, account):
        found_id = None
        if account.id in self.folders:
            found_id = account.id
        if found_id is None:
            for account_id, folderlist in self.folders:
                if folderlist[0].address == account.address:
                    found_id = account_id
        if found_id is None:
            raise errors.account_not_found
        self.folders[found_id][0] = account

    def read_from_db(self, folder):
        if type(folder) is int:
            settings.database.read_to_folder(self, settings.database.search_folder_by_id(folder))
        else:
            settings.database.read_to_folder(self, folder)

    def save_to_db(self):
        settings.database.save_folder(self)

    def __load_from_json__(self, string):
        structure_from_json = json.loads(string)
        for account_id_string, folderlist in structure_from_json.items():
            #json decodes dictionary keys to string type; see
            #http://stackoverflow.com/questions/1450957/pythons-json-module-converts-int-dictionary-keys-to-strings
            account_id = int(account_id_string)
            newaccount = accounts.Account()
            newaccount.id = account_id
            self.folders[account_id] = [newaccount, folderlist]
        self.reload_accounts_db_all()

    def __generate_json__(self):
        #will be exactly the same as self.folders, but without the actual accounts
        structure_to_write = {}
        for account_id, folderlist in self.folders.items():
            structure_to_write[account_id] = folderlist[1]
        return json.dumps(structure_to_write)

    json = property(__generate_json__, __load_from_json__)