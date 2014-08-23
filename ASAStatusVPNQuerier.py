#!/usr/bin/env python

from networkstatesystem.vendors.snmp import querysnmpdata
import string
# import sys
import sqlite3
import argparse

__author__ = "Ben Mason"
__copyright__ = "Copyright 2014"
__version__ = "1.0.0"
__email__ = "su1droot@gmail.com"
__status__ = "Development"

# class tunnel:
class ipsectunnel(object):

    def __init__(self, tunnelid):

        self.cikeTunIndex = tunnelid
        self.cikeTunLocalType = 0
        self.cikeTunLocalValue = ""
        self.cikeTunLocalAddr = ""
        self.cikeTunLocalName = ""
        self.cikeTunRemoteType = 0
        self.cikeTunRemoteValue = ""
        self.cikeTunRemoteAddr = ""
        self.cikeTunRemoteName = ""
        self.cikeTunNegoMode = 0
        self.cikeTunDiffHellmanGrp = 0
        self.cikeTunEncryptAlgo = 0
        self.cikeTunHashAlgo = 0
        self.cikeTunAuthMethod = 0
        self.cikeTunLifeTime = 0
        self.cikeTunActiveTime = 0
        self.cikeTunSaRefreshThreshold = 0
        self.cikeTunTotalRefreshes = 0
        self.cikeTunInOctets = 0
        self.cikeTunInPkts = 0
        self.cikeTunInDropPkts = 0
        self.cikeTunInNotifys = 0
        self.cikeTunInP2Exchgs = 0
        self.cikeTunInP2ExchgInvalids = 0
        self.cikeTunInP2ExchgRejects = 0
        self.cikeTunInP2SaDelRequests = 0
        self.cikeTunOutOctets = 0
        self.cikeTunOutPkts = 0
        self.cikeTunOutDropPkts = 0
        self.cikeTunOutNotifys = 0
        self.cikeTunOutP2Exchgs = 0
        self.cikeTunOutP2ExchgInvalids = 0
        self.cikeTunOutP2ExchgRejects = 0
        self.cikeTunOutP2SaDelRequests = 0
        self.cikeTunStatus = 0

    def __str__(self):

        return_string = "Tunnel Index: {0}\n".format(self.cikeTunIndex)
        return_string += "cikeTunLocalType: {0}\n".format(self.cikeTunLocalType)
        return_string += "cikeTunLocalValue: {0}\n".format(self.cikeTunLocalValue)
        return_string += "cikeTunLocalAddr: {0}\n".format(self.cikeTunLocalAddr)
        return_string += "cikeTunLocalName: {0}\n".format(self.cikeTunLocalName)
        return_string += "cikeTunRemoteType: {0}\n".format(self.cikeTunRemoteType)
        return_string += "cikeTunRemoteValue: {0}\n".format(self.cikeTunRemoteValue)
        return_string += "cikeTunRemoteAddr: {0}\n".format(self.cikeTunRemoteAddr)
        return_string += "cikeTunRemoteName: {0}\n".format(self.cikeTunRemoteName)
        return_string += "cikeTunNegoMode: {0}\n".format(self.cikeTunNegoMode)
        return_string += "cikeTunDiffHellmanGrp: {0}\n".format(self.cikeTunDiffHellmanGrp)
        return_string += "cikeTunEncryptAlgo: {0}\n".format(self.cikeTunEncryptAlgo)
        return_string += "cikeTunHashAlgo: {0}\n".format(self.cikeTunHashAlgo)
        return_string += "cikeTunAuthMethod: {0}\n".format(self.cikeTunAuthMethod)
        return_string += "cikeTunLifeTime: {0}\n".format(self.cikeTunLifeTime)
        return_string += "cikeTunActiveTime: {0}\n".format(self.cikeTunActiveTime)
        return_string += "cikeTunSaRefreshThreshold: {0}\n".format(self.cikeTunSaRefreshThreshold)
        return_string += "cikeTunTotalRefreshes: {0}\n".format(self.cikeTunTotalRefreshes)
        return_string += "cikeTunInOctets: {0}\n".format(self.cikeTunInOctets)
        return_string += "cikeTunInPkts: {0}\n".format(self.cikeTunInPkts)
        return_string += "cikeTunInDropPkts: {0}\n".format(self.cikeTunInDropPkts)
        return_string += "cikeTunInNotifys: {0}\n".format(self.cikeTunInNotifys)
        return_string += "cikeTunInP2Exchgs: {0}\n".format(self.cikeTunInP2Exchgs)
        return_string += "cikeTunInP2ExchgInvalids: {0}\n".format(self.cikeTunInP2ExchgInvalids)
        return_string += "cikeTunInP2ExchgRejects: {0}\n".format(self.cikeTunInP2ExchgRejects)
        return_string += "cikeTunInP2SaDelRequests: {0}\n".format(self.cikeTunInP2SaDelRequests)
        return_string += "cikeTunOutOctets: {0}\n".format(self.cikeTunOutOctets)
        return_string += "cikeTunOutPkts: {0}\n".format(self.cikeTunOutPkts)
        return_string += "cikeTunOutDropPkts: {0}\n".format(self.cikeTunOutDropPkts)
        return_string += "cikeTunOutNotifys: {0}\n".format(self.cikeTunOutNotifys)
        return_string += "cikeTunOutP2Exchgs: {0}\n".format(self.cikeTunOutP2Exchgs)
        return_string += "cikeTunOutP2ExchgInvalids: {0}\n".format(self.cikeTunOutP2ExchgInvalids)
        return_string += "cikeTunOutP2ExchgRejects: {0}\n".format(self.cikeTunOutP2ExchgRejects)
        return_string += "cikeTunOutP2SaDelRequests: {0}\n".format(self.cikeTunOutP2SaDelRequests)
        return_string += "cikeTunStatus: {0}\n".format(self.cikeTunStatus)

        return return_string

    def returnlist(self):

        return [int(self.cikeTunLocalType),
        unicode(self.cikeTunLocalValue),
        unicode(self.cikeTunLocalAddr),
        unicode(self.cikeTunLocalName),
        int(self.cikeTunRemoteType),
        unicode(self.cikeTunRemoteValue),
        unicode(self.cikeTunRemoteAddr),
        unicode(self.cikeTunRemoteName),
        int(self.cikeTunNegoMode),
        int(self.cikeTunDiffHellmanGrp),
        int(self.cikeTunEncryptAlgo),
        int(self.cikeTunHashAlgo),
        int(self.cikeTunAuthMethod),
        int(self.cikeTunLifeTime),
        int(self.cikeTunActiveTime),
        int(self.cikeTunSaRefreshThreshold),
        int(self.cikeTunTotalRefreshes),
        int(self.cikeTunInOctets),
        int(self.cikeTunInPkts),
        int(self.cikeTunInDropPkts),
        int(self.cikeTunInNotifys),
        int(self.cikeTunInP2Exchgs),
        int(self.cikeTunInP2ExchgInvalids),
        int(self.cikeTunInP2ExchgRejects),
        int(self.cikeTunInP2SaDelRequests),
        int(self.cikeTunOutOctets),
        int(self.cikeTunOutPkts),
        int(self.cikeTunOutDropPkts),
        int(self.cikeTunOutNotifys),
        int(self.cikeTunOutP2Exchgs),
        int(self.cikeTunOutP2ExchgInvalids),
        int(self.cikeTunOutP2ExchgRejects),
        int(self.cikeTunOutP2SaDelRequests),
        int(self.cikeTunStatus),
        self.cikeTunIndex]

    def snmpsetvalue(self, counter, tunnelvalue):

        if counter == 1:
            self.cikeTunIndex = tunnelvalue
        elif counter == 2:
            self.cikeTunLocalType = tunnelvalue
        elif counter == 3:
            self.cikeTunLocalValue = tunnelvalue
        elif counter == 4:
            self.cikeTunLocalAddr = tunnelvalue
        elif counter == 5:
            self.cikeTunLocalName = tunnelvalue
        elif counter == 6:
            self.cikeTunRemoteType = tunnelvalue
        elif counter == 7:
            self.cikeTunRemoteValue = tunnelvalue
        elif counter == 8:
            self.cikeTunRemoteAddr = tunnelvalue
        elif counter == 9:
            self.cikeTunRemoteName = tunnelvalue
        elif counter == 10:
            self.cikeTunNegoMode = tunnelvalue
        elif counter == 11:
            self.cikeTunDiffHellmanGrp = tunnelvalue
        elif counter == 12:
            self.cikeTunEncryptAlgo = tunnelvalue
        elif counter == 13:
            self.cikeTunHashAlgo = tunnelvalue
        elif counter == 14:
            self.cikeTunAuthMethod = tunnelvalue
        elif counter == 15:
            self.cikeTunLifeTime = tunnelvalue
        elif counter == 16:
            self.cikeTunActiveTime = tunnelvalue
        elif counter == 17:
            self.cikeTunSaRefreshThreshold = tunnelvalue
        elif counter == 18:
            self.cikeTunTotalRefreshes = tunnelvalue
        elif counter == 19:
            self.cikeTunInOctets = tunnelvalue
        elif counter == 20:
            self.cikeTunInPkts = tunnelvalue
        elif counter == 21:
            self.cikeTunInDropPkts = tunnelvalue
        elif counter == 22:
            self.cikeTunInNotifys = tunnelvalue
        elif counter == 23:
            self.cikeTunInP2Exchgs = tunnelvalue
        elif counter == 24:
            self.cikeTunInP2ExchgInvalids = tunnelvalue
        elif counter == 25:
            self.cikeTunInP2ExchgRejects = tunnelvalue
        elif counter == 26:
            self.cikeTunInP2SaDelRequests = tunnelvalue
        elif counter == 27:
            self.cikeTunOutOctets = tunnelvalue
        elif counter == 28:
            self.cikeTunOutPkts = tunnelvalue
        elif counter == 29:
           self.cikeTunOutDropPkts = tunnelvalue
        elif counter == 30:
            self.cikeTunOutNotifys = tunnelvalue
        elif counter == 31:
            self.cikeTunOutP2Exchgs = tunnelvalue
        elif counter == 32:
            self.cikeTunOutP2ExchgInvalids = tunnelvalue
        elif counter == 33:
            self.cikeTunOutP2ExchgRejects = tunnelvalue
        elif counter == 34:
            self.cikeTunOutP2SaDelRequests = tunnelvalue
        elif counter == 35:
            self.cikeTunStatus = tunnelvalue
        else:
            print "Bad OID"

def collectargs():
    """ Defines the Command line Arguments """

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--ip_address', 
        help='i.e. -i "192.168.31.21"',
        default="10.0.0.1")
    parser.add_argument('-c', '--community', 
        help='Enter SNMP Community',
        default="public")
    parser.add_argument('-d', '--database', 
        help='Database file',
        default="tunnels.db")

    arg = parser.parse_args()

    return arg

def writetodatabase(dbfile, tunnellist):

    db = sqlite3.connect(dbfile)
    curr = db.cursor()

    try:
        curr.execute('''CREATE TABLE tunnels (active int,
            cikeTunLocalType int,
            cikeTunLocalValue text,
            cikeTunLocalAddr text,
            cikeTunLocalName text,
            cikeTunRemoteType int,
            cikeTunRemoteValue text,
            cikeTunRemoteAddr text,
            cikeTunRemoteName text,
            cikeTunNegoMode int,
            cikeTunDiffHellmanGrp int,
            cikeTunEncryptAlgo int,
            cikeTunHashAlgo int,
            cikeTunAuthMethod int,
            cikeTunLifeTime int,
            cikeTunActiveTime int,
            cikeTunSaRefreshThreshold int,
            cikeTunTotalRefreshes int,
            cikeTunInOctets int,
            cikeTunInPkts int,
            cikeTunInDropPkts int,
            cikeTunInNotifys int,
            cikeTunInP2Exchgs int,
            cikeTunInP2ExchgInvalids int,
            cikeTunInP2ExchgRejects int,
            cikeTunInP2SaDelRequests int,
            cikeTunOutOctets int,
            cikeTunOutPkts int,
            cikeTunOutDropPkts int,
            cikeTunOutNotifys int,
            cikeTunOutP2Exchgs int,
            cikeTunOutP2ExchgInvalids int,
            cikeTunOutP2ExchgRejects int,
            cikeTunOutP2SaDelRequests int,
            cikeTunStatus int,
            cikeTunIndex int PRIMARY KEY UNIQUE)''')
    except sqlite3.OperationalError:
        print "Skipping Table Creation"

    for line in tunnellist:
        print line,
        print tunnellist[line].returnlist()
        try:
            curr.execute('INSERT INTO tunnels VALUES (1,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', tunnellist[line].returnlist())
        except sqlite3.IntegrityError:
            curr.execute('''UPDATE tunnels SET
                active = 1,
                cikeTunLocalType = ?,
                cikeTunLocalValue = ?,
                cikeTunLocalAddr = ?,
                cikeTunLocalName = ?,
                cikeTunRemoteType = ?,
                cikeTunRemoteValue = ?,
                cikeTunRemoteAddr = ?,
                cikeTunRemoteName = ?,
                cikeTunNegoMode = ?,
                cikeTunDiffHellmanGrp = ?,
                cikeTunEncryptAlgo = ?,
                cikeTunHashAlgo = ?,
                cikeTunAuthMethod = ?,
                cikeTunLifeTime = ?,
                cikeTunActiveTime = ?,
                cikeTunSaRefreshThreshold = ?,
                cikeTunTotalRefreshes = ?,
                cikeTunInOctets = ?,
                cikeTunInPkts = ?,
                cikeTunInDropPkts = ?,
                cikeTunInNotifys = ?,
                cikeTunInP2Exchgs = ?,
                cikeTunInP2ExchgInvalids = ?,
                cikeTunInP2ExchgRejects = ?,
                cikeTunInP2SaDelRequests = ?,
                cikeTunOutOctets = ?,
                cikeTunOutPkts = ?,
                cikeTunOutDropPkts = ?,
                cikeTunOutNotifys = ?,
                cikeTunOutP2Exchgs = ?,
                cikeTunOutP2ExchgInvalids = ?,
                cikeTunOutP2ExchgRejects = ?,
                cikeTunOutP2SaDelRequests = ?,
                cikeTunStatus = ? WHERE cikeTunIndex = ?''', tunnellist[line].returnlist())

    db.commit()
    db.close()

def cleanuptunnels(dbfile, tunnellist):

    db = sqlite3.connect(dbfile)
    curr1 = db.cursor()
    curr2 = db.cursor()


    try:
        tunnelkeys = tunnellist.keys()
    except AttributeError:
        tunnelkeys = []

    # print tunnellist.keys()

    curr1.execute('''SELECT cikeTunIndex FROM tunnels WHERE active != 0''')

    for row in curr1:
        print row

        # row = int(row)
        if row[0] not in tunnelkeys:
            curr2.execute('''UPDATE tunnels SET active = 0 WHERE cikeTunIndex = ?''', row) 
            print "Deativated tunnel {0}".format(row)

    db.commit()
    db.close()


def queryvpndata(args):

    alltunnels = {}

    oids = '1.3.6.1.4.1.9.9.171.1.2.3.1'
    community = args.community
    device = args.ip_address

    walkreturn = querysnmpdata.snmpwalkoid(device, community, oids)

    if walkreturn == []:
        print "No Active tunnels"
        alltunnels = []
    else:
        for line in walkreturn:
            oid, value = line[0]
            oid = string.replace(str(oid), oids+".", "")
            counter, tunnelid = oid.split(".") 

            try:
                alltunnels[int(tunnelid)].snmpsetvalue(int(counter), value) 
            except:
                alltunnels[int(tunnelid)] = ipsectunnel(int(tunnelid))
                alltunnels[int(tunnelid)].snmpsetvalue(int(counter), value.prettyPrinter()) 

    return alltunnels


# Start Main functions
args = collectargs()
alltunnels = queryvpndata(args)
writetodatabase(args.database, alltunnels)
cleanuptunnels(args.database, alltunnels)
