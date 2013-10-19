__author__ = 'asdffdsa'


from lxml import etree
import urllib.request
import urllib.error
import errors
import protocols
import threading
import copy
from os import path

GET_PROTOCOLS = ['imap', 'pop3']
SEND_PROTOCOLS = ['smtp']
AUTHENTICATIONS = ['password-cleartext']
SOCKETS = ['SSL', 'STARTTLS']
#the location of the local autoconfig files
LOCAL_AUTOCONFIG_PATH = ''

class Account:

    def __init__(self):
        self.id = 0
        self.address = ''
        self.short_name = ''
        self.send_protocol = 0
        self.send_authentication = 0
        self.send_socket = 0
        self.send_servername = ''
        self.send_port = 0
        self.send_username = ''
        self.send_password = ''
        self.get_protocol = 0
        self.get_authentication = 0
        self.get_socket = 0
        self.get_servername = ''
        self.get_port = 0
        self.get_username = ''
        self.get_password = ''

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def auto_fill(self, address, password, guess=True):
        """ mailwizard: finds the appropriate settings for you if you give over email account and password
        """

        domain = address.split('@')[1]
        #look for local file
        if LOCAL_AUTOCONFIG_PATH and not LOCAL_AUTOCONFIG_PATH == '':
            try:
                f = open(path.join(LOCAL_AUTOCONFIG_PATH, domain), 'r')
                self.__get_settings_xml__(address, password, f.read())
            except (FileNotFoundError, errors.settings_not_right):
                pass
            else:
                return 1
        #now look for file at autoconfig.domain (providers can store their own autoconfig files
        try:
            f = urllib.request.urlopen('http://autoconfig.' + domain)
            self.__get_settings_xml__(address, password, f.read())
        except (urllib.error.HTTPError, urllib.error.URLError, errors.settings_not_right):
            pass
        else:
            return 2
        #now look for file at the mozilla database
        try:
            f = urllib.request.urlopen('http://autoconfig.thunderbird.net/v1.1/' + domain)
            self.__get_settings_xml__(address, password, f.read())
        except (urllib.error.HTTPError, errors.settings_not_right):
            pass
        else:
            return 3
        if not guess:
            raise errors.settings_not_found()
        #now guess
        try:
            self.__guess_settings__(address, password, domain)
        except errors.settings_not_guessed:
            #throw exception
            raise errors.settings_not_found()
        return 4

    def __get_settings_xml__(self, address, password, string):
        """reads the settings out of an xml file used for mozilla thunderbird"""
        xml_tree = etree.fromstring(string)
        if xml_tree.get("version") != "1.1":
            raise errors.settings_not_right() # support for version 1.0 will be added later
        provider = xml_tree[0]  # the first element is the provider
        shortname = provider.find('displayShortName').text
        #always take the first incoming to come up
        incoming = None
        for incoming_protocol in provider.iter('incomingServer'):
            if (
                    incoming_protocol.get('type') in GET_PROTOCOLS
                    and incoming_protocol.find('authentication').text in AUTHENTICATIONS
                    and incoming_protocol.find('socketType').text in SOCKETS):
                #everything is supported
                incoming = incoming_protocol
                break
        #same for outgoing
        outgoing = None
        for outgoing_protocol in provider.iter('outgoingServer'):
            if (
                    outgoing_protocol.get('type') in SEND_PROTOCOLS
                    and outgoing_protocol.find('authentication').text in AUTHENTICATIONS
                    and outgoing_protocol.find('socketType').text in SOCKETS):
                #everything is supported
                outgoing = outgoing_protocol
                break
        if outgoing is None or incoming is None:
            raise errors.settings_not_right
        #fill the account
        self.address = address
        self.short_name = shortname
        self.get_password = password
        self.get_port = int(incoming.find('port').text)
        self.get_username = Account.__substitute_username__(address, incoming.find('username').text)
        self.get_servername = incoming.find('hostname').text
        self.get_protocol_string = incoming.get('type')
        self.get_authentication_string = incoming.find('authentication').text
        self.get_socket_string = incoming.find('socketType').text
        self.send_password = password
        self.send_port = int(outgoing.find('port').text)
        self.send_username = Account.__substitute_username__(address, outgoing.find('username').text)
        self.send_servername = outgoing.find('hostname').text
        self.send_protocol_string = outgoing.get('type')
        self.send_authentication_string = outgoing.find('authentication').text
        self.send_socket_string = outgoing.find('socketType').text

    def __guess_settings__(self, address, password, domain):
        """ guesses the appropriate settings and writes them into the instance
        """
        #one for the settings to get mails, one for the settings to send mails
        threads = []
        successlist_get = []
        successlist_send = []
        had_success = False
        #the function that will be called in the thread
        def threadfunction(account, successlist, guessfunction, u):
            try:
                account = guessfunction(domain, account)
            except errors.settings_not_guessed:
                success = 0
            else:
                success = 1
            successlist.append([u, success, account])

        i = 0
        for get_protocol in GET_PROTOCOLS:
            newguessfunction = getattr(protocols, 'guesssettings_' + get_protocol)
            newaccount = copy.deepcopy(self)
            newthread = threading.Thread(target=threadfunction, args=[newaccount, successlist_get, newguessfunction,
                                                                      i])
            newthread.start()
            threads.append(newthread)

        i = 0
        for send_protocol in SEND_PROTOCOLS:
            newguessfunction = getattr(protocols, 'guesssettings_' + send_protocol)
            newaccount = copy.deepcopy(self)
            newthread = threading.Thread(target=threadfunction, args=[newaccount, successlist_send, newguessfunction,
                                                                      i])
            newthread.start()
            threads.append(newthread)

        #now let them finish
        for i in threads:
            i.join()
        #now order the successlists by the index i
        successlist_get = sorted(successlist_get, key=lambda element: element[0])
        successlist_send = sorted(successlist_send, key=lambda element: element[0])
        for i in successlist_get:
            if i[1]: # success
                self.get_authentication = i[2].get_authentication
                self.get_protocol = i[2].get_protocol
                self.get_socket = i[2].get_socket
                self.get_servername = i[2].get_servername
                self.get_username = address
                self.get_password = password
                had_success = True
                break
        if not had_success:
            raise errors.settings_not_guessed
        had_success = False
        for i in successlist_send:
            if i[1]: # success
                self.send_authentication = i[2].send_authentication
                self.send_protocol = i[2].send_protocol
                self.send_socket = i[2].send_socket
                self.send_servername = i[2].send_servername
                self.send_username = address
                self.send_password = password
                had_success = True
                break
        if not had_success:
            raise errors.settings_not_guessed


    def passwords_verify(self):
        return self.test_password_get() and self.test_password_send()

    def test_password_send(self):
        method = getattr(protocols, "testpassword_" + self.send_protocol_string)
        return method(self)

    def test_password_get(self):
        method = getattr(protocols, "testpassword_" + self.get_protocol_string)
        return method(self)

    def test_settings_send(self):
        method = getattr(protocols, "testsettings_" + self.send_protocol_string)
        return method(self)

    def test_settings_get(self):
        method = getattr(protocols, "testsettings_" + self.get_protocol_string)
        return method(self)

    @staticmethod
    def __substitute_username__(address, string):
        """ substitutes strings found in mozilla's xml files
        """
        string = string.replace('%EMAILLOCALPART%', address.split('@')[0])
        string = string.replace('%EMAILADDRESS%', address)
        return string

    def __setprop__(self, value, indexlist, attribute_name):
        """ set a property by assigning the index of a list of a statement
        """
        setattr(self, attribute_name, indexlist.index(value))

    def __getprop__(self, indexlist, attribute_name):
        """ translate a property by using it as index of a indexlist
        """
        return indexlist[getattr(self, attribute_name)]

    send_protocol_string = property(lambda self: self.__getprop__(SEND_PROTOCOLS, 'send_protocol'),
                                    lambda self, value: self.__setprop__(value, SEND_PROTOCOLS, 'send_protocol'))
    send_authentication_string = property(lambda self: self.__getprop__(AUTHENTICATIONS, 'send_authentication'),
                                          lambda self, value: self.__setprop__(value,
                                                                               AUTHENTICATIONS, 'send_authentication'))
    send_socket_string = property(lambda self: self.__getprop__(SOCKETS, 'send_socket'),
                                  lambda self, value: self.__setprop__(value, SOCKETS, 'send_socket'))
    get_protocol_string = property(lambda self: self.__getprop__(GET_PROTOCOLS, 'get_protocol'),
                                   lambda self, value: self.__setprop__(value, GET_PROTOCOLS, 'get_protocol'))
    get_authentication_string = property(lambda self: self.__getprop__(AUTHENTICATIONS, 'getauthentication'),
                                         lambda self, value: self.__setprop__(value,
                                                                               AUTHENTICATIONS, 'get_authentication'))
    get_socket_string = property(lambda self: self.__getprop__(SOCKETS, 'get_socket'),
                                 lambda self, value: self.__setprop__(value, SOCKETS, 'get_socket'))