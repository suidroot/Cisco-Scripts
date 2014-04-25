
import json
import prettytable

class device(object):
	"""

		Definitaion of a device

	"""
	def __init__(self, hostname, osversion, ipaddress, datasource, routingtable, interfacetable):
		#super(device, self).__init__()
		self.hostname = hostname
		self.osversion = osversion
		self.ipaddress = ipaddress
		self.datasource = datasource
		self.routingtable = routingtable
		self.interfacetable = interfacetable



	def printinterfacestats(self, format):

		interfacedata = self.interfacetable
		hostname = self.hostname

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

		
		if format == 'csv':
			headerrow = []
			headerrow.append("hostname")
						
			for id in sorted(ifmib):
				if id not in ignoreoids:
					headerrow.append(ifmib[id])

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

		elif format == 'table':
			headerrow = []
			headerrow.append("hostname")
						
			for id in sorted(ifmib):
				if id not in ignoreoids:
					headerrow.append(ifmib[id])

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
						#	print "{0}".format(interfacedata[ifindex][oid].hexdigits)
						else:
							print interfacedata[ifindex][oid]
				print "\n",

	def printinterfacesumary(self, format):

		interfacedata = self.interfacetable
		hostname = self.hostname
		#format = 'text'

		numberup = 0
		numberdown = 0
		status = 0
		
		for ifindex in sorted(interfacedata):
			if interfacedata[ifindex][7] < interfacedata[ifindex][8]:
				status = interfacedata[ifindex][8]
			else:
				status = interfacedata[ifindex][7]
					
			if status == '1':
				numberup = int(numberup + 1)
			else:
				numberdown = int(numberdown + 1)

		percentfree = (numberdown / (numberup + numberdown))*100
		
		if format == 'csv':
			print 'hostname,up,down,percent'
			print '{0},{1},{2},{3}'.format(hostname, numberup, numberdown, percentfree)
		else:
			print "Hostname: {0}".format(hostname)			
			print "Total Number up: {0}".format(numberup)
			print "Total Number down: {0}".format(numberdown)
			print "Percent Free: {0}".format(percentfree)

	def printroutingtable (self, format):

		routingtable = self.routingtable

		ignoreoids = [8,11,12,13,14,15]

		ipCidrRouteEntry = {
			1:"ipCidrRouteDest",
			10:"ipCidrRouteNextHopAS",
			11:"ipCidrRouteMetric1",
			12:"ipCidrRouteMetric2",
			13:"ipCidrRouteMetric3",
			14:"ipCidrRouteMetric4",
			15:"ipCidrRouteMetric5",
			16:"ipCidrRouteStatus",
			2:"ipCidrRouteMask",
			3:"ipCidrRouteTos",
			4:"ipCidrRouteNextHop",
			5:"ipCidrRouteIfIndex",
			6:"ipCidrRouteType",
			7:"ipCidrRouteProto",
			8:"ipCidrRouteAge",
			9:"ipCidrRouteInfo"
		}

		headerrow = []
		headerrow.append("hostname")
					
		for id in sorted(ipCidrRouteEntry):
			if id not in ignoreoids:
				headerrow.append(ipCidrRouteEntry[id])

		if format == 'csv':
			print ",".join(headerrow)
			for routeid in sorted(routingtable):
				currentrow = [self.hostname]
				for oid in sorted(routingtable[routeid]):
					if oid not in ignoreoids:
						currentrow.append(routingtable[routeid][oid])
				print ",".join(currentrow)

		else:
			thetable = prettytable.PrettyTable(headerrow)

			for routeid in sorted(routingtable):
				currentrow = [self.hostname]
				for oid in sorted(routingtable[routeid]):
					if oid not in ignoreoids:
						currentrow.append(routingtable[routeid][oid])
				thetable.add_row(currentrow)

			print thetable

	def printallinfo(self, format):
		print "Hostname: {0}".format(self.hostname) 
		print "Version: {0}".format(self.osversion)
		print "IP Address: {0}".format(self.ipaddress)
		print "Data Source: {0}".format(self.datasource)
		print "\mRouting Table"

		device.printroutingtable(self, 'table')

		print "\nInterface Infomration"

		device.printinterfacestats(self, 'table')


	def returnjson(self):

		device = {}

		device['hostname'] = self.hostname
		device['osversion'] = self.osversion
		device['ipaddress'] = self.ipaddress
		device['datasource'] = self.datasource
		device['routingtable'] = self.routingtable
		device['interfacetable'] = self.interfacetable

		#print device
		return json.dumps(device, sort_keys=True, indent=4, separators=(',', ': '))
