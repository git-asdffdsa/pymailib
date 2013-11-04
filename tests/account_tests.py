from pymailib import accounts

__author__ = 'asdffdsa'
from . import testaccounts
from . import testsettings
from . import testhelpers
import string
import random
import unittest

class MailAccountTest(unittest.TestCase):
    """test the class MailAccount"""
    def setUp(self):
        self.accounts = testhelpers.make_accountlist(testaccounts.accounts)

    def test_mailwizard(self):
        """test the mail wizard to get settings automatically"""
        for account in self.accounts:
            if account.address in testaccounts.accounts_no_wizard:
                continue
            testaccount = accounts.Account()
            testaccount.auto_fill(account.address, account.get_password)  # lets hope they are the same
            self.assertEqual(testaccount, account)

    def testpasswordverifytrue(self):
        """test wether the password verifier returns true for the right password"""
        for account in self.accounts:
            if account.address in testaccounts.accounts_no_pwcheck:
                continue
            self.assertTrue(account.passwords_verify())

    def testpasswordverifyfalse_random(self):
        """test wether the password verifier returns false for the wrong (random) password"""
        for account in self.accounts:
            testaccount = account
            for counter in range(0, testsettings.random_password_times):
                password_length = random.choice(range(testsettings.random_password_lengths[0],
                                                      testsettings.random_password_lengths[1]))
                password = ''
                for number in range(0, password_length):
                    password = password + random.choice(string.printable)
                if password == account.get_password:
                    continue
                testaccount.get_password = password
                testaccount.send_password = password
                self.assertFalse(testaccount.test_password_get())
                self.assertFalse(account.test_password_send())

    def testpasswordverifyfalse_list(self):
        """test wether the password verifier returns false for the wrong password (out of a list)"""
        for account in self.accounts:
            testaccount = account
            for password in testsettings.false_passwords:
                if password == account.get_password:
                    continue
                testaccount.get_password = password
                testaccount.send_password = password
                self.assertFalse(testaccount.test_password_get())
                self.assertFalse(account.test_password_send())

