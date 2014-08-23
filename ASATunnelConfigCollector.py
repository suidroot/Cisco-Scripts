#!/usr/bin/env python
"""  stolen from https://pynet.twb-tech.com/blog/python/paramiko-ssh-part1.html """


import paramiko
import argparse
from time import sleep
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

def disable_paging(remote_conn,device_type):
    '''Disable paging on a Cisco ASA'''

    if device_type.lower() == 'ios':
        remote_conn.send("terminal length 0\n")
    elif device_type.lower() == 'asa':
        remote_conn.send("terminal pager 0\n")

    sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)
    # print remote_conn
    return output


def addtoconfig(thebuffer, totallist):

    lines = thebuffer.split("\n")
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

    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password)
    print "SSH connection established to %s" % ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established\n"

    # Strip the initial router prompt
    # output = remote_conn.recv(1000)

    remote_conn.send("\n")

    if args.enable != "":
        remote_conn.send("enable\n")
        remote_conn.send(enable+"\n")

    # Turn off paging
    disable_paging(remote_conn,'asa')


    if collectby.lower() == 'ip':
        # Gather Tunnel Group By IP
        remote_conn.send("show running-config tunnel-group " + tunnelendpoint + "\n")
        sleep(2)    
        output = remote_conn.recv(2000)
        completeconfig = addtoconfig(output,completeconfig)

        # Determine Crypto Map Number form IP Address
        remote_conn.send("show run crypto map | i " + tunnelendpoint + "\n")
        sleep(2)
        output = remote_conn.recv(2000)
        lines = output.split("\n")
        cryptomapnumber = lines[1].split(" ")[3]
        cryptomapname = lines[1].split(" ")[2]

        # Collect all Crypto Map Configuration
        remote_conn.send("show run crypto map | i " + cryptomapname + " " + cryptomapnumber + " \n")
        sleep(2)
        output = remote_conn.recv(2000)
        completeconfig = addtoconfig(output,completeconfig)

        # Determine access-list name from Crypto Map config
        lines = output.split("\n")
        for line in lines: 
            if "match" in line:
                accesslistname = line.split(" ")
                accesslistname = accesslistname[6]
                accesslistname = accesslistname.strip()

        # Collect access-list by Name
        remote_conn.send("show run access-list " + accesslistname + " \n")
        sleep(2)
        output = remote_conn.recv(2000)
        completeconfig = addtoconfig(output,completeconfig)


    elif collectby.lower() == 'number':



        # Determine Crypto Map by Name
        remote_conn.send('show run crypto map | i interface\n')
        sleep(2)
        output = remote_conn.recv(2000)
        lines = output.split("\n")
        cryptomapname = lines[1].split(" ")[2]

        # Collect Crypto Map config
        remote_conn.send('show run crypto map | i ' + cryptomapname + " " + cryptomapnumber + ' \n')
        sleep(2)
        output = remote_conn.recv(2000)
        completeconfig = addtoconfig(output,completeconfig)

        # Determine Tunnel IP address
        lines = output.split("\n")
        for line in lines: 
            if "set peer" in line:
                tunnelendpoint = line.split(" ")
                tunnelendpoint = tunnelendpoint[6]
                tunnelendpoint = tunnelendpoint.strip()

        # Determine access-list name from Crypto Map config
        for line in lines: 
            if "match" in line:
                accesslistname = line.split(" ")
                accesslistname = accesslistname[6]
                accesslistname = accesslistname.strip()

        # Gather Tunnel Group By IP
        remote_conn.send("show running-config tunnel-group " + tunnelendpoint + "\n")
        sleep(2)    
        output = remote_conn.recv(2000)
        completeconfig = addtoconfig(output,completeconfig)

        # Collect access-list by Name
        remote_conn.send("show run access-list " + accesslistname + " \n")
        sleep(2)
        output = remote_conn.recv(2000)
        completeconfig = addtoconfig(output,completeconfig)

    else:
        exit("No correct Search type, this should not happen")


    print "\n\n The Whole thing\n"
    print "\n".join(completeconfig)

    # crypto map VPN 1 set peer 192.168.1.1



