#!/usr/bin/env python
# encoding: utf-8

import sys
import getopt
import base64
import requests

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    first_blood = False # indicates when to start counting the posts

    count_read = 0
    count_unread = 0

    def handle_starttag(self, tag, attrs):
        """ Overrides handle_starttag:
            When the <div> tag with class 'ipsLayout_content' is found,
            set the flag `first_blood` in order to search into <tr> tags.
            <tr> tags have an attribute class, where there is the word
            '_recordRow' some others and the word 'unread' if the post is
            unread. If the post is read, simply there is no 'unread'.
        """
        # Scan the <div> tags
        if tag == u'div' and not self.first_blood:
            for attr in attrs:
                if attr[0] == u'class' and attr[1] == u'ipsLayout_content':
                    self.first_blood = True
                    break

        # Scan the <tr> tags
        if tag == 'tr' and self.first_blood:
            for attr in attrs:
                if attr[0] == u'class' and u'_recordRow' in attr[1]:
                    if (u'unread' in attr[1]):
                        self.count_unread += 1;
                    else:
                        self.count_read += 1;

    #def handle_startendtag(self, tag, attrs):
    #    if (tag == u'img'):
    #        for attr in attrs:
    #            if (attr[0] == u'src'):
    #                print "\t" + str(attr)


def parse_args(argv):
    """ Parse the arguments from `argv`. They must be a username and
        a password as the usage says. I unexpected arguments are met,
        then exit.
    """
    username, password = '', ''

    try:
        opts, args = getopt.getopt(argv,"hu:p:",["username=","password="])
    except getopt.GetoptError:
        print 'true_insomniac.py -u <username> -p <password>'
        sys.exit(2)

    if len(opts) == 0:
        print 'true_insomniac.py -u <username> -p <password>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'true_insomniac.py -u <username> -p <password>'
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg

    return username, password


def main(argv):
    url = 'http://www.insomnia.gr/index.php?app=core&module=search&do=user_activity&mid=223995'

    # Parse the arguments
    username, password = parse_args(argv)

    # Get the contents of the url
    r = requests.get(url, auth=(username, password)) # send auth unconditionally
    r.raise_for_status() # raise an exception if the authentication fails
    user_contents = r.text

    # Parse the contents of the url
    parser = MyHTMLParser()
    parser.feed(user_contents);

    # Print the results
    print "READ   = " + str(parser.count_read)
    print "UNREAD = " + str(parser.count_unread)


if __name__ == "__main__":
    main(sys.argv[1:])

