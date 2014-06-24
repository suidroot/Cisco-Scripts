#!/usr/bin/env python


from querysnmpdata import snmpwalkoid
from querysnmpdata import snmpgetoid
import string

class snmp(object):

    def ___init___(self, address, community):

        self.community = community
        self.address = address

    def getInterfaces(self):
        """ add a new interface """

        oids = '1.3.6.1.2.1.2.2.1'
        interfacetable = {}

        walkreturn = snmpwalkoid(device, community, oids)

        for currentrow in walkreturn:
            for indexoid, val in currentrow:
                replaced = string.replace(indexoid.prettyPrint(), oids, '')[1::]
                value = val.prettyPrint()

                (oidnumber, ifindex) = string.split(replaced, '.')
                ifindex = int(ifindex)
                oidnumber = int(oidnumber)

                if ifindex in interfacetable:
                    interfacetable[ifindex][oidnumber] = value
                else:
                    interfacetable[ifindex] = {}
                    interfacetable[ifindex][oidnumber] = value

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

            interfacetable[loop_ifIndex] = device_interface(ifIndex, \
                ifDescr, ifType, ifMtu, ifSpeed, ifPhysAddress, ifAdminStatus, \
                ifOperStatus, ifLastChange, ifInOctets, ifUcastPkts, \
                ifInNUcastPkts, ifInDiscards, ifInErrors, ifInUnknownProtos, \
                ifOutOctets, ifOutUcastPkts, ifOutNUcastPkts, ifOutDiscards, \
                ifOutErrors, ifOutQLen, ifSpecific)

        return interfacetable

    def getRoutes(self):
        """ Add a new Route """

        oids = '1.3.6.1.2.1.4.24.4.1.'
        walkreturn = snmpwalkoid(device, community, oids)

        # oid example 1.3.6.1.2.1.4.24.4.1.24.4.1.1.10.5.6.0.255.255.255.0.0.0.0.0.0
        routingtable = {}

        for currentrow in walkreturn:
            for indexoid, val in currentrow:
                replaced = string.replace(indexoid.prettyPrint(), oids, '')
                value = val.prettyPrint()

                (oidnumber, routeindex) = string.split(replaced, '.', 1)
                oidnumber = int(oidnumber)

                if routeindex in routingtable:
                    routingtable[routeindex][oidnumber] = value
                else:
                    routingtable[routeindex] = {}
                    routingtable[routeindex][oidnumber] = value

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

            routingtable[loop_rtIndex] = device_routingtable( \
                ipCidrRouteDest, ipCidrRouteNextHopAS, ipCidrRouteMetric1, \
                ipCidrRouteMetric2, ipCidrRouteMetric3, ipCidrRouteMetric4, \
                ipCidrRouteMetric5, ipCidrRouteStatus, ipCidrRouteMask, \
                ipCidrRouteTos, ipCidrRouteNextHop, ipCidrRouteIfIndex, \
                ipCidrRouteType, ipCidrRouteProto, ipCidrRouteAge, \
                ipCidrRouteInf)

        return routingtable


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


    def getHostname(device, community):
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

    def getFacts(self):

        cpu_utilization = self.getCPU()
        free_memory = self.getfreeMemory()
        total_memory = self.gettotalMemory()
        hostname = self.getHostname()
        uptime = self.getUptime()
        platform = self.getPlatform()
        serial_number = self.getserialNumber()
        reboot_reason = self.getReasonforReboot()
        connect_ip = self.address
        interfaces = self.getInterfaces()

        facts = {'connect_ip': connect_ip,'serial_number': serial_number, 'cpu_utilization': cpu_utilization, 'free_system_memory': free_memory, 
                    'total_sytem_memory': total_memory,'hostname': hostname, 'system_uptime': uptime, 'platform': platform,
                    'last_reboot_reason': reboot_reason, 'vendor':'cisco','interfaces':interfaces,'var_name':self.obj}

        return facts

