__author__ = 'asdffdsa'
#settings that are used for the tests

#fields in the accounts that are not used in the account class
accounts_not_needed = ['password']

#fields in the account class that should not be tested against the wizard
accountfields_no_wizard = ['short_name']
#terms for the email search
searchTestValues = {
    'test': {
        'name__': 'test'
    }
}

#wrong passwords for the password checker
false_passwords = [
        'asdf',
        '--',
        '_/\\NOPE//°!"§$%&/()=   #+~*´`',
        '\', DROP TABLE \'accounts\'--'
]

#minimum and maximum password length for the random password checker
random_password_lengths = [2, 7]
#how much passwords per account to try
random_password_times = 1