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

random_foldername_lengths = [2, 100]
#how much foldernames per virtual folder (between first and second value)
random_foldername_times = [1, 50]
#how much virtual folders per account
folders_per_account = [1, 10]

random_mail_field_strings = {
    #will be strings with lengths between the two values
    'sender': [2, 100],
    '__full_header__': [50, 100],
    'folder': [2, 100],
    'subject': [2, 100]
}
random_mail_field_integers = {
    #will be integers between the first and the second values
    'server_id': [1, 10000],
    'time_sent': [0, 10000],
    'size': [0, 10000],
    'answer_to': [0,10000]

}
random_mail_field_lists = {
    #will be a lists with {firstvalue} to {secondvalue} strings; each between {thirdvalue} and {fourthvalue} long
    'receivers': [0, 20, 2, 200],
    'flags': [0, 20, 2, 200],
    'cc': [0, 20, 2, 200],
    'bcc': [0, 20, 2, 200]
}
#how much mails to generate
mails_all_in_all = [20, 30]