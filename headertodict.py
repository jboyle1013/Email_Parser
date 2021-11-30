import email
import json
import mailbox
import os
from email.parser import BytesParser
from email.policy import default
import sys
import threading


def header_dict_parser(jdict, inbox_dict, message_num, message):
    hdict = {"Date": [], "Recieved": [], "Subject": [], "From": [], "To": [], "Content-Type": [],
             "DKIM-signature": [], "Message-ID": [], "Mime-Version": [],
             "All Others": {}}  # This dict holds individual header values
    for item in message.items():  # goes through headers and add then to hdict
        if item[0].lower() == "date":
            hdict["Date"].append(item[1])
        elif item[0].lower() == "received":
            hdict["Recieved"].append(item[1])
        elif item[0].lower() == "subject":
            hdict["Subject"].append(item[1])
        elif item[0].lower() == "from":
            hdict["From"].append(item[1])
        elif item[0].lower() == "to":
            hdict["To"].append(item[1])
        elif item[0].lower() == "content-type":
            hdict["Content-Type"].append(item[1])
        elif item[0].lower() == "dkim-signature":
            hdict["DKIM-signature"].append(item[1])
        elif item[0].lower() == "message-id":
            hdict["Message-ID"].append(item[1])
        elif item[0].lower() == "mime-version":
            hdict["Mime-Version"].append(item[1])
        elif item[0] in hdict["All Others"].keys():
            hdict[item[0]].append(item[1])
        else:
            hdict["All Others"][item[0]] = [item[1]]

    jdict["Headers"] = hdict  # adding email headers to jdict

    datafile = open("jdict.json", "w")  # opening json file for writing
    json.dump(hdict, datafile, indent=4)  # printing data in nice format to file
    datafile.close()
