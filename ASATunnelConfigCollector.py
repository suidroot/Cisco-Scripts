#!/usr/bin/env python
"""  
stolen from https://pynet.twb-tech.com/blog/python/paramiko-ssh-part1.html 
"""

from networkstatesystem.vendors.ssh.sshhelper import *
import argparse
from sys import exit


def initargs():
    """ initialize variables with command-line arguments """
    parser = argparse.ArgumentParser(description='input -f [file]')
    parser.add_argument('-i', '--ip', \
        help='ASA IP address', \
        default='10.0.0.1')
    parser.add_argument('-u', '--username', \
        help='Logon Username', \
        default='admin')
    parser.add_argument('-p', '--password', \
        help='SSH/Telnet Password', \
        default='1234567')
    parser.add_argument('-e', '--enable', \
        help='Enable Password', \
        default='1234567')
    parser.add_argument('-t', '--tunnelip', \
        help='Search by Tunnel IP')
    parser.add_argument('-m', '--mapnumber', \
        help='Search by Crypto Map Number')

    arg = parser.parse_args()

    return arg

def addtoconfig(thebuffer, totallist):

    # lines = thebuffer.split("\n")
    lines = thebuffer
    lines = lines[1:]
    lines = lines[:-1]

    for line in lines:
        # print line
        totallist.append(line)

    return totallist


if __name__ == '__main__':

    args = initargs()

    ip = args.ip
    username = args.username
    password = args.password
    enable = args.enable

    completeconfig = []

    if args.tunnelip:
        tunnelendpoint = args.tunnelip
        collectby = 'ip'
    elif args.mapnumber:
        cryptomapnumber = args.mapnumber
        collectby = 'number'
    else:
        exit("Specify a Search Parameter -t or -m")

    remote_conn_pre, remote_conn = \
        sshconnect(ip, username, password, 'asa', enable)

    if collectby.lower() == 'ip':
        # Gather Tunnel Group By IP

        output = ssh_runcommand(remote_conn, \
            "show running-config tunnel-group " + tunnelendpoint + "\n", \
            recvbuffer=2000, \
            recvsleep=2)
        completeconfig = addtoconfig(output, completeconfig)

        # Determine Crypto Map Number form IP Address
        output = ssh_runcommand(remote_conn, \
            "show run crypto map | i " + tunnelendpoint + "\n", \
            recvbuffer=2000, \
            recvsleep=2)

        cryptomapnumber = output[1].split(" ")[3]
        cryptomapname = output[1].split(" ")[2]

        # Collect all Crypto Map Configuration
        output = ssh_runcommand(remote_conn, \
            "show run crypto map | i " + cryptomapname + " " + \
            cryptomapnumber + " \n", \
            recvbuffer=2000, \
            recvsleep=2)

        completeconfig = addtoconfig(output, completeconfig)
        # Determine access-list name from Crypto Map config

        for line in output: 
            if "match" in line:
                accesslistname = line.split(" ")
                accesslistname = accesslistname[6]
                accesslistname = accesslistname.strip()

        # Collect access-list by Name
        output = ssh_runcommand(remote_conn, \
            "show run access-list " + accesslistname + " \n", \
            recvbuffer=2000, \
            recvsleep=2)
        completeconfig = addtoconfig(output, completeconfig)


    elif collectby.lower() == 'number':
        # Determine Crypto Map by Name
        output = ssh_runcommand(remote_conn, \
            'show run crypto map | i interface\n', \
            recvbuffer=2000, \
            recvsleep=2)
        cryptomapname = output[1].split(" ")[2]

        # Collect Crypto Map config
        output = ssh_runcommand(remote_conn, \
            'show run crypto map | i ' + cryptomapname + " " + \
            cryptomapnumber + ' \n', \
            recvbuffer=2000, \
            recvsleep=2)
        completeconfig = addtoconfig(output, completeconfig)

        # Determine Tunnel IP address
        for line in output: 
            if "set peer" in line:
                tunnelendpoint = line.split(" ")
                tunnelendpoint = tunnelendpoint[6]
                tunnelendpoint = tunnelendpoint.strip()

        # Determine access-list name from Crypto Map config
        for line in output: 
            if "match" in line:
                accesslistname = line.split(" ")
                accesslistname = accesslistname[6]
                accesslistname = accesslistname.strip()

        # Gather Tunnel Group By IP
        output = ssh_runcommand(remote_conn, \
            "show running-config tunnel-group " + tunnelendpoint + "\n", \
            recvbuffer=2000, \
            recvsleep=2)
        completeconfig = addtoconfig(output, completeconfig)

        # Collect access-list by Name
        output = ssh_runcommand(remote_conn, \
            "show run access-list " + accesslistname + " \n", \
            recvbuffer=2000, \
            recvsleep=2)
        completeconfig = addtoconfig(output, completeconfig)

    else:
        exit("No correct Search type, this should not happen")

    # print "\n\n The Whole thing\n"
    print "\n".join(completeconfig)



