import json
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        datafile = open("MessageLinks.json", "r")  # opening json file for writing
        linkdict = json.load(datafile)
        datafile.close()

        if tag == 'a':  # or tag == 'td' or tag == 'span':
            for attr in attrs:
                if attr[0] == 'href' or attr[0] == 'data-saferedirecturl':
                    linkdict["Website"].append(attr[1])
                if attr[0] == 'ping':
                    pass
        if tag == 'img':  # or tag == 'td' or tag == 'span':
            for attr in attrs:
                if attr[0] == 'src':
                    linkdict["Image"].append(attr[1])

        datafile = open("MessageLinks.json", "w")  # opening json file for writing
        json.dump(linkdict, datafile, indent=4)  # printing data in nice format to file
        datafile.close()


