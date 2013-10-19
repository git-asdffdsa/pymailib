__author__ = 'asdffdsa'
#this file will not be synched
#accounts that are used in the tests
#to run the tests completely, you have to fill in valid email accounts

#accounts which should not be tested by the wizard
accounts_no_wizard = ['no_wizard_check@imagi.com']
#accounts which should not be tested by the passwordchecker
accounts_no_pwcheck = ['no_password_check@please.thanks']
#zb:
accounts = [
    {  #obviously, this must be deleted first
        'address': 'notreal@gmail.com',
        'password': 'testpassword',
        #for the wizard to validate
        'short_name': 'GMail',
        'get_protocol_string': 'imap', # or zb pop3
        'get_authentication_string': 'password-cleartext',
        'get_socket_string': 'SSL',
        'get_servername': 'imap.googlemail.com',
        'get_port': 993,
        'get_username': 'asdffdsa.test@gmail.com',
        'get_password': 'testpassword',
        'send_protocol_string': 'smtp',
        'send_authentication_string': 'password-cleartext',
        'send_socket_string': 'SSL',
        'send_servername': 'smtp.googlemail.com',
        'send_port': 465,
        'send_username': 'notreal@gmail.com',
        'send_password': 'testpassword'
    }
]