the Account class
=================
[Methods](#methods)

[Values](#values)

[Usage Examples](#usage-examples)


Methods
-------
###auto_fill(address, password, guess=True)
Tries to fill the necessary fields by itself, if you provide an email-address and a general password.

The mechanics used are somehow derived from what Mozilla Thunderbird does.
#####Mechanism list:
*    looks for a local xml file; located in settings.LOCAL_AUTOCONFIG_PATH (by default not set)
*    looks for a xml file at the domain the email is registered to (e.g. asf@hotmail.com -> hotmail.com)
*    looks for a xml file at the mozilla database (autoconfig.thunderbird.net/v1.1/)
*    if *guess* is True, try to guess the settings, simply by trying to connect again and again to different servers

This method does **not** expect you to deliver the right password, you can reset the password later yourself
#####Possible outcomes:
1.   Neither of these mechanisms worked:

     In this case, the exception errors.settings_not_found is thrown.
2.   It worked, but you have to ask the user a question, or he has to do something manually

     Since some providers require different things (e.g. enable smtp), this could be the case... look at
     **return values** for further explanation
3.   Everything worked

     In this case, the second two return values are empty lists

#####Return Values:
This function returns three values:

1.    Which mechanism worked.

      An integer 1-4, tells you which of the mechanism provided the information
2.    A Todo List

      A list containing things to do. Every "thing to do" is a dictionary with the following fields:
      *    visiturl

           The URL the user has to visit and where he has to do something
      *    description

           A description what to do there.

3.    A Input Field List

      A list containing input fields which should be filled. Every "input field" is a dictionary with these fields:
      *    label

           How to name the input field (e.g. "User ID")
      *    example

           An example of what to fill in (e.g. "192930")
      *    key

           The actual name of the field, you need to use this later

      After you asked the user about the input field, you should give the values back to the account with the
      __substitute__ method

If the second two values are empty lists, there is nothing to do
###__substitute__(dictionary=None)
Use this to return the values you asked the user about after using auto_fill

For the dictionary, provide a dictionary with the form

"key": "value_the_user_gave_you"
###password_verify()
Returns True if the passwords are right, False if they aren't.
###read_from_db(account)
Fill this account with values read from the database.
Which account to use will be decided by what you provide by account; you can provide
*    A string

     In this case, an account with the address you provided will be searched in the database
*    An integers

     In this case, an account with the id you provided will be searched in the database
*    Anything else

     In this case, it will be interpreted as a database object and will be passed to the database directly

#####Possible outcomes
*    The account is filled and everything went good
*    There was no account with the id/address you provided

     In this case, an errors.account_not_found will be thrown

###save_to_db()
Save the account to the database
Values
------
*    id

     A unique id
*    address

     The email-address
*    short_name

     The shortname for the provider (e.g. hotmail.com -> hotmail)
*    send_servername; get_servername

     The servernames to send emails and to get emails
*    send_username; send_password; get_username; get_password

     The login crecedentials for the get- and send-server
*    send_protocol_string; get_protocol_string

     The names for the protocols (e.g. "smtp", "imap")
*    send_authentication_string; get_authentication_string

     The authentication methods (e.g. "plain")
*    send_socket_string; get_socket_string

     The sockets to use (e.g. "STARTTLS", "SSL")
*    send_port, get_port

     The ports to use

Usage Examples
--------------

#####a simple program that returns and imap/pop and smtp server for email adresses
```python
from pymailib import accounts

new_account = accounts.Account()
number = new_account.auto_fill(input("Please enter your email Address:\n"), '')
if number[0] == 4:
    print("The server had to be guessed!")
print(number)
print("Your " + new_account.get_protocol_string + " server is '" + new_account.get_servername + "'.")
print("Your " + new_account.send_protocol_string + " server is '" + new_account.send_servername + "'.")
```
