#!/usr/bin/env python
"""Log in and out of HiN's wireless network"""

import urllib2, getpass, getopt, sys

def main():
    """Main function"""

    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, 'sioh', ["status", "login", "logout", "help"])
    except getopt.GetoptError, err:
        print(err)
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt == "-s" or opt == "--status":
            print logonstatus()
        elif opt == "-i" or opt == "--login":
            log_in()
        elif opt == "-o" or opt == "--logout":
            log_out()
        elif opt == "-h" or opt == "--help":
            usage()
            sys.exit()
        else:
            usage()
            sys.exit()

def usage():
    """Print help for the user"""
    print "Usage:", sys.argv[0], "OPTION"
    print "Log in and out of HiN's wireless network\n"

    print "-s\t\tChecks if you are logged in or not"
    print "-i\t\tLog in to the network"
    print "-o\t\tLog out of the network"

    print "\nYou have to be connected to the Wireless Network before running the script"

def getlogonstatus(websitedata):
    """Check if we're logged in or not"""
    location = websitedata.rfind("You are not logged on.")

    if websitedata.rfind("You are not logged on") > 0:
        return "Not logged in" 
    else:
        split_site = websitedata.split()
        loginuser = split_site[70].partition("</b>")[0]
        return "Logged in as: " + loginuser

def logonstatus():
    """Uses the getlogonstatus function and prints out a user friendly message"""
    site = urllib2.urlopen("https://acs.hin.no/logon")
    the_page = site.read()
    print getlogonstatus(the_page)
    sys.exit()


def find_value(pagesplit, fieldname):
    """Tries to find the 'secret' and 'vernier' fields"""
    loc_field = pagesplit.index('name=' + fieldname) #location of field. The value is +2 fields relative to this.
    loc_value = loc_field + 2
    return pagesplit[loc_value].lstrip('value="').rstrip('">')

def log_in():
    """Logs the user in"""
    site = urllib2.urlopen("https://acs.hin.no/")
    the_page = site.read()
    page_split = the_page.split()

    username = raw_input("Username: ")
    password = getpass.getpass()
    secret = find_value(page_split, "secret")
    vernier = find_value(page_split, "verify_vernier")

    dummy = urllib2.urlopen("https://acs.hin.no/logon?query_string=&javaworks=1&vernier_id=hp&product_id=VNSS&releast_id=1.0&logon_status=0&guest_allowed=0&realm_required=0&secret="+secret+"&verify_vernier="+vernier+"&username="+username+"&password="+password+"&logon_action=Logon+User")

    logonstatus()
    sys.exit()

def log_out():
    """Logs the user out"""
    site = urllib2.urlopen("https://acs.hin.no/logon?logon_action=Logoff")
    logoffpage = site.read()
    
    if logoffpage.rfind("<!-- logged_off") > -1:
        print "You are now logged off..."
    else:
        print "Hmmm...not logged off... Strange..."

    #logonstatus()
    sys.exit()

if __name__ == "__main__":
    main()
