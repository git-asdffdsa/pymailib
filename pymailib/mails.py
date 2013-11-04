from pymailib import settings, accounts, protocols

__author__ = 'asdffdsa'
import json

from . import settings
from . import accounts
from . import protocols

class Attachment:
    """ a class that can hold any email attachment
    """
    def __init__(self):
        self.is_loaded = False
        self.source = ''
        self.__content__ = None
        self.account = accounts.Account()
        self.name = ''

    def __get_content__(self):
        if self.__content__ is None:
            protocol, url = self.source.split('://')
            get_function = getattr(protocols, 'get_content_' + protocol)
            self.__content__ = get_function(url, self.account)
        return self.__content__

    def __set_content__(self, content):
        self.__content__ = content
        self.source = 'explicit://explicit'

    content = property(__get_content__, __set_content__)


class Mail():
    """ a class that holds a specific mail, including attachments
    it can easily be converted to the python std email.message.Message class
    """  # TODO
    def __init__(self):
        #id the database uses for this message
        self.id = 0
        #id the server uses for this message
        self.server_id = 0
        #an account can be bound to the email
        self.__bound_account__ = None
        self.__bound_account_is_receiver__ = False
        self.sender = ''
        self.receivers = []
        self.time_sent = 0
        self.__full_header__ = None
        self.flags = []
        self.folder = ''
        self.size = 0
        self.subject = ''
        self.answer_to = 0
        self.seen = False
        self.cc = []
        self.bcc = []
        self.attachments = []
        self.__content__ = ''
        self.__has_content__ = False

    def __eq__(self, other):
        #simply comparing __dict__ does not work, because the flags, cc and bcc, etc could have a different order
        #thats why we order them first
        if isinstance(other, self.__class__):
            self.flags.sort()
            self.cc.sort()
            self.bcc.sort()
            self.receivers.sort()
            other.flags.sort()
            other.cc.sort()
            other.bcc.sort()
            other.receivers.sort()
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __load_content__(self):
        """ loads the content from the internet, if not available locally, and returns it
        """
        if self.__has_content__:
            return self.__content__
        else:
            raise NotImplementedError  # TODO

    def __save_content__(self, text):
        self.__content__ = text
        self.__has_content__ = True

    def save(self):
        self.save_to_db()
        self.save_to_server()

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

    def save_to_server(self):
        pass  # TODO

    def __get_bound_account_id__(self):
        """ returns the id of the bound account, zero if there is none
        """
        if self.__bound_account__ is None:
            return 0
        else:
            return self.__bound_account__.id

    def __set_bound_account_id__(self, number):
        if number == 0:
            return
        if self.__bound_account__ is None:
            self.__bound_account__ = accounts.Account()
        self.__bound_account__.read_from_db(number)
        for attachment in self.attachments:
            attachment.account = self.__bound_account__

    def __get_sender_account__(self):
        if self.__bound_account_is_receiver__:
            return None
        return self.__bound_account__

    def __set_sender_account__(self, account):
        self.__bound_account_is_receiver__ = False
        self.__bound_account__ = account

    def __get_receiver_account__(self):
        if self.__bound_account_is_receiver__:
            return None
        return self.__bound_account__

    def __set_receiver_account__(self, account):
        self.__bound_account_is_receiver__ = True
        self.__bound_account__ = account

    def __set_attachments_json__(self, string):
        for sublist in json.loads(string):
            new_attachment = Attachment()
            new_attachment.source = sublist[0]
            new_attachment.name = sublist[1]
            new_attachment.account = self.__bound_account__

    def __get_attachments_json__(self):
        new_structure = []
        for attachment in self.attachments:
            new_structure.append([attachment.source, attachment.name])
        return json.dumps(new_structure)

    def make_message_class(self):
        pass  # TODO

    def send(self):
        if self.sender_account is None:
            raise AttributeError
        method = getattr(protocols, "sendmail_" + self.__bound_account__.send_protocol_string)
        return method(self)

    content = property(__load_content__, __save_content__)
    sender_account = property(__get_sender_account__, __set_sender_account__)
    receiver_account = property(__get_receiver_account__, __set_receiver_account__)
    bound_account_id = property(__get_bound_account_id__, __set_bound_account_id__)
    attachments_json = property(__get_attachments_json__, __set_attachments_json__)
    flags_json = property(lambda self: json.dumps(self.flags),
                            lambda self, x: setattr(self, 'flags', json.loads(x)))
    cc_json = property(lambda self: json.dumps(self.cc),
                         lambda self, x: setattr(self, 'cc', json.loads(x)))
    bcc_json = property(lambda self: json.dumps(self.bcc),
                          lambda self, x: setattr(self, 'bcc', json.loads(x)))
    receivers_json = property(lambda self: json.dumps(self.receivers),
                          lambda self, x: setattr(self, 'receivers', json.loads(x)))
