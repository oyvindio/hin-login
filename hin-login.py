#!/usr/bin/env python
"""Log in and out of HiN's wireless network"""

import urllib2, getpass, sys
from optparse import OptionParser

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

    sys.exit()


def main():
    """Main function"""

    parser = OptionParser(description='Lets you log in via the authentication on the wireless network at HiN. You have to be connected to the wireless network before trying to use this program to authenticate.')
    
    parser.add_option("-s", "--status", 
                      action="store_true", 
                      dest="status",
                      help="Print status -- checks if you are logged in or not.")
    parser.add_option("-i", "--login", 
                      action="store_true", 
                      dest="login",
                      help="Log in via the authentication site.")
    parser.add_option("-o", "--logout", 
                      action="store_true", 
                      dest="logout",
                      help="Log out.")

    (options, args) = parser.parse_args()

    if options.status:
        logonstatus()
    elif options.login:
        log_in()
    elif options.logout:
        log_out()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
