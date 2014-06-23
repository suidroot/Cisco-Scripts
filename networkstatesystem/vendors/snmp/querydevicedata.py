#!/usr/bin/env python
"""
This Script polls all interface statistics using the OID form the IF-MIB object
It returns the data to the screen
"""

from .querysnmpdata import snmpwalkoid
from .querysnmpdata import snmpgetoid
import string

# This function retrieves the available interface data
def populateifdata(device, community):
    """ Collect Information statistics """
    oids = '1.3.6.1.2.1.2.2.1'
    indextable = {}

    walkreturn = snmpwalkoid(device, community, oids)

    for currentrow in walkreturn:
        for indexoid, val in currentrow:
            replaced = string.replace(indexoid.prettyPrint(), oids, '')[1::]
            value = val.prettyPrint()

            (oidnumber, ifindex) = string.split(replaced, '.')
            ifindex = int(ifindex)
            oidnumber = int(oidnumber)

            if ifindex in indextable:
                indextable[ifindex][oidnumber] = value
            else:
                indextable[ifindex] = {}
                indextable[ifindex][oidnumber] = value

    return indextable

def collectipaddresses(device, community):
    """ Collects list of IP addresses from the device """
    oids = '1.3.6.1.2.1.4.34.1.3.1.4.'
    walkreturn = snmpwalkoid(device, community, oids)

    ipaddresslist = []

    for currentrow in walkreturn:
        for indexoid, val in currentrow:
            # .1.3.6.1.2.1.4.34.1.3.1.4.127.0.0.1 = INTEGER: 1
            # collect IP address
            ipaddress = string.replace(indexoid.prettyPrint(), oids, '')
            # collect IF id
            #ifindex = val.prettyPrint()
            ipaddresslist.append(ipaddress)

            # some stuff here
    return ipaddresslist


def collectlldpneighbors(device, community):

    """
    nei {
        neighborid {
            ifindex 0
            lldpRemChassisIdSubtype 4
            lldpRemChassisId 5
            lldpRemPortIdSubtype 6
            lldpRemPortId 7
            lldpRemPortDesc 8
            lldpRemSysName 9
            lldpRemSysDesc 10
            lldpRemSysCapSupported 11
            lldpRemSysCapEnabled 12
            lldpRemManAddrIfSubtype 3
            lldpRemManAddrIfId 4
            lldpRemManAddrOID 5
    """

    lldpneighborlist = {}

    # collect lldpRemTable
    oids = '1.0.8802.1.1.2.1.4.1.1.'
    walkreturn = snmpwalkoid(device, community, oids)

    for currentrow in walkreturn:
        for indexoid, val in currentrow:
            value = val.prettyPrint()
            remainingoid = string.replace(indexoid.prettyPrint(), oids, '')
            # 4.85400.2.1
            print remainingoid
            (mibfunction, neighborindex, ifindex, null) = string.split(remainingoid, '.')
            mibfunction =+ ".1"
            # oid 10 in hex not ascii

            if neighborindex in lldpneighborlist:
                lldpneighborlist[neighborindex][mibfunction] = value
            else:
                lldpneighborlist[neighborindex] = {}
                lldpneighborlist[neighborindex][0] = ifindex
                lldpneighborlist[neighborindex][mibfunction] = value

    oids = '1.0.8802.1.1.2.1.4.2.1.'
    walkreturn = snmpwalkoid(device, community, oids)

    for currentrow in walkreturn:
        for indexoid, val in currentrow:
            value = val.prettyPrint()
            remainingoid = string.replace(indexoid.prettyPrint(), oids, '')
            # 5.85400.2.1.1.4.192.168.56.50

            (mibfunction, neighborindex, ifindex, null) = string.split(remainingoid, '.', 4)
            mibfunction =+ ".2"
            print null

            if neighborindex in lldpneighborlist:
                lldpneighborlist[neighborindex][mibfunction] = value
            else:
                lldpneighborlist[neighborindex] = {}
                lldpneighborlist[neighborindex][mibfunction] = value

    return lldpneighborlist 

def collectroutingtable(device, community):
    """ Collect Routing Table """

    oids = '1.3.6.1.2.1.4.24.4.1.'
    walkreturn = snmpwalkoid(device, community, oids)

    # oid example 1.3.6.1.2.1.4.24.4.1.24.4.1.1.10.5.6.0.255.255.255.0.0.0.0.0.0
    indextable = {}

    for currentrow in walkreturn:
        for indexoid, val in currentrow:
            replaced = string.replace(indexoid.prettyPrint(), oids, '')
            value = val.prettyPrint()

            (oidnumber, routeindex) = string.split(replaced, '.', 1)
            oidnumber = int(oidnumber)

            if routeindex in indextable:
                indextable[routeindex][oidnumber] = value
            else:
                indextable[routeindex] = {}
                indextable[routeindex][oidnumber] = value
    return indextable

def gethostname(device, community):
    """ Collect Hostname of device """

    sysname = '.1.3.6.1.2.1.1.5.0'
    oid, hostreturn = snmpgetoid(device, community, sysname)

    return hostreturn.prettyPrint()

def getosversion(device, community):
    """ Collect OS Information form device """

    #osversion = '.1.3.6.1.2.1.25.6.3.1.2.2'
    osversion = '.1.3.6.1.2.1.1.1.0'
    oid, versionreturn = snmpgetoid(device, community, osversion)

    return versionreturn.prettyPrint()
