#!/usr/bin/env python

# system Libraries
import sys
import string
import struct
import argparse
import csv

# Network Libraries
from classes import *
from vendors.snmp.querygeneraldata import *
from vendors.snmp.interfacedump import *
from vendors.snmp.routingdump import *


def initArgs():

	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
	parser.add_argument('-c', '--community', help='Enter SNMP Community')
	parser.add_argument('-f', '--file', help='Load Host list from File')
	parser.add_argument('-s', '--ifcount', help='Summary Interface Inventory', action='store_true')
	parser.add_argument('-a', '--detail', help='Detailed Interface Inventory', action='store_true')
	parser.add_argument('-b', '--csv', help='CSV Format', action='store_true')
	parser.add_argument('-o', '--output', help='Output to file')

	arg = parser.parse_args()

	hosts = []

	# Gather host information from File or Commandline
	if arg.file:
		with open(arg.file, "r") as host_list:
			for line in host_list:
				(device, community) = string.split(line,':')
				if device[0] == "#":
					pass
				else:
					hosts.append([device, community.rstrip()])
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
		
#		hosts = [device, community]
		hosts.append([device, community.rstrip()])


	# Parse other options
	if arg.ifcount:
		ifcount = True
	else: 
		ifcount = False
		
	if arg.detail:
		detail = True
	else:
		detail = False
	
	if arg.csv:
		format = 'csv'
	else:
		format = 'text'

	if arg.output:
		outputfile = arg.output
	else:
		outputfile = ""

	return hosts, ifcount, detail, format, outputfile


if __name__ == "__main__":
##### Start Main Section ######

	host_list = []
	host_list, ifcount, detail, format, outputfile = initArgs()

	device_detail_list = {}
	
	# Collect information from host_list
	for ipaddress, community in host_list:

		if format == 'text':
			print "Gathering SNMP Data for, %s using the community %s" % (ipaddress, community)


		hostname = hostinfo(ipaddress, community)
		interfacedata = populateifdata(ipaddress, community)
		routingdata = collectroutingtable(ipaddress, community)
		# Collect routing info

		device_detail_list[ipaddress] = device(hostname, ipaddress, 'snmp', routingdata, interfacedata)

		"""print device_detail_list[ipaddress].hostname
		print device_detail_list[ipaddress].ipaddress
		print device_detail_list[ipaddress].datasource
		print device_detail_list[ipaddress].routingtable
		print device_detail_list[ipaddress].interfacetable"""

		device_detail_list[ipaddress].printinfo()



		"""if ifcount == True:
			printinterfacesumary(interfacedata, format, hostname)
		if detail == True:
			printinterfacestats(interfacedata, format, hostname)"""

