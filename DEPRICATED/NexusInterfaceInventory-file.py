#!/usr/bin/env python
#
# Create an Inventory of all interfaces in all VDC on Nexus 7000 switches
#

from __future__ import division
import pprint

""" Parse Interface data and create CSV summmary data """
DEBUG = True

class interface(object):

    def __init__(self,ifname,vdc='1'):
        self.ifname = ifname
        temp = ifname.split("Eth")[1]
        self.blade, self.portnum = temp.split("/")
        self.vdc = vdc

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

        return [ 'Blade Number', 'Port Number', 'ifName', 'Type', 'Speed', 
        'Description', 'VLAN', 'Mode', 'Status', 'Status Reason', 'Speed Mode', 
        'Port Channel', 'vdc', 'asic' ]

    def returnlist(self):
        returnstring = [ self.blade, self.portnum, self.ifname, self.iftype, self.speed, 
            self.desc, self.vlan, self.mode, self.status, self.statusreason, self.speedmode, 
            self.portchannel, self.connectortype, self.vdc, 'na' ]

        return returnstring


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
    """ Clean data return csv of columns """

    data = []

    for line in filelist:
        csvline = line.split('  ')

        csvline = filter(None, csvline)

        for counter in range(len(csvline)):
            csvline[counter] = csvline[counter].strip()

        data.append(csvline)

        if DEBUG == True:
            print csvline


    # print data

    filterprefix = 'Eth'

    returndata = []

    for line in data:
        if "Ethernet" in line[0]:
            continue
        elif filterprefix in line[0]:
            # print line
            returndata.append(line)

    if DEBUG == True:
        pprint.pprint(returndata)

    return returndata


def printinterfacesumary(outformat=''):
    """ Display Interface Summary Information """

    numberup = 0
    numberdown = 0
    total = 0
    # status = 0

    for ifindex in sorted(allinterfaces):
        
        total += 1

        if allinterfaces[ifindex].status == 'up':
            numberup += 1
        else:
            numberdown += 1

    percentfree = int((numberdown / total) * 100)

    if outformat == 'csv':
        print [ 'up', 'down', 'percent', 'total' ]
        print [ numberup, numberdown, percentfree, total ]
    else:
        print "Total Ports up: {0}".format(numberup)
        print "Total Ports down: {0}".format(numberdown)
        print "Total Ports: {0}".format(total)
        print "Percent Free: {0} %".format(percentfree)


def parseshowintdesc(data):

    """
    Port          Type   Speed   Description
    -------------------------------------------------------------------------------
    Eth1/1        eth    1000    vPC peer keepalive link


    ifname = desc
    type = desc
    speed = desc
    desc = desc

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
            allinterfaces[ifname] = interface(ifname)
            allinterfaces[ifname].settype(iftype)
            allinterfaces[ifname].setspeed(ifspeed)
            allinterfaces[ifname].setdescription(ifdescription)


def parseshowbr(data):
    """
    vlan = brief
    mode = brief
    status = brief
    status reason = brief
    Speed mode = brief '1000(D)' the letter
    Port Channel = brief

    --------------------------------------------------------------------------------
    Ethernet      VLAN    Type Mode   Status  Reason                   Speed     Port
    Interface                                                                    Ch #
    --------------------------------------------------------------------------------
    Eth1/1        --      eth  routed up      none                       1000(D) 1
    Eth1/2        1       eth  trunk  up      none                       1000(D) --
    Eth1/3        30      eth  access up      none                       1000(D) --


    """

    global allinterfaces

    def splitmode(value):
        speedmode, portchannel = value.split(" ")
        speedmode = speedmode.split("(")[1][0]

        return speedmode, portchannel


    for line in data:

        ifname = line[0]
        vlan = line[1]

        """
        ['Eth2/18', '1', 'eth', 'access down', 'Administratively down', 'auto(D) --'],
        ['Eth2/19', '1', 'eth', 'trunk', 'down', 'Link not connected', 'auto(D) 32'],
        """

        if DEBUG == True:
            print line

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
            allinterfaces[ifname] = interface(ifname)
            allinterfaces[ifname].setvlan(vlan)
            allinterfaces[ifname].setmode(mode)
            allinterfaces[ifname].setstatus(status)
            allinterfaces[ifname].setstatusreason(statusreason)
            allinterfaces[ifname].setspeedmode(speedmode)
            allinterfaces[ifname].setportchannel(portchannel)


    pass

def parseshowintstat(data):
    """
    type = stat '-- is not present'


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
            allinterfaces[ifname] = interface(ifname)
            allinterfaces[ifname].setconnectortype(line[-1])


allinterfaces = {}

if __name__ == '__main__':

    # Test using file input
    filenamedesc = 'NexusInterfaceInventory-files/shointdesc.txt'
    filenamebr = 'NexusInterfaceInventory-files/shointbr.txt'
    filenamestat = 'NexusInterfaceInventory-files/shointstat.txt'

    dataoutput = loadfile(filenamedesc)
    dataoutput = cleandata(dataoutput)
    parseshowintdesc(dataoutput)

    dataoutput = loadfile(filenamebr)
    dataoutput = cleandata(dataoutput)
    parseshowbr(dataoutput)

    dataoutput = loadfile(filenamestat)
    dataoutput = cleandata(dataoutput)
    parseshowintstat(dataoutput)

    if DEBUG == True:
        print allinterfaces[allinterfaces.keys()[0]]

    print allinterfaces[allinterfaces.keys()[0]].returnheader()
    for thekey in allinterfaces.keys():
        print(allinterfaces[thekey].returnlist())

    printinterfacesumary()




