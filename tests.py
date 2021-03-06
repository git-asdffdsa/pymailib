__author__ = 'asdffdsa'
from tests import database_tests
from tests import folder_tests
from tests import mail_tests
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(database_tests.DatabaseTest)
unittest.TextTestRunner(verbosity=2).run(suite)

suite2 = unittest.TestLoader().loadTestsFromTestCase(folder_tests.FolderTestOffline)
unittest.TextTestRunner(verbosity=2).run(suite2)

suite3 = unittest.TestLoader().loadTestsFromTestCase(mail_tests.MailTestOffline)
unittest.TextTestRunner(verbosity=2).run(suite3)