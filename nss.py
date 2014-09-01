#!/usr/bin/env python
""" This is the main function to execute and test functions """

# system Libraries
import sys
import string
import argparse
import ipaddress
from socket import gethostbyname

# Network Libraries
from networkstatesystem.classes import *
from networkstatesystem.vendors.snmp.querydevicedata import *

__author__ = "Ben Mason"
__copyright__ = "Copyright 2014"
__version__ = "1.0.0"
__email__ = "su1droot@gmail.com"
__status__ = "Development"

def collectargs():
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

    return arg

def createhostlist(arg):
    """ Create hosst list from either file for Commandline """

    hosts = []

    # Gather host information from File or Commandline
    if arg.file:
        with open(arg.file, "r") as host_list:
            for line in host_list:
                line = line.strip()
                if line == "":
                    # if lines blank skip
                    pass
                elif line[0] == "#":
                    # if comment line skip
                    pass
                else:
                    (device, community, datasource) = string.split(line, ':')
                    try:
                        device = gethostbyname(device)
                    except:
                        errormsg = "Invalid hostname in config file: " + str(device)
                        sys.exit(errormsg)

                    if ipaddress.ip_address(device):
                        hosts.append([device, community.rstrip(), datasource])
                    else:
                        errormsg = "Invalid IP Address in config file: " + str(device)
                        sys.exit(errormsg)

    else:
        # set ip address to make calls on
        if arg.ip_address:
            try:
                device = gethostbyname(arg.ip_address)
            except:
                errormsg = "Invalid hostname: " + str(arg.ip_address)
                sys.exit(errormsg)

            if ipaddress.ip_address(device):
                pass
            else:
                errormsg = "Invalid IP Address: " + str(device)
                sys.exit(errormsg)
        else:
            sys.exit("You should specify a Host")

        if arg.ip_address:
            community = arg.community
        else:
            sys.exit("You should specify a community")

        if arg.datasource:
            datasource = arg.datasource
        else:
            datasource = 'snmp'

        hosts.append([device, community.rstrip(), datasource])

    return hosts

def optionoptions(arg):
    """ Set output parameters """

    toggles = {}

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

    return toggles


if __name__ == "__main__":
##### Start Main Section ######

    args = collectargs()
    host_list = createhostlist(args)
    toggles = optionoptions(args)

    device_detail_list = {}

    # Collect information from host_list
    for dev_ipaddress, community, datasource in host_list:
        if toggles['format'] == 'text':
            print "Gathering SNMP Data for {0} using the community {1}\n".format(dev_ipaddress, community)

        hostname = gethostname(dev_ipaddress, community)
        osversion = getosversion(dev_ipaddress, community)
        interfacedata = populateifdata(dev_ipaddress, community)
        routingdata = collectroutingtable(dev_ipaddress, community)

        # Collect routing info
        device_detail_list[dev_ipaddress] = device(hostname, osversion, dev_ipaddress, \
            datasource)
        device_detail_list[dev_ipaddress].addSNMPInterfaces(interfacedata)
        device_detail_list[dev_ipaddress].addSNMPRoutes(routingdata)
        device_detail_list[dev_ipaddress].ipaddresses = \
            collectipaddresses(dev_ipaddress, community)
        device_detail_list[dev_ipaddress].neighborinformation = \
            collectlldpneighbors(dev_ipaddress, community)

        if toggles['ifcount'] == True:
            device_detail_list[dev_ipaddress].printinterfacesumary(toggles['format'])
        if toggles['ifdetail'] == True:
            device_detail_list[dev_ipaddress].printinterfacestats(toggles['format'])
        if toggles['routedetail'] == True:
            device_detail_list[dev_ipaddress].printroutingtable(toggles['format'])
        if toggles['allinfo'] == True:
            if toggles['format'] == 'json':
                print device_detail_list[dev_ipaddress].returnjson()
            elif toggles['format'] == 'text':
                print device_detail_list[dev_ipaddress]

                #device_detail_list[dev_ipaddress].printallinfo(toggles['format'])

