__author__ = 'asdffdsa'
#this file will not be synched
#accounts that are used in the tests
#to run the tests completely, you have to fill in valid email accounts

#accounts which should not be tested by the wizard
accounts_no_wizard = []
#accounts which should not be tested by the passwordchecker
accounts_no_pwcheck = ['asdffdsa.test@outlook.com']
#zb:
accounts = [
    #delete or comment out this account, since these settings won't work
    {
        'id': 0,
        'address': 'asdffdsa.test@gmail.com',
        'password': 'testpassword',
        #for the
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
        'send_username': 'asdffdsa.test@gmail.com',
        'send_password': 'testpassword'
    },
    {
        'id': 1,
        'address': 'asdffdsa.test@outlook.com',
        'password': 'test1234',
        'short_name': 'Hotmail',
        'get_protocol_string': 'imap', # or zb pop3
        'get_authentication_string': 'password-cleartext',
        'get_socket_string': 'SSL',
        'get_servername': 'imap-mail.outlook.com',
        'get_port': 993,
        'get_username': 'asdffdsa.test@outlook.com',
        'get_password': 'test1234',
        'send_protocol_string': 'smtp',
        'send_authentication_string': 'password-cleartext',
        'send_socket_string': 'STARTTLS',
        'send_servername': 'smtp-mail.outlook.com',
        'send_port': 587,
        'send_username': 'asdffdsa.test@outlook.com',
        'send_password': 'test1234'
    },
    {
        'id': 2,
        'address': 'asdf.fdsa.1@gmx.net',
        'password': '!§$%&/()',
        'short_name': 'GMX',
        'get_protocol_string': 'imap', # or zb pop3
        'get_authentication_string': 'password-cleartext',
        'get_socket_string': 'SSL',
        'get_servername': 'imap.gmx.net',
        'get_port': 993,
        'get_username': 'asdf.fdsa.1@gmx.net',
        'get_password': '!§$%&/()',
        'send_protocol_string': 'smtp',
        'send_authentication_string': 'password-cleartext',
        'send_socket_string': 'SSL',
        'send_servername': 'mail.gmx.net',
        'send_port': 465,
        'send_username': 'asdf.fdsa.1@gmx.net',
        'send_password': '!§$%&/()'
    }
    #add more accounts for better testing; also add pop3-only accounts
]