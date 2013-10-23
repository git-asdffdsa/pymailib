__author__ = 'asdffdsa'
import unittest

from . import testaccounts
from . import testsettings
import accounts
import settings

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

    def test_integry(self):
        """ test wether writing to and reading accounts from a database leaves everything unaltered
        """
        oldAccount = None
        for account in self.accounts:
            account.save_to_db()
            newaccount = accounts.Account()
            newaccount.read_from_db(account.address)
            self.assertTrue(newaccount == account)
            if oldAccount is not None:
                self.assertFalse(newaccount == oldAccount)
            oldAccount = account
        #so now all accounts are in the database



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