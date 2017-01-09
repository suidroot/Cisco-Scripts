#!/usr/bin/env python
"""
Functions to interface with SNMP library and return data as a 
dictionary or single element
"""

from pysnmp.entity.rfc3413.oneliner import cmdgen

def snmpwalkoid(device, community, oids):
    """ This Walks more then one SNMP OID returns dictionary 
    of a list of OIDs """

    snmpcmdgen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBindTable = snmpcmdgen.nextCmd(
        # securityIndex is a dumby value does nothing
        cmdgen.CommunityData('securityIndex', community, mpModel=1),
        cmdgen.UdpTransportTarget((device, 161)),
        oids)

    if errorIndication:
        print errorIndication
    else:
        if errorStatus:
            print '%s at %s' % (errorStatus.prettyPrint(), \
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?')
        else:
            return varBindTable

def snmpgetoid(device, community, oids):
    """ This function queries the device for a given ip, community and single 
    OID. intented to return one OID ad value """

    snmpcmdgen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBindTable = snmpcmdgen.getCmd(
        # securityIndex is a dumby value does nothing
        cmdgen.CommunityData('securityIndex', community, mpModel=1),
        cmdgen.UdpTransportTarget((device, 161)), oids)

    if errorIndication:
        print errorIndication
    else:
        if errorStatus:
            print '%s at %s' % (errorStatus.prettyPrint(), \
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?')
        else:
            return varBindTable[0]

