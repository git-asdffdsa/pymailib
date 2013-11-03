__author__ = 'asdffdsa'
import random
import string
import accounts
import folders
import mails
from . import testsettings


def make_accountlist(account_dicts):
    accountlist = []
    for account in account_dicts:
        newaccount = accounts.Account()
        for argument, value in account.items():
            if argument in testsettings.accounts_not_needed:
                continue
            setattr(newaccount, argument, value)
        accountlist.append(newaccount)
    return accountlist


def make_folderlist_fictional(accountlist):
    folderlist = []
    for account in accountlist:
        foldernames_used = []
        folders_per_account = random.choice(range(testsettings.folders_per_account[0],
                                                  testsettings.folders_per_account[1]))
        for u in range(0, folders_per_account):
            newfolder = folders.Folder()
            foldername_times = random.choice(range(testsettings.random_foldername_times[0],
                                                   testsettings.random_foldername_times[1]))
            for i in range(0, foldername_times):
                #no foldername per account shall be used twice
                foldername = None
                while True:
                    foldername_length = random.choice(range(testsettings.random_foldername_lengths[0],
                                                            testsettings.random_foldername_lengths[1]))
                    foldername = ''
                    for u in range(0, foldername_length):
                        foldername += random.choice(string.printable)
                    if foldername not in foldernames_used:
                        break
                newfolder.enrich(account, foldername, False)
                foldernames_used.append(foldername)
            folderlist.append(newfolder)
    #make some random recombinations
    #but recombinations should never be the same
    recombinations_used = []
    #never use the already recombinated
    folderlist_length = len(folderlist) - 1
    for i in range(0, folderlist_length):
        first_index = random.choice(range(0, folderlist_length))
        second_index = random.choice(range(0, folderlist_length))
        if [first_index, second_index] in recombinations_used or [second_index, first_index] in recombinations_used:
            #so we already had that one
            continue
        #new combination!
        recombinations_used.append([first_index, second_index])
        folderlist.append(folderlist[first_index] + folderlist[second_index])
    return folderlist

def make_maillist_fictional(accountlist):
    maillist = []
    mail_number = random.randint(testsettings.mails_all_in_all[0], testsettings.mails_all_in_all[1])
    for i in range(0, mail_number):
        new_mail = mails.Mail()
        for argument, value in testsettings.random_mail_field_strings.items():
            # the attributes that are strings
            new_string = ''
            string_length = random.randint(value[0], value[1])
            for u in range(0, string_length):
                new_string += random.choice(string.printable)
            setattr(new_mail, argument, new_string)
        for argument, value in testsettings.random_mail_field_lists.items():
            # the attributes that are lists filled with strings
            number_of_elements = random.randint(value[0], value[1])
            new_list = []
            for u in range(0, number_of_elements):
                new_string = ''
                string_length = random.randint(value[2], value[3])
                for o in range(0, string_length):
                    new_string += random.choice(string.printable)
                new_list.append(new_string)
            setattr(new_mail, argument, new_list)
        for argument, value in testsettings.random_mail_field_integers.items():
            # the attributes that are simple numbers
            setattr(new_mail, argument, random.randint(value[0], value[1]))
        # now set a random account as receiver and as sender
        #accountlist.append(None)
        new_mail.receiver_account = random.choice(accountlist)
        new_mail.sender_account = random.choice(accountlist)
        new_mail.id = i
        maillist.append(new_mail)
    return maillist