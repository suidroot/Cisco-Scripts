#!/usr/bin/env python

import string
import ipaddress
import sys
from graphviz import Digraph
# from graphviz import Graph
from networkstatesystem.vendors.snmp import querydevicedata

neighbortable = {}
hosts = []
hostfile = 'hostlist.txt'
graphfilename = 'test2'

with open(hostfile, "r") as host_list:
    for line in host_list:
        line = line.strip()
        if line == "":
            # if lines blank skip
            pass
        elif line[0] == "#":
            # if comment line skip
            pass
        else:
            (dev_ipaddress, community, datasource) = string.split(line, ':')
            
            if ipaddress.ip_address(dev_ipaddress):
                print dev_ipaddress

                hostname = querydevicedata.gethostname(dev_ipaddress, community)
                neighbortable[hostname] = {}
                neighbortable[hostname] = querydevicedata.collectcdpneighbors(dev_ipaddress, community.rstrip())
            else:
                errormsg = "Invalid IP Address in config file: " + str(dev_ipaddress)
                sys.exit(errormsg)

# Directed Graph
dot = Digraph(comment='The Network')
# UnDirected Graph
# dot = Graph(comment='The Network')

for device in neighbortable:
    dot.node(device)
    for entry in neighbortable[device]:
        neighborhostname = neighbortable[device][entry][6]
        dot.edge(device,neighborhostname)

dot.engine = 'circo'
print dot.source
dot.render(filename=graphfilename)

