#!/usr/bin/python3
#
#
import os
import sys
import getpass
from vconnector.core import VConnector

def get_serverlist(listfile):
    f = open(listfile)
    serverlist = f.read().splitlines()
    f.close()
    return (serverlist)

def check_login(user,pw,host):
    try:
        client = VConnector(user=user, pwd=pw, host=host)
        client.connect()
        client.disconnect()
        del client
        return True
    except:
        client.disconnect()
        del client
        return False

if __name__ == '__main__':
    try:
        listfile = sys.argv[1]
        servers = get_serverlist(listfile)
        user = str(input("Enter username (domain\\userid) : "))
        pw = getpass.getpass("Enter password for " + user + " :")
        logfile = open("esx_check.log", "a+")
        for i in servers:
            if check_login(user,pw,i):
                logfile.write("SUCCESS: %s\n" % i)
                continue
            else:
                logfile.write("FAILED: %s\n" %i)
                continue
        logfile.close()
        print("Check complete. Refer esx_check.log file for further details.")
        sys.exit(0)
    except FileNotFoundError:
        print("File %s not found." % listfile)
        sys.exit(2)
    except IndexError:
        print("Usage: " + sys.argv[0] + " <server_list_file>")
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nUgghh.. Cancelling..")
        sys.exit(5)
    except Exception as x:
        print('Error: ' + str(x))
        sys.exit(3)
