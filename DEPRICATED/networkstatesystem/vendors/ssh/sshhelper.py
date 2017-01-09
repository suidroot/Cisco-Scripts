#!/usr/bin/env python
""" This module defines helpers to connect to Network devices and execute
commands on Network devices over SSH """

import paramiko
from time import sleep

def sshconnect(sship, username, password, devtype, enable=''):
    ''' This function initates a SSH conection given an IP address, username
    Password, device take to disable pagging for terminal output.
    If the device is a Cisco device and a enable password is provided it will
    change to privileged mode. '''

    def disable_paging(remote_conn, device_type):
        ''' Disable paging on a Terminal outputs. '''

        if device_type.lower() == 'ios':
            remote_conn.send("terminal length 0\n")
        elif device_type.lower() == 'asa':
            remote_conn.send("terminal pager 0\n")
        elif device_type.lower() == 'juniper':
            remote_conn.send("set cli screen-length 0\n")
        else:
            print "disable_paging: Incorrect Device Type"

        sleep(1)
        # Clear the buffer on the screen
        output = remote_conn.recv(1000)

        return output

    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security
    # policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(sship, username=username, password=password)
    print "SSH connection established to {0}".format(sship)

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established\n"
    remote_conn.send("\n")

    if enable != "":
        remote_conn.send("enable\n")
        remote_conn.send(enable+"\n")

    # Turn off paging
    if devtype != 'none':
        disable_paging(remote_conn, devtype)

    return remote_conn_pre, remote_conn

def ssh_get_prompt(remote_conn):
    ''' Gather the Prompt by hitting enter and collecting the last line '''

    remote_conn.send("\n")

    sessionoutput = remote_conn.recv(1024)
    sessionlist = sessionoutput.split("\n")

    returnprompt = sessionlist[-1].strip()
    print returnprompt

    return returnprompt

def ssh_runcommand(remote_conn, command, prompt='', recvbuffer=30000, \
    recvsleep=10, showcommand=False):
    ''' Send command to device and return list of data '''

    # Gather Tunnel Group By IP
    if showcommand:
        print "Sending the command: {0}".format(command)

    sent = remote_conn.send(command + "\n")

    if prompt:
        sessionoutput = ''
        # igorelen = len(prompt)*8+sent
        # print igorelen
        # ignore = remote_conn.recv(igorelen)
        # print "ignore: " + ignore + "end"

        print prompt

        sessionoutpu1t = remote_conn.recv(1024)
        print "'" + sessionoutpu1t + "'"

        print "start whjile"
        while not prompt in sessionoutput:
            sessionoutput += remote_conn.recv(1024)
            # print sessionoutput
        print len(sessionoutput)
        sessionlist = sessionoutput.split("\n")
    else:
        sleep(recvsleep)
        sessionoutput = remote_conn.recv(recvbuffer)
        sessionlist = sessionoutput.split("\n") 

    return sessionlist
