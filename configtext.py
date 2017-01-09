#!/usr/bin/env python
import ConfigParser
import pprint
import argparse
import cgi
from networkstatesystem.vendors.ssh.sshhelper import *


""" this will run pre determined sets of commands on specified device

username
password
enable password

will be passed as arguments

"""

configfile = "command.cfg"


def initargs():
    """ initialize variables with command-line arguments """
    parser = argparse.ArgumentParser(description='input -f [file]')
    parser.add_argument('-i', '--ip', \
        help='IP Address', \
        default='10.5.6.254')
    parser.add_argument('-u', '--username', \
        help='SSH Username', \
        default='username')
    parser.add_argument('-p', '--password', \
        help='SSH Password', \
        default='password')
    parser.add_argument('-e', '--enable', \
        help='Enable Password', \
        default='1234567')

    arg = parser.parse_args()

    return arg


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def htmlheader(title):
    contents = '''Content-Type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title>%s</title>
</head><body>'''

    print contents % title

def htmlpre(contents):
    print "<pre>"
    print contents
    print "</pre>"

def htmlheadtag(contents, level):
    if level > 4:
        print "Header Error!"
    else:
        level = 3

    level = str(level)
    contents = "<h" + level + ">" + contents + "</h" + level + ">"
    print contents

def htmlfooter():

    print "</body></html>"


def htmllistbox(name, listofoptions):

    print '<select name="{0}" multiple="single">'.format(name)

    for line in listofoptions:
        print "<option>{0}</option>".format(line)

    print "</select>"


def someformstuff():
    
    form = cgi.FieldStorage()
    if (form.has_key("action") and form.has_key("username") \
    and form.has_key("password")):
        if (form["action"].value == "display"):
            result = test(form["username"].value, form["password"].value)
            display_page(result)
    else:
        generate_form()

if __name__ == '__main__':

    args = initargs()

    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    allsections = Config.sections()

    ip = args.ip
    username = args.username
    password = args.password
    enable = args.enable

    everything = {}

    for line in Config.sections():
        everything[line] = ConfigSectionMap(line)

    # print allsections

    pprint.pprint(everything)

    htmlheader('Choose Command')
    htmllistbox('commandname', everything.keys())
    htmlfooter()

    thecommands = raw_input("commands:")

    if everything[thecommands]['arguements'] == 'True':
        interface = raw_input("interface:")


    htmlheader('Command Output')

    remote_conn_pre, remote_conn = \
        sshconnect(ip, username, password, 'ios', enable)

    for command in everything[thecommands]['commandlist'].split(","):
        command = command.strip()

        if everything[thecommands]['arguements'] == 'True':
            runcommand = everything[thecommands][command] + " " + interface
        else:
            runcommand = everything[thecommands][command]

        htmlheadtag(runcommand, 2)

        output = ssh_runcommand(remote_conn, \
            runcommand + "\n", \
            recvbuffer=2000, \
            recvsleep=2)

        htmlpre("\n".join(output))

        htmlfooter()

        # pprint.pprint(output)



