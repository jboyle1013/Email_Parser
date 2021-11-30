from chardet import detect
import json


def content_parser(message, parser):
    messagedict = {}
    if message.is_multipart():
        html = None

        for part in message.get_payload():
            if part.get_content_charset() is None:
                charset = detect(str(part))['encoding']
            else:
                charset = part.get_content_charset()
            if part.get_content_type() == 'text/plain':
                text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
            if part.get_content_type() == 'text/html':
                html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
            if part.get_content_type() == 'multipart/alternative':
                for subpart in part.get_payload():
                    if subpart.get_content_charset() is None:
                        charset = detect(str(subpart))['encoding']
                    else:
                        charset = subpart.get_content_charset()
                    if subpart.get_content_type() == 'text/plain':
                        text = str(subpart.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                    if subpart.get_content_type() == 'text/html':
                        html = str(subpart.get_payload(decode=True), str(charset), "ignore").encode('utf8',
                                                                                                    'replace')

        if html is None:
            messagetext = text.strip()
            messagedict["Message"] = messagetext
            """datafile = open( "Message.json", "w" )  # opening json file for writing
            json.dump( messagedict, datafile, indent=4 )  # printing data in nice format to file
            datafile.close()"""
        else:
            html = html.strip()
            parser.feed(html.decode("utf-8"))


    else:
        text = str(message.get_payload(decode=True), message.get_content_charset(), 'ignore').encode('utf8', 'replace')
        messagetext = text.strip()
        messagedict["Message"] = messagetext
        """datafile = open( "Message.json", "w" )  # opening json file for writing
        json.dump( messagedict, datafile, indent=4 )  # printing data in nice format to file
        datafile.close()"""
