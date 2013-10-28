__author__ = 'asdffdsa'
import unittest

from . import testaccounts
from . import testhelpers
from . import testsettings
import accounts
import settings
import folders
import mails
import random
import string

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        settings.set_database('sqlite', ':memory:')
        settings.database.setup()
        self.accounts = testhelpers.make_accountlist(testaccounts.accounts)
        self.folders = testhelpers.make_folderlist_fictional(self.accounts)
        self.mails = testhelpers.make_maillist_fictional(self.accounts)

    def test_integry(self):
        """ test wether writing to and reading accounts and/or folders from a database leaves everything unaltered
        """
        old_account = None
        for account in self.accounts:
            account.save_to_db()
            new_account = accounts.Account()
            new_account.read_from_db(account.address)
            self.assertEqual(new_account, account)
            if old_account is not None:
                self.assertNotEqual(new_account, old_account)
            old_account = account
        #so now all accounts are in the database
        #now test for the folders
        old_folder = None
        for folder in self.folders:
            folder.save_to_db()
            new_folder = folders.Folder()
            new_folder.read_from_db(folder.id)
            self.assertEqual(new_folder, folder)
            if old_folder is not None:
                self.assertNotEqual(new_folder, old_folder)
            old_folder = folder
        old_mail = None
        for mail in self.mails:
            mail.save_to_db()
            new_mail = mails.Mail()
            new_mail.read_from_db(mail.id)
            self.assertEqual(new_mail, mail)
            if old_mail is not None:
                self.assertNotEqual(new_mail, old_mail)
            old_mail = mail

    def test_overwriting(self):
        """ test wether overwriting an account or folder (by using the same id) really alters the account
        """
        #accounts
        for account in self.accounts:
            account.save_to_db()
            account.get_servername = 'asdf'
            account.save_to_db()
            newaccount = accounts.Account()
            newaccount.read_from_db(account.address)
            self.assertEqual(account, newaccount)
        #folders
        for folder in self.folders:
            folder.save_to_db()
            for account_id, folderlist in folder.folders.items():
                i = 0
                for foldername in folderlist[1]:
                    folderlist[1][i] = foldername + '_test'
                    i += 1
            folder.save_to_db()
            newfolder = folders.Folder()
            newfolder.read_from_db(folder.id)
            self.assertEqual(folder, newfolder)
        #mails
        for mail in self.mails:
            mail.save_to_db()
            mail.receiver = 'THE_CHOSEN_ONE'
            mail.save_to_db()
            newmail = mails.Mail()
            newmail.read_from_db(mail.id)
            self.assertEqual(mail, newmail)

