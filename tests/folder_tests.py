__author__ = 'asdffdsa'
import unittest
import random
from . import testaccounts
from . import testhelpers


class FolderTestOffline(unittest.TestCase):
    def setUp(self):
        self.accounts = testhelpers.make_accountlist(testaccounts.accounts)
        self.folders = testhelpers.make_folderlist_fictional(self.accounts)

    def test_addition(self):
        """ test wether the normal rules for addition (kommutativ, etc.) are active for accounts
        """
        for folder in self.folders:
            to_recombinate = random.choice(range(0, len(self.folders) - 1))
            to_recombinate_2 = random.choice(range(0, len(self.folders) - 1))
            self.assertEqual(folder + self.folders[to_recombinate], self.folders[to_recombinate] + folder)
            self.assertEqual((folder + self.folders[to_recombinate]) + self.folders[to_recombinate_2],
                             folder + (self.folders[to_recombinate] + self.folders[to_recombinate_2]))

    def test_equality(self):
        """  the same folders should be equal, different folders should not
        """
        for folder1 in self.folders:
            index1 = self.folders.index(folder1)
            for folder2 in self.folders:
                index2 = self.folders.index(folder2)
                if index1 == index2:
                    self.assertEqual(folder1, folder2)
                else:
                    self.assertNotEqual(folder1, folder2)