#!/usr/bin/env python

from pysnmp.entity.rfc3413.oneliner import cmdgen

def snmpwalkoid(device, community, oids):
# This function queries the device for a given ip, community and OID. It will talk the OID tree.	
	snmpdata = {}
	
	cmdGen = cmdgen.CommandGenerator()
	
	errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
		# securityIndex is a dumby value does nothing
		cmdgen.CommunityData('securityIndex', community, mpModel=1),
		cmdgen.UdpTransportTarget((device, 161)),
		oids
	)
	
	if errorIndication:
		print(errorIndication)
	else:
		
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
				)
			)
		else:
			return varBindTable

def snmpgetoid(device, community, oids):
# This function queries the device for a given ip, community and OID. It will talk the OID tree.	
	snmpdata = {}
	
	cmdGen = cmdgen.CommandGenerator()
	
	errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.getCmd(
		# securityIndex is a dumby value does nothing
		cmdgen.CommunityData('securityIndex', community, mpModel=1),
		cmdgen.UdpTransportTarget((device, 161)),
		oids
	)
	
	if errorIndication:
		print(errorIndication)
	else:
		
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
				)
			)
		else:
			return varBindTable[0]

def hostinfo(device, community):
	sysName = ".1.3.6.1.2.1.1.5.0"
	osVersion = ".1.3.6.1.2.1.25.6.3.1.2.2"
	
	oid, hostreturn =  snmpgetoid(device, community, sysName)
	
	'''oid, versionreturn = snmpgetoid(device, community, osVersion)

	if format == 'csv':
		print 'hostname,version'
		print '{0},{1}'.format(hostreturn.prettyPrint(),versionreturn.prettyPrint())
	else:	
		print "Hostname: %s" % hostreturn.prettyPrint()
		print "OS Version: %s" % versionreturn.prettyPrint()'''
	
	return hostreturn.prettyPrint()
	
