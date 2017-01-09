#!/usr/bin/env python
from jnpr.junos import Device


# Session ID: 23082, Policy name: trust-to-untrust/4, Timeout: 164, Valid
#   In: 10.5.6.54/55269 --> 17.172.232.166/5223;tcp, If: vlan.0, Pkts: 20, Bytes: 5629
#   Out: 17.172.232.166/5223 --> 67.253.16.3/25955;tcp, If: fe-0/0/0.0, Pkts: 26, Bytes: 5742

session = {}

# sessionfile = "sessions.txt"


ip = '10.5.6.254'
username = 'locutus'
password = 'xxxxxx'


dev = Device(host=ip, user=username, password=password)
dev.open()
sessionoutput = dev.cli('show security flow session brief')

# print sessionlist

sessionlist = sessionoutput.split("\n")

# with open(sessionfile, "r") as sessionlist:

for line in sessionlist:

    temp = []
    # print line

    if "Session ID" in line:
        temp = line.split(", ")
        sessionid = int(temp[0].split("Session ID: ")[1])
        policyname = temp[1].split("Policy name: ")[1]
        timeout = int(temp[2].split("Timeout: ")[1])
        session[sessionid] = {}
        session[sessionid]['policyname'] = policyname
        session[sessionid]['timeout'] = timeout
    elif "In: " in line:
        temp = line.split(", ")
        temp2 = line.split(" ")
        # print temp2
        temp2[5] = temp2[5].strip(",")
        session[sessionid]['insrcaddr'], session[sessionid]['insrcport'] = temp2[3].split("/")
        session[sessionid]['indstaddr'], session[sessionid]['indstport'] = temp2[5].split("/")
        session[sessionid]['indstport'], session[sessionid]['inproto'] = session[sessionid]['indstport'].split(";")
        # print session[sessionid]['indstport']

        session[sessionid]['inpkt'] = int(temp[2].split("Pkts: ")[1])
        session[sessionid]['inbits'] = int(temp[3].split("Bytes: ")[1]) * 8

    elif "Out: " in line:
        temp = line.split(", ")
        temp2 = line.split(" ")
        # print temp2
        temp2[5] = temp2[5].strip(",")


        session[sessionid]['outsrcaddr'], session[sessionid]['outsrcport'] = temp2[3].split("/")
        session[sessionid]['outdstaddr'], session[sessionid]['outdstport'] = temp2[5].split("/")
        session[sessionid]['outdstport'], session[sessionid]['outproto'] = session[sessionid]['outdstport'].split(";")
        session[sessionid]['outpkt'] = int(temp[2].split("Pkts: ")[1])
        session[sessionid]['outbits'] = int(temp[3].split("Bytes: ")[1]) * 8

    elif "Total sessions: " in line:
        totalsessions = int(line.split("Total sessions: ")[1])

for sessionno in session:
    print "Sess: {0}, Src: {1}, Dst: {2}, DstPrt: {3}, Bits: {4}".format(sessionno, session[sessionno]['insrcaddr'], session[sessionno]['indstaddr'], session[sessionno]['indstport'], session[sessionno]['inbits'])


print "Total Sessions: {0}".format(totalsessions)
