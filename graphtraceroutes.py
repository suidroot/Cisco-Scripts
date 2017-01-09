#!/usr/bin/env python

"""
R1#traceroute 172.16.1.4

Type escape sequence to abort.
Tracing the route to 172.16.1.4

  1 192.168.1.1 16 msec 24 msec 20 msec
  2 192.168.2.2 48 msec 56 msec 28 msec
  3 192.168.2.10 76 msec 48 msec 56 msec
  4 192.168.1.14 [AS 1] 64 msec 48 msec 76 msec
"""


from networkstatesystem.vendors.ssh.sshhelper import *
from graphviz import Digraph

allitems = {}
graphfilename = 'test-traceroute'

def parsetraceroute(text):

    hops = []

    for line in text[5:]:
        line = line.strip()
        print line.split(" ")
        try: 
            line.strip()
            nexthop = line.split(" ")[1]
            print "nextop: " + nexthop
            hops.append(nexthop)

        except IndexError:

            pass

    return hops

hostlist = ['172.16.1.1', '172.16.1.2','172.16.1.3','172.16.1.4']


for line in hostlist:

    # ip, username, password = line.split(":")

    ip = line
    username = 'cisco'
    password = '1234567'
    enable = '1234567'

    remote_conn_pre, remote_conn = sshconnect(ip, username, password, 'ios', '')
    allitems[ip] = {}

    for tracehost in hostlist:

        content = ssh_runcommand(remote_conn, "traceroute " + tracehost)
        # print content
        hops = parsetraceroute(content)
        allitems[ip][tracehost] = hops


dot = Digraph(comment='The Network')
# UnDirected Graph
# dot = Graph(comment='The Network')

for device in allitems:
    dot.node(device)
    for entry in allitems[device]:
        # neighborhostname = allitems[device][entry]
        hop1 = device
        allitems[device][entry].append(entry)
        for hop in allitems[device][entry]:
            hop2 = hop
            dot.edge(hop1,hop2)
            hop1 = hop2

dot.engine = 'circo'
print dot.source
dot.render(filename=graphfilename)
