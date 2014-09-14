#!/usr/bin/env python2.7
""" Parse Interface data from a Nexus Switch and create CSV summmary data """


import pprint
import argparse
import sys
from networkstatesystem.vendors.ssh.sshhelper import *

DEBUG = True


def initargs():
    """ initialize variables with command-line arguments """
    parser = argparse.ArgumentParser(description='input -f [file]')
    parser.add_argument('-i', '--ip', \
        help='Nexus IP address', \
        default='192.168.56.100')
    parser.add_argument('-u', '--username', \
        help='Logon Username', \
        default='admin')
    parser.add_argument('-p', '--password', \
        help='SSH/Telnet Password', \
        default='cisco')
    parser.add_argument('-e', '--enable', \
        help='Enable Password', \
        default='')
    parser.add_argument('-v', '--vdc', \
        help='Additional VDCs')
    
    arg = parser.parse_args()

    return arg

class interface(object):

    def __init__(self,ifname,vdc=1):
        self.ifname = ifname
        temp = ifname.split("Eth")[1]
        self.blade, self.portnum = temp.split("/")
        self.vdc = int(vdc)

        # Initialize None values
        self.iftype = ''
        self.speedmode = ''        
        self.speed = ''
        self.desc = ''
        self.vlan = ''
        self.mode = ''
        self.status = ''
        self.statusreason = ''
        self.portchannel = ''
        self.connectortype = ''

    def __str__(self):

        returnstring = "ifname: " + str(self.ifname) + "\n"
        returnstring += "iftype: " + str(self.iftype) + "\n"
        returnstring += "speed: " + str(self.speed) + "\n"
        returnstring += "speed mode: " + str(self.speedmode) + "\n"
        returnstring += "description: " + str(self.desc) + "\n"
        returnstring += "vlan: " + str(self.vlan) + "\n"
        returnstring += "mode: " + str(self.mode) + "\n"
        returnstring += "status: " + str(self.status) + "\n"
        returnstring += "status reason: " + str(self.statusreason) + "\n"
        returnstring += "portchannel: " + str(self.portchannel) + "\n"
        returnstring += "connectortype: " + str(self.connectortype) + "\n"
        returnstring += "vdc: " + str(self.vdc) + "\n"

        return returnstring

    def settype(self, iftype):
        self.iftype = iftype

    def setspeed(self, speed):

        if speed == '10G':
            self.speed = 10000
        elif speed == '--':
            self.speed = 0
        else:
            self.speed = int(speed)

    def setspeedmode(self, speedmode):
        # D or S
        if speedmode == 'D':
            speedmode = 'Dedicated'
        elif speedmode == 'S':
            speedmode = 'Shared'
        
        self.speedmode = speedmode

    def setdescription(self, desc):
        if desc == '--':
            self.desc = ''
        else:
            self.desc = desc

    def setvlan(self, vlan):
        try:
            self.vlan = int(vlan)
        except ValueError:
            self.vlan = 0

    def setmode(self, mode):
        self.mode = mode

    def setstatus(self, status):
        self.status = status

    def setstatusreason(self, statusreason):
        self.statusreason = statusreason

    def setportchannel(self, portchannel):
        try:
            self.portchannel = int(portchannel)
        except ValueError:
            self.portchannel = None

    def setconnectortype(self, connectortype):
        if connectortype == '10/100/1000':
            self.connectortype = 'Copper'
        elif connectortype == '--':
            self.connectortype = 'sfpAbsent'
        else:
            self.connectortype = connectortype

    def setvdc(self, vdc):
        try:
            self.vdc = int(vdc)
        except ValueError:
            print "Invalid VDC must be Integer"
            self.vdc = None        

    def returnheader(self):
        """ Return header matching items in returnlist() """

        return [ 'Blade Number', 'Port Number', 'ifName', 'Type', 'Speed', 
        'Description', 'VLAN', 'Mode', 'Status', 'Status Reason', 'Speed Mode', 
        'Port Channel', 'vdc', 'asic' ]

    def returnlist(self):
        """ Return list of all intrface values """

        return [ self.blade, self.portnum, self.ifname, self.iftype, self.speed, 
            self.desc, self.vlan, self.mode, self.status, self.statusreason, self.speedmode, 
            self.portchannel, self.connectortype, self.vdc, 'na' ]

def loadfile(filename):

    listoffilecontents = []

    with open(filename, "r") as filecontents:
        for line in filecontents:

            line = line.strip()
            if line == "":
                # if lines blank skip
                pass
            elif line[0] == "-":
                # if comment line skip
                pass
            else:
                listoffilecontents.append(line)
                # print line

    return listoffilecontents


def cleandata(filelist):
    """ Divide data delinitated by 2 spaces into columns and 
        strip leading and trailing white space.
        
        Return only interface with prefix "Eth"

        Remove Headers
    """

    filterprefix = 'Eth'
    returndata = []
    data = []

    # Split data and remove white space
    for line in filelist:
        csvline = line.split('  ')

        csvline = filter(None, csvline)

        for counter in range(len(csvline)):
            csvline[counter] = csvline[counter].strip()

        data.append(csvline)

        if DEBUG == True:
            print csvline

    # Filter rows for prefix and headers
    for line in data:
        if "Ethernet" in line[0]:
            continue
        elif filterprefix in line[0]:
            returndata.append(line)

    if DEBUG == True:
        pprint.pprint(returndata)

    return returndata


def parseshowintdesc(data, vdc=1):

    """
    Collect ifname, iftype, ifspeed, ifdescription from "show interface description" output

    Port          Type   Speed   Description
    -------------------------------------------------------------------------------
    Eth1/1        eth    1000    vPC peer keepalive link

    """

    global allinterfaces

    for line in data:
        ifname = line[0]
        iftype = line[1]
        ifspeed = line[2]
        ifdescription = line[3]

        if DEBUG == True:
            print ifname, iftype, ifspeed, ifdescription

        try:
            allinterfaces[ifname].settype(iftype)
            allinterfaces[ifname].setspeed(ifspeed)
            allinterfaces[ifname].setdescription(ifdescription)
        except KeyError:
            allinterfaces[ifname] = interface(ifname, vdc)
            allinterfaces[ifname].settype(iftype)
            allinterfaces[ifname].setspeed(ifspeed)
            allinterfaces[ifname].setdescription(ifdescription)


def parseshowbr(data, vdc=1):
    """
    Collect vlan, mode, status, statusreason, speedmode, and portchannel 
    from "show interface brief" output

    --------------------------------------------------------------------------------
    Ethernet      VLAN    Type Mode   Status  Reason                   Speed     Port
    Interface                                                                    Ch #
    --------------------------------------------------------------------------------
    Eth1/1        --      eth  routed up      none                       1000(D) 1
    Eth1/2        1       eth  trunk  up      none                       1000(D) --
    Eth1/3        30      eth  access up      none                       1000(D) --

    ['Eth2/18', '1', 'eth', 'access down', 'Administratively down', 'auto(D) --'],
    ['Eth2/19', '1', 'eth', 'trunk', 'down', 'Link not connected', 'auto(D) 32'],
    """

    global allinterfaces

    def splitmode(value):
        """ Split final column into speed mode and port channel 
            Also return only mode with out other data from Speed column
        """
        speedmode, portchannel = value.split(" ")
        speedmode = speedmode.split("(")[1][0]

        return speedmode, portchannel

    for line in data:
        ifname = line[0]
        vlan = line[1]

        if DEBUG == True:
            print line

        # Try frust to split column 3 into 2 values, if column 3 
        # only has single word follow alternate flowe
        try:
            mode, status = line[3].split(" ")
            statusreason = line[4]
            speedmode, portchannel = splitmode(line[5])
        except ValueError:
            mode = line[3]
            status = line[4] 
            statusreason = line[5]
            speedmode, portchannel = splitmode(line[6])

        if DEBUG == True:
            print vlan, mode, status, statusreason, speedmode, portchannel

        try:
            allinterfaces[ifname].setvlan(vlan)
            allinterfaces[ifname].setmode(mode)
            allinterfaces[ifname].setstatus(status)
            allinterfaces[ifname].setstatusreason(statusreason)
            allinterfaces[ifname].setspeedmode(speedmode)
            allinterfaces[ifname].setportchannel(portchannel)
        except KeyError:
            allinterfaces[ifname] = interface(ifname, vdc)
            allinterfaces[ifname].setvlan(vlan)
            allinterfaces[ifname].setmode(mode)
            allinterfaces[ifname].setstatus(status)
            allinterfaces[ifname].setstatusreason(statusreason)
            allinterfaces[ifname].setspeedmode(speedmode)
            allinterfaces[ifname].setportchannel(portchannel)


    pass

def parseshowintstat(data, vdc=1):
    """
    Collect Interface Connectory Type from "show interface status" output

    Port          Name               Status    Vlan      Duplex  Speed   Type
    --------------------------------------------------------------------------------
    Eth1/1        vPC peer keepalive connected routed    full    1000    10/100/1000

    stat: ['Eth4/12', 'Trunk_To_LMS_UCS_6 notconnec trunk', 'full', 'auto', '10Gbase-SR']
    stat: ['Eth4/13', 'DEDICATED_TO_4/9', 'sfpAbsent 1', 'full', 'auto', '--']
    stat: ['Eth4/14', '--', 'sfpAbsent 1', 'full', 'auto', '--']

    """
    global allinterfaces

    for line in data:

        ifname = line[0]

        if DEBUG == True:
            print "stat: " + str(line)

        try:
            allinterfaces[ifname].setconnectortype(line[-1])
        except KeyError:
            allinterfaces[ifname] = interface(ifname, vdc)
            allinterfaces[ifname].setconnectortype(line[-1])


allinterfaces = {}

if __name__ == '__main__':
    args = initargs()

    ip = args.ip
    username = args.username
    password = args.password
    enable = args.enable
    vdc = args.vdc

    vdclist = vdc.split(",")
    for counter in range(len(vdclist)):
        vdclist[counter] = vdclist[counter].strip()

    remote_conn_pre, remote_conn = \
    sshconnect(ip, username, password, 'ios', enable)

    descoutput = []
    briefoutput = []
    statoutput = []


    buffersize=20000
    sleeptime=5

    print "Running Command: show interface description"
    output = ssh_runcommand(remote_conn, \
        "show interface description\n", \
        recvbuffer=buffersize, \
        recvsleep=sleeptime)

    if DEBUG == True:
        print output

    descoutput.append(output)

    print "Running Command: show interface brief"
    output = ssh_runcommand(remote_conn, \
            "show interface brief\n", \
            recvbuffer=buffersize, \
            recvsleep=sleeptime)

    if DEBUG == True:
        print output

    briefoutput.append(output)

    print "Running Command: show interface status"
    output = ssh_runcommand(remote_conn, \
            "show interface status\n", \
            recvbuffer=buffersize, \
            recvsleep=sleeptime)
    
    if DEBUG == True:
        print output

    statoutput.append(output)

    # Collect Data from other VDCs 
    if vdclist != []:
        for nextvdc in vdclist:

            print "Changing to VDC {0}".format(nextvdc)
            output = ssh_runcommand(remote_conn, \
                    "switchto vdc " + nextvdc + "\n", \
                    recvbuffer=2000, \
                    recvsleep=sleeptime)

            if "Invalid command" in "\n".join(output):
                print "\n".join(output)
                sys.exit("could not change vdc")

            if DEBUG == True:
                print output

            print "Running Command: show interface description"
            output = ssh_runcommand(remote_conn, \
                "show interface description\n", \
                recvbuffer=buffersize, \
                recvsleep=sleeptime)

            if DEBUG == True:
                print output

            descoutput.append(output)

            print "Running Command: show interface brief"
            output = ssh_runcommand(remote_conn, \
                    "show interface brief\n", \
                    recvbuffer=buffersize, \
                    recvsleep=sleeptime)

            if DEBUG == True:
                print output

            briefoutput.append(output)

            print "Running Command: show interface status"
            output = ssh_runcommand(remote_conn, \
                    "show interface status\n", \
                    recvbuffer=buffersize, \
                    recvsleep=sleeptime)

            if DEBUG == True:
                print output

            statoutput.append(output)

    ##### Process Data
    # Process "show interface description" Output
    counter = 0
    for output in descoutput:
        print 'Processing "show interface description" data for VDC {0}'.format(counter+1)
        descoutput = cleandata(output)
        parseshowintdesc(descoutput, counter + 1)
        counter += 1

    # Process "show interface brief" Output
    counter = 0
    for output in briefoutput:
        print 'Processing "show interface brief" data for VDC {0}'.format(counter+1)
        briefoutput = cleandata(output)
        parseshowbr(briefoutput, counter + 1)
        counter += 1

    # Process "show interface status" Output
    counter = 0
    for output in statoutput:
        print 'Processing "show interface status" data for VDC {0}'.format(counter+1)
        statoutput = cleandata(output)
        parseshowintstat(statoutput, counter + 1)
        counter += 1

    if DEBUG == True:
        print allinterfaces[allinterfaces.keys()[0]]

    # Display Data
    print allinterfaces[allinterfaces.keys()[0]].returnheader()
    for thekey in allinterfaces.keys():
        print(allinterfaces[thekey].returnlist())




