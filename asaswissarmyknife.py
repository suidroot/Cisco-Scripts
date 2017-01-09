#!/usr/bin/python3

from netmiko import ConnectHandler
import ipaddress
from sys import exit

ASA_CREDENTIALS = {
    'device_type': 'cisco_asa',
    'ip': '172.16.1.54',
    'username': 'cisco',
    'password': 'cisco',
    'port' : 22,          # optional, defaults to 22
    'secret': 'cisco',     # optional, defaults to ''
    'verbose': False       # optional, defaults to False
}

class device(object):
	def __init__(self):
		# self.net_connect = ""
		pass

	def connect(self, devicedef):
		print (devicedef)
		self.net_connect = ConnectHandler(**devicedef)

	def runcommand(self, mycommand):
		runnetconnect = self.net_connect

		output = runnetconnect.send_command(mycommand)
		return output


class routing_table(object):
	def __init__(self):
		self.routingtable = []

	def setroutingtable(self, commandoutput):

		outputlist = commandoutput.split('\n')

		for currentline in outputlist[10:]:
			currentline = currentline.split()
			print (currentline)

			if len(currentline) > 0:
				routetype = currentline[0]

				if routetype == 'L':
					address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
					interface = currentline[6]
					current_route = {'routetype':routetype, 'address_pair':address_pair, 'interface': interface, 'default':'no'}

				elif routetype == 'C':
					address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
					interface = currentline[6]
					current_route = {'routetype':routetype, 'address_pair':address_pair, 'interface': interface, 'default':'no'}

				elif routetype == 'S*':
					# [u'S*', u'0.0.0.0', u'0.0.0.0', u'[1/0]', u'via', u'10.0.0.6,', u'outside']
					address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
					interface = currentline[6]
					metric = currentline[3]
					nexthop = currentline[4]
					interface = currentline[6]
					current_route = {'routetype':routetype, 'address_pair':address_pair, 'interface': interface, 'default':'yes'}
				else:
				#	[u'S', u'3.3.3.0', u'255.255.255.252', u'[1/0]', u'via', u'10.0.0.6,', u'outside']				
					address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
					interface = currentline[6]
					metric = currentline[3]
					nexthop = currentline[4]
					interface = currentline[6]
					current_route = {'routetype':routetype, 'address_pair':address_pair, 'interface': interface, 'default':'no'}

				self.routingtable.append(current_route) 

	def whatinterface(self, ipaddr):

		addr4 = ipaddress.ip_address(ipaddr)

		for currententry in self.routingtable:
			if addr4 in currententry['address_pair']:
				print (currententry['interface'])
				print (currententry)

	def whatnexthop():
		pass;

	def printtable(self):
		print (self.routingtable)



def runpackettracer(interface, protocol, srcip, srcport, dstip, dstport):
	import xmltodict

	# ciscoasa# packet-tracer input outside tcp 1.1.1.1 2 2.2.2.2 443 xml
	mycommand = "packet-tracer input " + interface + " "  + protocol + " " + srcip + " " + srcport + " " + dstip + " " + dstport + " xml"

	output = mydevice.runcommand(mycommand)
	output = output.replace("\n","")
	print (output)
	print (xmltodict.parse(output))



def tunnelconfigcollector(tunnelip='', mapnumber=''):
	# 
	# Collect all configation for a specific VPN tunnel
	#

	def addtoconfig(thebuffer, totallist):

	    # lines = thebuffer.split("\n")
	    lines = thebuffer
	    lines = lines[1:]
	    lines = lines[:-1]

	    for line in lines:
	        # print line
	        totallist.append(line)

	    return totallist


    completeconfig = []

    if tunnelip != '':
        tunnelendpoint = tunnelip
        collectby = 'ip'
    elif mapnumber != '':
        cryptomapnumber = mapnumber
        collectby = 'number'
    else:
        exit("Specify a Search Parameter -t or -m")

    if collectby.lower() == 'ip':
        # Gather Tunnel Group By IP

        output = mydevice.runcommand("show running-config tunnel-group " + tunnelendpoint + "\n")
        completeconfig = addtoconfig(output, completeconfig)

        # Determine Crypto Map Number form IP Address
        output = mydevice.runcommand("show run crypto map | i " + tunnelendpoint + "\n")

        cryptomapnumber = output[1].split(" ")[3]
        cryptomapname = output[1].split(" ")[2]

        # Collect all Crypto Map Configuration
        output = mydevice.runcommand("show run crypto map | i " + cryptomapname + " " + \
            cryptomapnumber)

        completeconfig = addtoconfig(output, completeconfig)
        # Determine access-list name from Crypto Map config

        for line in output: 
            if "match" in line:
                accesslistname = line.split(" ")
                accesslistname = accesslistname[6]
                accesslistname = accesslistname.strip()

        # Collect access-list by Name
        output = mydevice.runcommand("show run access-list " + accesslistname)
        completeconfig = addtoconfig(output, completeconfig)


    elif collectby.lower() == 'number':
        # Determine Crypto Map by Name
        output = mydevice.runcommand('show run crypto map | i interface\n')
        cryptomapname = output[1].split(" ")[2]

        # Collect Crypto Map config
        output = mydevice.runcommand('show run crypto map | i ' + cryptomapname + " " + \
            cryptomapnumber)
        completeconfig = addtoconfig(output, completeconfig)

        # Determine Tunnel IP address
        for line in output: 
            if "set peer" in line:
                tunnelendpoint = line.split(" ")
                tunnelendpoint = tunnelendpoint[6]
                tunnelendpoint = tunnelendpoint.strip()

        # Determine access-list name from Crypto Map config
        for line in output: 
            if "match" in line:
                accesslistname = line.split(" ")
                accesslistname = accesslistname[6]
                accesslistname = accesslistname.strip()

        # Gather Tunnel Group By IP
        output = mydevice.runcommand("show running-config tunnel-group " + tunnelendpoint)
        completeconfig = addtoconfig(output, completeconfig)

        # Collect access-list by Name
        output = mydevice.runcommand("show run access-list " + accesslistname)
        completeconfig = addtoconfig(output, completeconfig)

    else:
        exit("No correct Search type, this should not happen")

    # print "\n\n The Whole thing\n"
    print ("\n".join(completeconfig))


###############################################

# print(output)

mydevice = device()
mydevice.connect(ASA_CREDENTIALS)

mycommand = "sh route"
output = mydevice.runcommand(mycommand)
myroutingtable = routing_table()
myroutingtable.setroutingtable(output)
myroutingtable.printtable()
myroutingtable.whatinterface('10.0.0.7')

runpackettracer('outside', 'tcp', '1.1.1.1', '2345', '2.2.2.2', '23')

