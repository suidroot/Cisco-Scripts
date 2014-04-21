#!/usr/bin/env python

from . import querysnmpdata

def hostinfo(device, community):
	sysName = ".1.3.6.1.2.1.1.5.0"
	osVersion = ".1.3.6.1.2.1.25.6.3.1.2.2"
	
	oid, hostreturn = querysnmpdata.snmpgetoid(device, community, sysName)
	
	'''oid, versionreturn = snmpgetoid(device, community, osVersion)

	if format == 'csv':
		print 'hostname,version'
		print '{0},{1}'.format(hostreturn.prettyPrint(),versionreturn.prettyPrint())
	else:	
		print "Hostname: %s" % hostreturn.prettyPrint()
		print "OS Version: %s" % versionreturn.prettyPrint()'''
	
	return hostreturn.prettyPrint()
