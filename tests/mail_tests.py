__author__ = 'asdffdsa'
import unittest
from . import testhelpers
from . import testaccounts


class MailTestOffline(unittest.TestCase):

    def setUp(self):
        self.accounts = testhelpers.make_accountlist(testaccounts.accounts)
        self.mails = testhelpers.make_maillist_fictional(self.accounts)

    def test_equality(self):
        """  the same folders should be equal, different folders should not
        """
        for mail1 in self.mails:
            index1 = self.mails.index(mail1)
            for mail2 in self.mails:
                index2 = self.mails.index(mail2)
                if index1 == index2:
                    self.assertEqual(mail1, mail2)
                else:
                    self.assertNotEqual(mail1, mail2)