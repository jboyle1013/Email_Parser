import email
import json
import mailbox
import os
from email.parser import BytesParser
from email.policy import default
import sys
import threading
from headertodict import *
import concurrent.futures
from queue import Queue
from htmlparser import MyHTMLParser
from content_parser import content_parser
import chardet



def emails_loop():
    parser = MyHTMLParser()
    directory = "UaA-Database_Emails"  # This is where the files are
    emails_list = []  # This is the final list of dicts to go into data.json
    num_inboxes = 1  # I'm manually starting the count at 1 for readability
    directory_completed = 0  # This is the counter for progress bar 1
    inbox_completed = 0  # This is the counter for progress bar 2
    numfile = len(os.listdir(directory))  # number of files in directory
    header_sub_dict = {}  # header subjects dictionary
    header_sub = []  # header subjects overall
    total_message_num = 0  # total number of messages in database
    total_inbox_num = 0  # total number of inboxes in database
    nums = {}

    for entry in os.scandir(directory):  # This is looping through each file in the directory above
        file_str = str(entry.name)  # Turns the name of the entry to a string
        filepath = directory + "/"
        file_name = filepath + file_str  # Adds the folder to the filename so it can be read in the right location
        name = file_str.split(".")[1]  # Pulls name of the ID who owns this inbox
        print(name)
        mb = mailbox.mbox(file_name, factory=BytesParser(policy=default).parse)  # Reading in mbox file
        mblen = len(mb)  # number of messages
        message_num = 1  # I'm manually starting the count at 1 for readability
        msg_dict = {}  # Holds list of messages in inbox
        jdict = {}  # Holds individual email headers
        htmldict = {}
        inboxdict = {}  # Holds inbox
        inbox_completed = 0  # This is the counter for progress bar 2
        nums[name] = mblen
        for _, message in enumerate(mb):  # Loops through messages in inbox
            datafile = open("MessageLinks.json", "w")  # opening json file for writing
            linkdict = {"Website": [],
                        "Image": []}
            msg_dict[f"Message Number {message_num}:"] = {}
            json.dump(linkdict, datafile, indent=4)  # printing data in nice format to file
            datafile.close()
            print(_)
            t1 = threading.Thread(target=header_dict_parser, args=(jdict, inboxdict, message_num, message))
            t2 = threading.Thread(target=content_parser, args=(message, parser))
            t1.start()
            t2.start()

            t1.join()
            t2.join()


            
            jdfile = open("jdict.json", "r")  # opening json file for writing
            jdict = json.load(jdfile)
            jdfile.close()
            mlfile = open("MessageLinks.json", "r")  # opening json file for writing
            htmldict = json.load(mlfile)
            total_message_num = total_message_num + 1
              # keeping track of number of messages
            msg_dict[f"Message Number {message_num}:"]["Headers"] = jdict  # adding message headers to list of messages in inbox
            msg_dict[f"Message Number {message_num}:"]["Links"] = htmldict
            jdict = {}  # clearing dict for next message
            message_num = message_num + 1
        inboxdict["Inbox Number"] = num_inboxes  # Adding the inbox numver to inbox dict
        inboxdict["Number Of Messages"] = message_num - 1
        inboxdict[name] = msg_dict  # adding inbox messages to inboxdict
        emails_list.append(inboxdict)  # adding inbox to emails list
        num_inboxes = num_inboxes + 1  # keeping track of number of inboxes
        total_inbox_num = total_inbox_num + 1

    total = {
        "Total Number of Emails": total_message_num,
        "Total Number of Inboxes": total_inbox_num
    }
    nums["Total"] = total_message_num
    header_sub_dict["Total"] = header_sub

    emails_list.append(total)
    datafile = open("data.json", "w")  # opening json file for writing
    json.dump(emails_list, datafile, indent=4)  # printing data in nice format to file
    datafile.close()  # closing file
