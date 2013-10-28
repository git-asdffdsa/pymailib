__author__ = 'asdffdsa'

import accounts
import pickle
import settings
import json

class Mail:
    """ a class that holds a specific mail
    """
    def __init__(self):
        #id the database uses for this message
        self.id = 0
        #id the server uses for this message
        self.server_id = 0
        self.sender_account = None
        self.receiver_account = None
        self.sender = ''
        self.receiver = ''
        self.time_sent = 0
        self.full_header = ''
        self.flags = []
        self.folder = ''
        self.seen = False
        self.size = 0
        self.subject = ''
        self.answer_to = 0
        self.cc = []
        self.bcc = []
        self.__content__ = ''
        self.__has_content__ = False

    def __eq__(self, other):
        #simply comparing __dict__ does not work, because the flags, cc and bcc could have a different order
        #thats why we order them first
        if isinstance(other, self.__class__):
            self.flags.sort()
            self.cc.sort()
            self.bcc.sort()
            other.flags.sort()
            other.cc.sort()
            other.bcc.sort()
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __load_content__(self):
        """ loads the content from the internet, if not available, and returns it
        """
        return 'THIS IS CONTENT'
        pass

    def save(self):
        """ saves the whole mail to the database as well as to the server (if imap)
        """
        pass

    def __save_content__(self, text):
        self.__content__ = text

    def save_to_db(self):
        """ save the whole mail to the database
        """
        settings.database.save_mail(self)

    def read_from_db(self, mail):
        """ read from the database by the given id or specific mail
        """
        if type(mail) is int:
            settings.database.read_to_mail(self, settings.database.search_mail_by_id(mail))
        else:
            settings.database.read_to_mail(self, mail)


    def __get_sender_account_id__(self):
        """ returns the id of the sender account, zero if there is none
        """
        if self.sender_account is None:
            return 0
        else:
            return self.sender_account.id

    def __get_receiver_account_id__(self):
        """ same as __get_sender_account_id__, for receiver
        """
        if self.receiver_account is None:
            return 0
        else:
            return self.receiver_account.id

    def __set_receiver_account_id__(self, number):
        """ set the receiver id, if its not zero, load the receiver account from the db
        """
        if number == 0:
            return
        self.receiver_account = accounts.Account()
        self.receiver_account.read_from_db(number)

    def __set_sender_account_id__(self, number):
        """ set the sender account id, if its not zero, load the account from the db
        """
        if number == 0:
            return
        self.sender_account = accounts.Account()
        self.sender_account.read_from_db(number)

    def save_to_server(self):
        """ saves the whole mail to the server (if imap)
        """



    content = property(__load_content__, __save_content__)
    sender_account_id = property(__get_sender_account_id__, __set_sender_account_id__)
    receiver_account_id = property(__get_receiver_account_id__, __set_receiver_account_id__)
    flags_json = property(lambda self: json.dumps(self.flags),
                            lambda self, x: setattr(self, 'flags', json.loads(x)))
    cc_json = property(lambda self: json.dumps(self.cc),
                         lambda self, x: setattr(self, 'cc', json.loads(x)))
    bcc_json = property(lambda self: json.dumps(self.bcc),
                          lambda self, x: setattr(self, 'bcc', json.loads(x)))

    pass