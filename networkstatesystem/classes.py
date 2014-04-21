
class device(object):
	"""

		Definitaion of a device

	"""
	def __init__(self, hostname, ipaddress, datasource, routingtable, interfacetable):
		#super(device, self).__init__()
		self.hostname = hostname
		self.ipaddress = ipaddress
		self.datasource = datasource
		self.routingtable = routingtable
		self.interfacetable = interfacetable

	def printinfo(self):
		print "Hostname: {0}".format(self.hostname) 
		print "IP Address {0}".format(self.ipaddress)
		print "Data Source: {0}".format(self.datasource)
		print "Routing Table: {0}".format(self.routingtable)
		print "Interfaces: {0}".format(self.interfacetable)
		