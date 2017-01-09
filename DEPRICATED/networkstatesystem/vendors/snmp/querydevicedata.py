#!/usr/bin/env python
"""
This Script polls all interface statistics using the OID form the IF-MIB object
It returns the data to the screen
"""

from .querysnmpdata import snmpwalkoid
from .querysnmpdata import snmpgetoid
import string
import netaddr

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
    # oids = '1.3.6.1.2.1.4.34.1.3.1.4.'
    oids ='1.3.6.1.2.1.4.20.1.2.'
    walkreturn = snmpwalkoid(device, community, oids)

    ipaddresslist = []

    for currentrow in walkreturn:
        for indexoid, val in currentrow:
            # .1.3.6.1.2.1.4.34.1.3.1.4.127.0.0.1 = INTEGER: 1
            # collect IP address
            ipaddress = string.replace(indexoid.prettyPrint(), oids, '')
            # collect IF id
            ifindex = val.prettyPrint()
            ipaddresslist.append((ifindex,ipaddress))

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

            neighborindex = int(neighborindex)
            mibfunction = float(mibfunction)

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

            neighborindex = int(neighborindex)
            mibfunction = float(mibfunction)


            if neighborindex in lldpneighborlist:
                lldpneighborlist[neighborindex][mibfunction] = value
            else:
                lldpneighborlist[neighborindex] = {}
                lldpneighborlist[neighborindex][mibfunction] = value

    return lldpneighborlist 



def collectcdpneighbors(device, community):


    """

    http://www.oidview.com/mibs/9/CISCO-CDP-MIB.html
    cdpCacheIfIndex cdpCacheIfIndex 1.3.6.1.4.1.9.9.23.1.2.1.1.1
    cdpCacheDeviceIndex cdpCacheDeviceIndex 1.3.6.1.4.1.9.9.23.1.2.1.1.2
    cdpCacheAddressType cdpCacheAddressType 1.3.6.1.4.1.9.9.23.1.2.1.1.3
    cdpCacheAddress cdpCacheAddress 1.3.6.1.4.1.9.9.23.1.2.1.1.4
    cdpCacheVersion cdpCacheVersion 1.3.6.1.4.1.9.9.23.1.2.1.1.5
    cdpCacheDeviceId cdpCacheDeviceId   1.3.6.1.4.1.9.9.23.1.2.1.1.6
    cdpCacheDevicePort cdpCacheDevicePort   1.3.6.1.4.1.9.9.23.1.2.1.1.7
    cdpCachePlatform cdpCachePlatform   1.3.6.1.4.1.9.9.23.1.2.1.1.8
    cdpCacheCapabilities cdpCacheCapabilities   1.3.6.1.4.1.9.9.23.1.2.1.1.9
    cdpCacheVTPMgmtDomain cdpCacheVTPMgmtDomain 1.3.6.1.4.1.9.9.23.1.2.1.1.10
    cdpCacheNativeVLAN cdpCacheNativeVLAN   1.3.6.1.4.1.9.9.23.1.2.1.1.11
    cdpCacheDuplex cdpCacheDuplex   1.3.6.1.4.1.9.9.23.1.2.1.1.12
    cdpCacheApplianceID cdpCacheApplianceID 1.3.6.1.4.1.9.9.23.1.2.1.1.13
    cdpCacheVlanID cdpCacheVlanID   1.3.6.1.4.1.9.9.23.1.2.1.1.14
    cdpCachePowerConsumption cdpCachePowerConsumption   1.3.6.1.4.1.9.9.23.1.2.1.1.15
    cdpCacheMTU cdpCacheMTU 1.3.6.1.4.1.9.9.23.1.2.1.1.16
    cdpCacheSysName cdpCacheSysName 1.3.6.1.4.1.9.9.23.1.2.1.1.17
    cdpCacheSysObjectID cdpCacheSysObjectID 1.3.6.1.4.1.9.9.23.1.2.1.1.18
    cdpCachePrimaryMgmtAddrType cdpCachePrimaryMgmtAddrType 1.3.6.1.4.1.9.9.23.1.2.1.1.19
    cdpCachePrimaryMgmtAddr cdpCachePrimaryMgmtAddr 1.3.6.1.4.1.9.9.23.1.2.1.1.20
    cdpCacheSecondaryMgmtAddrType cdpCacheSecondaryMgmtAddrType 1.3.6.1.4.1.9.9.23.1.2.1.1.21
    cdpCacheSecondaryMgmtAddr cdpCacheSecondaryMgmtAddr 1.3.6.1.4.1.9.9.23.1.2.1.1.22
    cdpCachePhysLocation cdpCachePhysLocation   1.3.6.1.4.1.9.9.23.1.2.1.1.23
    cdpCacheLastChange cdpCacheLastChange   1.3.6.1.4.1.9.9.23.1.2.1.1.24

    {'1.3': {
      0: '1.3',
      '3': '1',
      '4': '192.168.1.1',
      '5': 'Vyatta Router running on Vyatta Core 6.6 R1',
      '6': 'vyatta',
      '7': 'eth1',
      '8': 'Vyatta',
      '9': '0x00000011',
      '11': '0',
      '12': '1',},

    """

    cdpneighborlist = {}

    oids = '1.3.6.1.4.1.9.9.23.1.2.1.1.'
    walkreturn = snmpwalkoid(device, community, oids)

    for currentrow in walkreturn:
        for indexoid, val in currentrow:
            value = val.prettyPrint()
            remainingoid = string.replace(indexoid.prettyPrint(), oids, '')
            # print remainingoid
            (mibfunction, neighborindex1, neighborindex2) = string.split(remainingoid, '.')

            neighborindex = int(neighborindex1 + neighborindex2)

            mibfunction = int(mibfunction)

            if mibfunction == 4:
                # Convery HEX formated IP into ASCII

                value = str(netaddr.IPAddress(value))

                # oct1 = value[2] + value[3]
                # oct2 = value[4] + value[5]
                # oct3 = value[6] + value[7]
                # oct4 = value[8] + value[9]

                # oct1 = str(int(oct1,16))
                # oct2 = str(int(oct2,16))
                # oct3 = str(int(oct3,16))
                # oct4 = str(int(oct4,16))

                # value = oct1 + "." + oct2 + "." + oct3 + "." + oct4

            elif mibfunction == 5:
                # Convert Hex return into plain text

                if value[0]+value[1] == '0x':
                    # print value
                    value = value[2:].decode('hex')
            else:
                # Convert numeric values into integers, else leave as is
                # NOTE: Could be a problem if a float is encounterd
                try:
                    value = int(value)
                except ValueError:
                    pass

            if neighborindex in cdpneighborlist:
                cdpneighborlist[neighborindex][mibfunction] = value
            else:
                cdpneighborlist[neighborindex] = {}
                cdpneighborlist[neighborindex][0] = neighborindex
                cdpneighborlist[neighborindex][mibfunction] = value

    # normalize data


    return cdpneighborlist 

def collectroutingtable(device, community):
    """ Collect Routing Table """

    nexthoplist = []

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

            if value not in nexthoplist:
                nexthoplist.append(value)

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
