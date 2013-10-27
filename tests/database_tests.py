__author__ = 'asdffdsa'
import unittest

from . import testaccounts
from . import testsettings
import accounts
import settings
import folders

import random
import string

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        settings.set_database('sqlite', ':memory:')
        settings.database.setup()
        self.accounts = []
        for account in testaccounts.accounts:
            newaccount = accounts.Account()
            for argument, value in account.items():
                if argument in testsettings.accounts_not_needed:
                    continue
                setattr(newaccount, argument, value)
            self.accounts.append(newaccount)
        self.folders = []
        for account in self.accounts:
            foldername_length = random.choice(range(testsettings.random_foldername_lengths[0],
                                                    testsettings.random_foldername_lengths[1]))
            foldername = ''
            for i in range(foldername_length):
                foldername += random.choice(string.printable)
            newfolder = folders.Folder(account, foldername)
            self.folders.append(newfolder)
        if len(self.folders) > 1:
            self.folders.append(self.folders[0] + self.folders[1])

    def test_integry(self):
        """ test wether writing to and reading accounts from a database leaves everything unaltered
        """
        old_account = None
        for account in self.accounts:
            account.save_to_db()
            new_account = accounts.Account()
            new_account.read_from_db(account.address)
            self.assertTrue(new_account == account)
            if old_account is not None:
                self.assertFalse(new_account == old_account)
            old_account = account
        #so now all accounts are in the database
        #now test for the folders
        old_folder = None
        for folder in self.folders:
            folder.save_to_db()
            new_folder = folders.Folder()
            new_folder.read_from_db(folder.id)
            self.assertTrue(new_folder == folder)
            if old_folder is not None:
                self.assertFalse(new_folder == old_folder)
            old_folder = folder

    def test_overwriting(self):
        """ test wether overwriting an account (by using the same id) really alters the account
        """
        for account in self.accounts:
            account.save_to_db()
            account.get_servername = 'asdf'
            account.save_to_db()
            newaccount = accounts.Account()
            newaccount.read_from_db(account.address)
            self.assertEqual(account, newaccount)

suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTest)
unittest.TextTestRunner(verbosity=2).run(suite)