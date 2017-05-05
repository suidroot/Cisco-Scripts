#!/usr/bin/python3
""" This is a collection of methods to interest with a Cisco ASA """

from sys import exit
from netmiko import ConnectHandler
import ipaddress
from prettyprint import pp

ASA_CREDENTIALS = {
    'device_type': 'cisco_asa',
    'ip': '192.168.56.50',
    'username': 'cisco',
    'password': '1234567',
    'port' : 22,          # optional, defaults to 22
    'secret': '1234567',     # optional, defaults to ''
    'verbose': True       # optional, defaults to False
}

SOURCEIP = '1.1.1.1'
DESTIP = '10.0.0.10'
PROTOCOL = 'tcp'
SOURCEPORT = '2345'
DESTPORT = '23'
MYCOMMAND = "sh route"

class Device(object):
    """ Object defines base devie functions """

    def __init__(self):
        self.net_connect = None
        # pass

    def connect(self, devicedef):
        """ Setup connection to device """
        # print (devicedef)
        self.net_connect = ConnectHandler(**devicedef)

    def runcommand(self, mycommand):
        """ Run arbitrary command on device and return text output """
        runnetconnect = self.net_connect
        output = runnetconnect.send_command(mycommand)

        return output


class RoutingTable(object):
    """ This object represents the device's route table """

    def __init__(self):
        self.routingtable = []

    def setroutingtable(self, commandoutput):
        """ Parse Routing table text and create List of disctionaries """

        outputlist = commandoutput.split('\n')

        for currentline in outputlist[10:]:
            currentline = currentline.split()
            # print (currentline)

            if len(currentline) > 0:
                routetype = currentline[0]

                if routetype == 'L':
                    address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
                    interface = currentline[6]

                    current_route = {'routetype':routetype, \
                    'address_pair':address_pair, \
                    'interface': interface, \
                    'default':'no'}

                elif routetype == 'C':
                    address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
                    interface = currentline[6]

                    current_route = {'routetype':routetype, \
                    'address_pair':address_pair, \
                    'interface': interface, \
                    'default':'no'}

                elif routetype == 'S*':
                    # [u'S*', u'0.0.0.0', u'0.0.0.0', u'[1/0]', u'via', u'10.0.0.6,', u'outside']
                    address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
                    interface = currentline[6]
                    metric = currentline[3]
                    nexthop = currentline[4]
                    interface = currentline[6]

                    current_route = {'routetype':routetype, \
                    'address_pair': address_pair, \
                    'interface': interface, \
                    'default': 'yes', \
                    'metric': metric, \
                    'nexthop': nexthop}
                else:
                # [u'S', u'3.3.3.0', u'255.255.255.252', u'[1/0]', u'via', u'10.0.0.6,', u'outside']
                    address_pair = ipaddress.ip_network(currentline[1]+'/'+currentline[2])
                    interface = currentline[6]
                    metric = currentline[3]
                    nexthop = currentline[4]
                    interface = currentline[6]

                    current_route = {'routetype':routetype, \
                    'address_pair': address_pair, \
                    'interface': interface, \
                    'default': 'no', \
                    'metric': metric, \
                    'nexthop': nexthop}

                self.routingtable.append(current_route)

    def whatinterface(self, ipaddr, nondefault=False):
        """ Determine what Interface a IP address exits """

        addr4 = ipaddress.ip_address(unicode(ipaddr))
        outboundinterface = ""

        for currententry in self.routingtable:
            if currententry['default'] == 'yes':
                defaultinterface = currententry['interface']
            else:
                if addr4 in currententry['address_pair']:
                    outboundinterface = currententry['interface']

            if not nondefault:
                if outboundinterface == "":
                    outboundinterface = defaultinterface

        return outboundinterface

    def whatnexthop(self):
        pass

    def printtable(self):
        """ Print Routing Table """
        # print self.routingtable

        for line in self.routingtable:
            print line
            # pp(line)

def runpackettracer(mydevice, interface, protocol, srcip, srcport, dstip, \
dstport):
    """ Run packet tracer command and return output in disctionary format """

    import xmltodict

    phases = []

    # ciscoasa# packet-tracer input outside tcp 1.1.1.1 2 2.2.2.2 443 xml
    mycommand = "packet-tracer input " + interface + " "  + protocol + " " + \
    srcip + " " + srcport + " " + dstip + " " + dstport + " xml"

    output = mydevice.runcommand(mycommand)

    # this section is needed to work thorugh non standard XML output
    output = output.split("</Phase>")
    for line in output:
        if "Phase" in line:
            currentphase = xmltodict.parse(line + "</Phase>")['Phase']
            phases.insert(int(currentphase['id']), currentphase)
        else:
            result = xmltodict.parse(line)

    return phases, result

def addtoconfig(thebuffer, totallist):

    # lines = thebuffer.split("\n")
    lines = thebuffer
    lines = lines[1:]
    lines = lines[:-1]

    for line in lines:
        # print line
        totallist.append(line)

    return totallist

def tunnelconfigcollector(mydevice, tunnelip='', mapnumber=''):
    """ Collect all configation for a specific VPN tunnel """

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
        output = mydevice.runcommand("show running-config tunnel-group " + \
        tunnelendpoint + "\n")
        completeconfig = addtoconfig(output, completeconfig)

        # Determine Crypto Map Number form IP Address
        output = mydevice.runcommand("show run crypto map | i " + \
        tunnelendpoint + "\n")

        cryptomapnumber = output[1].split(" ")[3]
        cryptomapname = output[1].split(" ")[2]

        # Collect all Crypto Map Configuration
        output = mydevice.runcommand("show run crypto map | i " + \
        cryptomapname + " " + cryptomapnumber)

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
        output = mydevice.runcommand('show run crypto map | i ' + \
        cryptomapname + " " + cryptomapnumber)
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
        output = mydevice.runcommand("show running-config tunnel-group " + \
        tunnelendpoint)
        completeconfig = addtoconfig(output, completeconfig)

        # Collect access-list by Name
        output = mydevice.runcommand("show run access-list " + accesslistname)
        completeconfig = addtoconfig(output, completeconfig)

    else:
        exit("No correct Search type, this should not happen")

    # print "\n\n The Whole thing\n"
    print "\n".join(completeconfig)


###############################################
def main():
    """ Main Function loop """

    mydevice = Device()
    mydevice.connect(ASA_CREDENTIALS)

    print "Run command {0}".format(MYCOMMAND)
    output = mydevice.runcommand(MYCOMMAND)

    myroutingtable = RoutingTable()
    myroutingtable.setroutingtable(output)

    print "\nPrint Routing Table"
    myroutingtable.printtable()

    print "\nWhat interface does {0} exit".format(DESTIP)
    print myroutingtable.whatinterface(DESTIP)

    print "\nRunning Packet Trace"
    _, results = runpackettracer(mydevice, 'outside', PROTOCOL, SOURCEIP, \
    SOURCEPORT, DESTIP, DESTPORT)

    pp(results)


main()
