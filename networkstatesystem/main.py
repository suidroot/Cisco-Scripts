#!/usr/bin/env python
""" This is the main function to execute and test functions """

# system Libraries
import sys
import string
#import struct
import argparse
#import csv

# Network Libraries
from classes import *
from vendors.snmp.querydevicedata import *

def initargs():
    """ Defines the Command line Arguments """

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
    parser.add_argument('-c', '--community', help='Enter SNMP Community')
    parser.add_argument('-d', '--datasource', help='Data Source (snmp)')
    parser.add_argument('-f', '--file', help='Load Host list from File')
    parser.add_argument('-s', '--ifcount', help='Summary Interface Inventory', \
        action='store_true')
    parser.add_argument('-t', '--ifdetail', help='Detailed Interface Inventory', \
        action='store_true')
    parser.add_argument('-r', '--routedetail', help='Detailed Routing Table', \
        action='store_true')
    parser.add_argument('-a', '--allinfo', help='All Device Information', \
        action='store_true')
    parser.add_argument('-b', '--format', help='Output Format ("csv", "json", \
        or "text")')
    parser.add_argument('-o', '--output', help='Output to file')

    arg = parser.parse_args()

    hosts = []
    toggles = {}

    # Gather host information from File or Commandline
    if arg.file:
        with open(arg.file, "r") as host_list:
            for line in host_list:
                (device, community, datasource) = string.split(line, ':')
                if device[0] == "#":
                    pass
                else:
                    hosts.append([device, community.rstrip(), datasource])
    else:
        # set ip address to make calls on
        if arg.ip_address:
            device = arg.ip_address
        else:
            sys.exit("You should specify a Host")
            #device = '10.5.6.254'

        if arg.ip_address:
            community = arg.community
        else:
            sys.exit("You should specify a community")
            #community = 'poopie'
        if arg.datasource:
            datasource = arg.datasource
        else:
            datasource = 'snmp'
        hosts.append([device, community.rstrip(), datasource])

    # Parse other options
    if arg.ifcount:
        toggles['ifcount'] = True
    else:
        toggles['ifcount'] = False

    if arg.ifdetail:
        toggles['ifdetail'] = True
    else:
        toggles['ifdetail'] = False

    if arg.routedetail:
        toggles['routedetail'] = True
    else:
        toggles['routedetail'] = False

    if arg.allinfo:
        toggles['allinfo'] = True
    else:
        toggles['allinfo'] = False

    if arg.format == 'csv':
        toggles['format'] = 'csv'
    elif arg.format == 'json':
        toggles['format'] = 'json'
    elif arg.format == 'table':
        toggles['format'] = 'table'
    else:
        toggles['format'] = 'text'

    if arg.output:
        toggles['output'] = arg.output
    else:
        toggles['output'] = ""

    return hosts, toggles


if __name__ == "__main__":
##### Start Main Section ######

    host_list, toggles = initargs()

    device_detail_list = {}

    # Collect information from host_list
    for ipaddress, community, datasource in host_list:
        if toggles['format'] == 'text':
            print "Gathering SNMP Data for, {0} using the community {1}\n\n".format(ipaddress, community)

        hostname = gethostname(ipaddress, community)
        osversion = getosversion(ipaddress, community)
        interfacedata = populateifdata(ipaddress, community)
        routingdata = collectroutingtable(ipaddress, community)

        # Collect routing info
        device_detail_list[ipaddress] = device(hostname, osversion, ipaddress, \
            datasource)
        device_detail_list[ipaddress].addSNMPInterfaces(interfacedata)
        device_detail_list[ipaddress].addSNMPRoutes(routingdata)

        if toggles['ifcount'] == True:
            device_detail_list[ipaddress].printinterfacesumary(toggles['format'])
        if toggles['ifdetail'] == True:
            device_detail_list[ipaddress].printinterfacestats(toggles['format'])
        if toggles['routedetail'] == True:
            device_detail_list[ipaddress].printroutingtable(toggles['format'])
        if toggles['allinfo'] == True:
            if toggles['format'] == 'json':
                print device_detail_list[ipaddress].returnjson()
            elif toggles['format'] == 'text':
                print device_detail_list[ipaddress]

                #device_detail_list[ipaddress].printallinfo(toggles['format'])

