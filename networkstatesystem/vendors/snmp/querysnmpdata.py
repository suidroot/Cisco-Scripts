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

