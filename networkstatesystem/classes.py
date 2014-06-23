"""
This Module conatins all of the information defining Network elements
"""

import json
import prettytable

class device_interface(object):
    """ This defines the information that defines an device interface """

    _ifIndex = 0
    _ifDescr = ""
    _ifType = ""
    _ifMtu = 0
    _ifSpeed = 0
    _ifPhysAddress = "na"
    _ifAdminStatus = 0
    _ifOperStatus = 0
    _ifLastChange = 0
    _ifInOctets = 0
    _ifUcastPkts = 0
    _ifInNUcastPkts = 0
    _ifInDiscards = 0
    _ifInErrors = 0
    _ifInUnknownProtos = 0
    _ifOutOctets = 0
    _ifOutUcastPkts = 0
    _ifOutNUcastPkts = 0
    _ifOutDiscards = 0
    _ifOutErrors = 0
    _ifOutQLen = 0
    _ifSpecific = 0

    def __init__(self, ifIndex, ifDescr, ifType, ifMtu, ifSpeed, \
        ifPhysAddress, ifAdminStatus, ifOperStatus, ifLastChange, ifInOctets, \
        ifUcastPkts, ifInNUcastPkts, ifInDiscards, ifInErrors, \
        ifInUnknownProtos, ifOutOctets, ifOutUcastPkts, ifOutNUcastPkts, \
        ifOutDiscards, ifOutErrors, ifOutQLen, ifSpecific):

        self._ifIndex = ifIndex
        self._ifDescr = ifDescr
        self._ifType = ifType
        self._ifMtu = ifMtu
        self._ifSpeed = ifSpeed
        self._ifPhysAddress = ifPhysAddress
        self._ifAdminStatus = ifAdminStatus
        self._ifOperStatus = ifOperStatus
        self._ifLastChange = ifLastChange
        self._ifInOctets = ifInOctets
        self._ifUcastPkts = ifUcastPkts
        self._ifInNUcastPkts = ifInNUcastPkts
        self._ifInDiscards = ifInDiscards
        self._ifInErrors = ifInErrors
        self._ifInUnknownProtos = ifInUnknownProtos
        self._ifOutOctets = ifOutOctets
        self._ifOutUcastPkts = ifOutUcastPkts
        self._ifOutNUcastPkts = ifOutNUcastPkts
        self._ifOutDiscards = ifOutDiscards
        self._ifOutErrors = ifOutErrors
        self._ifOutQLen = ifOutQLen
        self._ifSpecific = ifSpecific

    def __repr__(self):

        ifstatus = {
            1: "up",
            2: "down",
            3: "testing",
            4: "unknown",
            5: "dormant",
            6: "notPresent",
            7: "lowerLayerDown"
        }

        return_string = "\n"
        return_string += "ifIndex {0}\n".format(self._ifIndex)
        return_string += "ifDescr {0}\n".format(self._ifDescr)
        return_string += "ifType {0}\n".format(self._ifType)
        return_string += "ifMtu {0}\n".format(self._ifMtu)
        return_string += "ifSpeed {0}\n".format(self._ifSpeed)
        return_string += "ifPhysAddress {0}\n".format(self._ifPhysAddress)
        return_string += "ifAdminStatus {0}\n".format(ifstatus[int(self._ifAdminStatus)])
        return_string += "ifOperStatus {0}\n".format(ifstatus[int(self._ifOperStatus)])
        return_string += "ifLastChange {0}\n".format(self._ifLastChange)
        return_string += "ifInOctets {0}\n".format(self._ifInOctets)
        return_string += "ifUcastPkts {0}\n".format(self._ifUcastPkts)
        return_string += "ifInNUcastPkts {0}\n".format(self._ifInNUcastPkts)
        return_string += "ifInDiscards {0}\n".format(self._ifInDiscards)
        return_string += "ifInErrors {0}\n".format(self._ifInErrors)
        return_string += "ifInUnknownProtos {0}\n".format(self._ifInUnknownProtos)
        return_string += "ifOutOctets {0}\n".format(self._ifOutOctets)
        return_string += "ifOutUcastPkts {0}\n".format(self._ifOutUcastPkts)
        return_string += "ifOutNUcastPkts {0}\n".format(self._ifOutNUcastPkts)
        return_string += "ifOutDiscards {0}\n".format(self._ifOutDiscards)
        return_string += "ifOutErrors {0}\n".format(self._ifOutErrors)
        return_string += "ifOutQLen {0}\n".format(self._ifOutQLen)
        return_string += "ifSpecific {0}\n".format(self._ifSpecific)

        return return_string

    def dictrepr(self):
        """ Represent the information in dictionary format """

        return_dict = {}

        return_dict[1] = self._ifIndex
        return_dict[2] = self._ifDescr
        return_dict[3] = self._ifType
        return_dict[4] = self._ifMtu
        return_dict[5] = self._ifSpeed
        return_dict[6] = self._ifPhysAddress
        return_dict[7] = self._ifAdminStatus
        return_dict[8] = self._ifOperStatus
        return_dict[9] = self._ifLastChange
        return_dict[10] = self._ifInOctets
        return_dict[11] = self._ifUcastPkts
        return_dict[12] = self._ifInNUcastPkts
        return_dict[13] = self._ifInDiscards
        return_dict[14] = self._ifInErrors
        return_dict[15] = self._ifInUnknownProtos
        return_dict[16] = self._ifOutOctets
        return_dict[17] = self._ifOutUcastPkts
        return_dict[18] = self._ifOutNUcastPkts
        return_dict[19] = self._ifOutDiscards
        return_dict[20] = self._ifOutErrors
        return_dict[21] = self._ifOutQLen
        return_dict[22] = self._ifSpecific

        return return_dict

class device_routingtable(object):
    """ Define a route entry """

    _ipCidrRouteDest = ""
    _ipCidrRouteNextHopAS = ""
    _ipCidrRouteMetric1 = 0
    _ipCidrRouteMetric2 = 0
    _ipCidrRouteMetric3 = 0
    _ipCidrRouteMetric4 = 0
    _ipCidrRouteMetric5 = 0
    _ipCidrRouteStatus = 0
    _ipCidrRouteMask = ""
    _ipCidrRouteTos = 0
    _ipCidrRouteNextHop = ""
    _ipCidrRouteIfIndex = 0
    _ipCidrRouteType = 0
    _ipCidrRouteProto = 0
    _ipCidrRouteAge = 0
    _ipCidrRouteInf = 0

    def __init__(self, ipCidrRouteDest, ipCidrRouteNextHopAS, \
        ipCidrRouteMetric1, ipCidrRouteMetric2, ipCidrRouteMetric3, \
        ipCidrRouteMetric4, ipCidrRouteMetric5, ipCidrRouteStatus, \
        ipCidrRouteMask, ipCidrRouteTos, ipCidrRouteNextHop, \
        ipCidrRouteIfIndex, ipCidrRouteType, ipCidrRouteProto, ipCidrRouteAge, \
        ipCidrRouteInf):

        self._ipCidrRouteAge = ipCidrRouteAge
        self._ipCidrRouteDest = ipCidrRouteDest
        self._ipCidrRouteIfIndex = ipCidrRouteIfIndex
        self._ipCidrRouteInf = ipCidrRouteInf
        self._ipCidrRouteMask = ipCidrRouteMask
        self._ipCidrRouteMetric1 = ipCidrRouteMetric1
        self._ipCidrRouteMetric2 = ipCidrRouteMetric2
        self._ipCidrRouteMetric3 = ipCidrRouteMetric3
        self._ipCidrRouteMetric4 = ipCidrRouteMetric4
        self._ipCidrRouteMetric5 = ipCidrRouteMetric5
        self._ipCidrRouteNextHop = ipCidrRouteNextHop
        self._ipCidrRouteNextHopAS = ipCidrRouteNextHopAS
        self._ipCidrRouteProto = ipCidrRouteProto
        self._ipCidrRouteStatus = ipCidrRouteStatus
        self._ipCidrRouteTos = ipCidrRouteTos
        self._ipCidrRouteType = ipCidrRouteType

    def __repr__(self):

        return_string = "\n"
        return_string += "Dest: {0} ".format(self._ipCidrRouteDest)
        return_string += "Mask: {0} ".format(self._ipCidrRouteMask)
        return_string += "Next Hop: {0}\n".format(self._ipCidrRouteNextHop)
        return_string += "Proto: {0} ".format(self._ipCidrRouteProto)
        return_string += "Type: {0} ".format(self._ipCidrRouteType)
        return_string += "Inf: {0} ".format(self._ipCidrRouteInf)
        return_string += "Age: {0} ".format(self._ipCidrRouteAge)
        return_string += "Next Hop AS: {0} ".format(self._ipCidrRouteNextHopAS)
        return_string += "TOS: {0} ".format(self._ipCidrRouteTos)
        return_string += "Status: {0} ".format(self._ipCidrRouteStatus)
        return_string += "ifIndex: {0}\n".format(self._ipCidrRouteIfIndex)
        return_string += "Metric 1: {0} ".format(self._ipCidrRouteMetric1)
        return_string += "Metric 2: {0} ".format(self._ipCidrRouteMetric2)
        return_string += "Metric 3: {0} ".format(self._ipCidrRouteMetric3)
        return_string += "Metric 4: {0} ".format(self._ipCidrRouteMetric4)
        return_string += "Metric 5: {0}\n".format(self._ipCidrRouteMetric5)

        return return_string


# Generic Device Class
# This is the parent to all of the sub element information
class device(object):
    """ Definitaion of a device and contained information """
    _hostname = ""
    _osversion = ""
    _primaryipaddress = ""
    _datasource = ""
    interfacetable = {}
    ipaddresses = []
    neighborinformation = {}
    routingtable = {}


    def __init__(self, hostname, osversion, ipaddress, datasource):
        #super(device, self).__init__()
        self._hostname = hostname
        self._osversion = osversion
        self._primaryipaddress = ipaddress
        self._datasource = datasource
        #self.routingtable = routingtable
        #self.interfacetable = interfacetable

    def __str__(self):

        #outformat = 'table'
        return_string = "Hostname: {0}\n".format(self._hostname)
        return_string += "Version: {0}\n".format(self._osversion)
        return_string += "Primary IP Address: {0}\n".format(self._primaryipaddress)
        return_string += "IP Addresses: "
        for address in self.ipaddresses:
            return_string += "{0} ".format(address)
        return_string += "\n"
        return_string += "Data Source: {0}\n".format(self._datasource)
        return_string += "\nInterface Information\n"
        return_string += str(self.interfacetable)
        return_string += "\nRouting Information\n"
        return_string += str(self.routingtable)

        return return_string

    def addSNMPInterfaces(self, interfacetable):
        """ add a new interface """

        ifIndex = 0
        ifDescr = ""
        ifType = ""
        ifMtu = 0
        ifSpeed = 0
        ifPhysAddress = ""
        ifAdminStatus = 0
        ifOperStatus = 0
        ifLastChange = 0
        ifInOctets = 0
        ifUcastPkts = 0
        ifInNUcastPkts = 0
        ifInDiscards = 0
        ifInErrors = 0
        ifInUnknownProtos = 0
        ifOutOctets = 0
        ifOutUcastPkts = 0
        ifOutNUcastPkts = 0
        ifOutDiscards = 0
        ifOutErrors = 0
        ifOutQLen = 0

        for loop_ifIndex in interfacetable:
            for ifAttr in interfacetable[loop_ifIndex]:
                if ifAttr == 1:
                    ifIndex = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 2:
                    ifDescr = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 3:
                    ifType = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 4:
                    ifMtu = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 5:
                    ifSpeed = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 6:
                    ifPhysAddress = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 7:
                    ifAdminStatus = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 8:
                    ifOperStatus = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 9:
                    ifLastChange = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 10:
                    ifInOctets = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 11:
                    ifUcastPkts = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 12:
                    ifInNUcastPkt = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 13:
                    ifInDiscard = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 14:
                    ifInErrors = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 15:
                    ifInUnknownProtos = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 16:
                    ifOutOctets = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 17:
                    ifOutUcastPkts = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 18:
                    ifOutNUcastPkt = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 19:
                    ifOutDiscard = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 20:
                    ifOutError = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 21:
                    ifOutQLen = interfacetable[loop_ifIndex][ifAttr]
                elif ifAttr == 22:
                    ifSpecific = interfacetable[loop_ifIndex][ifAttr]

            self.interfacetable[loop_ifIndex] = device_interface(ifIndex, \
                ifDescr, ifType, ifMtu, ifSpeed, ifPhysAddress, ifAdminStatus, \
                ifOperStatus, ifLastChange, ifInOctets, ifUcastPkts, \
                ifInNUcastPkts, ifInDiscards, ifInErrors, ifInUnknownProtos, \
                ifOutOctets, ifOutUcastPkts, ifOutNUcastPkts, ifOutDiscards, \
                ifOutErrors, ifOutQLen, ifSpecific)

    def addSNMPRoutes(self, routingtable):
        """ Add a new Route """

        ipCidrRouteDest = ""
        ipCidrRouteNextHopAS = ""
        ipCidrRouteMetric1 = 0
        ipCidrRouteMetric2 = 0
        ipCidrRouteMetric3 = 0
        ipCidrRouteMetric4 = 0
        ipCidrRouteMetric5 = 0
        ipCidrRouteStatus = 0
        ipCidrRouteMask = ""
        ipCidrRouteTos = 0
        ipCidrRouteNextHop = ""
        ipCidrRouteIfIndex = 0
        ipCidrRouteType = 0
        ipCidrRouteProto = 0
        ipCidrRouteAge = 0
        ipCidrRouteInf = 0

        for loop_rtIndex in routingtable:
            for ifAttr in routingtable[loop_rtIndex]:
                if ifAttr == 1:
                    ipCidrRouteDest = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 10:
                    ipCidrRouteNextHopAS = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 11:
                    ipCidrRouteMetric1 = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 12:
                    ipCidrRouteMetric2 = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 13:
                    ipCidrRouteMetric3 = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 14:
                    ipCidrRouteMetric4 = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 15:
                    ipCidrRouteMetric5 = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 16:
                    ipCidrRouteStatus = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 2:
                    ipCidrRouteMask = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 3:
                    ipCidrRouteTos = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 4:
                    ipCidrRouteNextHop = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 5:
                    ipCidrRouteIfIndex = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 6:
                    ipCidrRouteType = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 7:
                    ipCidrRouteProto = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 8:
                    ipCidrRouteAge = routingtable[loop_rtIndex][ifAttr]
                elif ifAttr == 9:
                    ipCidrRouteInfo = routingtable[loop_rtIndex][ifAttr]

            self.routingtable[loop_rtIndex] = device_routingtable( \
                ipCidrRouteDest, ipCidrRouteNextHopAS, ipCidrRouteMetric1, \
                ipCidrRouteMetric2, ipCidrRouteMetric3, ipCidrRouteMetric4, \
                ipCidrRouteMetric5, ipCidrRouteStatus, ipCidrRouteMask, \
                ipCidrRouteTos, ipCidrRouteNextHop, ipCidrRouteIfIndex, \
                ipCidrRouteType, ipCidrRouteProto, ipCidrRouteAge, \
                ipCidrRouteInf)

    def printroutingtable(self, outformat):
        """ Display Routing table """

        routingtable = self.routingtable
        ignoreoids = [8, 11, 12, 13, 14, 15]

        ipCidrRouteEntry = {
            1:"ipCidrRouteDest",
            2:"ipCidrRouteMask",
            3:"ipCidrRouteTos",
            4:"ipCidrRouteNextHop",
            5:"ipCidrRouteIfIndex",
            6:"ipCidrRouteType",
            7:"ipCidrRouteProto",
            8:"ipCidrRouteAge",
            9:"ipCidrRouteInfo",
            10:"ipCidrRouteNextHopAS",
            11:"ipCidrRouteMetric1",
            12:"ipCidrRouteMetric2",
            13:"ipCidrRouteMetric3",
            14:"ipCidrRouteMetric4",
            15:"ipCidrRouteMetric5",
            16:"ipCidrRouteStatus"
         }

        headerrow = []
        headerrow.append("hostname")

        for routeid in sorted(ipCidrRouteEntry):
            if routeid not in ignoreoids:
                headerrow.append(ipCidrRouteEntry[routeid])

        if outformat == 'csv':
            print ",".join(headerrow)
            for routeid in sorted(routingtable):
                currentrow = [self._hostname]
                for oid in sorted(routingtable[routeid]):
                    if oid not in ignoreoids:
                        currentrow.append(routingtable[routeid][oid])
                print ",".join(currentrow)
        elif outformat == 'json':
            print json.dumps(routingtable, sort_keys=True, indent=4, \
                separators=(',', ': '))

            '''routetablehash = {}

            for routeid in sorted(routingtable):
                routetablehash[self.hostname] = {}
                for oid in sorted(routingtable[routeid]):
                    if oid not in ignoreoids:
                        routetablehash[self.hostname][oid] =
                        currentrow.append(routingtable[routeid][oid])
                print ",".join(currentrow)'''
        else:
            thetable = prettytable.PrettyTable(headerrow)

            for routeid in sorted(routingtable):
                currentrow = [self._hostname]
                for oid in sorted(routingtable[routeid]):
                    if oid not in ignoreoids:
                        currentrow.append(routingtable[routeid][oid])
                thetable.add_row(currentrow)

            print thetable

    def printinterfacesumary(self, outformat):
        """ Display Interface Summary Information """

        interfacedata = self.interfacetable
        hostname = self._hostname

        numberup = 0
        numberdown = 0
        status = 0

        for ifindex in sorted(interfacedata):
            if interfacedata[ifindex]._ifAdminStatus < interfacedata[ifindex]._ifOperStatus:
                status = interfacedata[ifindex]._ifOperStatus
            else:
                status = interfacedata[ifindex]._ifAdminStatus

            if status == '1':
                numberup = int(numberup + 1)
            else:
                numberdown = int(numberdown + 1)

        percentfree = (numberdown / (numberup + numberdown))*100

        if outformat == 'csv':
            print 'hostname,up,down,percent'
            print '{0},{1},{2},{3}'.format(hostname, numberup, numberdown, \
                percentfree)
        else:
            print "Hostname: {0}".format(hostname)
            print "Total Number up: {0}".format(numberup)
            print "Total Number down: {0}".format(numberdown)
            print "Percent Free: {0}".format(percentfree)


    def printinterfacestats(self, outformat):
        """ display all interface detail """

        interfacedata = self.interfacetable
        hostname = self._hostname

        ignoreoids = [22, 21, 18, 12]

        ifmib = {
            1:"ifIndex",
            2:"ifDescr",
            3:"ifType",
            4:"ifMtu",
            5:"ifSpeed",
            6:"ifPhysAddress",
            7:"ifAdminStatus",
            8:"ifOperStatus",
            9:"ifLastChange",
            10:"ifInOctets",
            11:"ifUcastPkts",
            12:"ifInNUcastPkts",
            13:"ifInDiscards",
            14:"ifInErrors",
            15:"ifInUnknownProtos",
            16:"ifOutOctets",
            17:"ifOutUcastPkts",
            18:"ifOutNUcastPkts",
            19:"ifOutDiscards",
            20:"ifOutErrors",
            21:"ifOutQLen",
            22:"ifSpecific"
        }

        # oid value of 8 or 7
        ifstatus = {
            1: "up",
            2: "down",
            3: "testing",
            4: "unknown",
            5: "dormant",
            6: "notPresent",
            7: "lowerLayerDown"
        }

        # Print CSV Formated Data
        if outformat == 'csv':
            headerrow = []
            headerrow.append("hostname")

            for ifid in sorted(ifmib):
                if ifid not in ignoreoids:
                    headerrow.append(ifmib[ifid])

            print ",".join(headerrow)

            for ifindex in sorted(interfacedata):
                currentrow = []
                currentrow.append(hostname)

                for oid in sorted(interfacedata[ifindex]):
                    for skip in ignoreoids:
                        if oid == skip:
                            exclude = True
                            break
                        else:
                            exclude = False
                    if exclude != True:
                        if oid == 8 or oid == 7:
                            currentrow.append(ifstatus[int(interfacedata[ifindex][oid])])
                        else:
                            currentrow.append(interfacedata[ifindex][oid])
                print ",".join(currentrow)

        elif outformat == 'table':
            headerrow = []
            headerrow.append("hostname")

            for ifid in sorted(ifmib):
                if ifid not in ignoreoids:
                    headerrow.append(ifmib[ifid])

            thetable = prettytable.PrettyTable(headerrow)

            for ifindex in sorted(interfacedata):
                currentrow = [hostname]
                for oid in sorted(interfacedata[ifindex]):
                    if oid not in ignoreoids:
                        if oid == 8 or oid == 7:
                            currentrow.append(ifstatus[int(interfacedata[ifindex][oid])])
                        else:
                            currentrow.append(interfacedata[ifindex][oid])
                thetable.add_row(currentrow)
            print thetable

        elif outformat == 'json':

            hostinterfaces = {}
            #hostinterfaces[self._hostname] = {}

            for ifindex in sorted(interfacedata):
                #print dict(interfacedata[ifindex].dictrepr().items())
                hostinterfaces[ifindex] = dict(interfacedata[ifindex].dictrepr().items())

            #print hostinterfaces
            print json.dumps(hostinterfaces, sort_keys=True, indent=4, \
                separators=(',', ': '))

        else:
        # Print Detailed textual list of interface information
            for ifindex in sorted(interfacedata):
                print "\nInterface Number", ifindex
                for oid in sorted(interfacedata[ifindex]):
                    if oid not in ignoreoids:
                        print "{0} ({1}) =".format(ifmib[oid], oid),

                        if oid == 8 or oid == 7:
                            print ifstatus[int(interfacedata[ifindex][oid])]
                        # Need to fid display of MAC Addresses
                        #elif oid == 6:
                        #   print "{0}".format(interfacedata[ifindex][oid].hexdigits)
                        else:
                            print interfacedata[ifindex][oid]
                print "\n",

    def returnjson(self):

        currentdevice = {}

        currentdevice['hostname'] = self._hostname
        currentdevice['osversion'] = self._osversion
        currentdevice['primaryipaddress'] = self._primaryipaddress
        currentdevice['datasource'] = self._datasource
        currentdevice['routingtable'] = self.routingtable
        currentdevice['interfacetable'] = self.interfacetable

        #print currentdevice
        return json.dumps(currentdevice, sort_keys=True, indent=4, \
            separators=(',', ': '))


