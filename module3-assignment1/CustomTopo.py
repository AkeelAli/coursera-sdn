'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from mininet.topo import Topo

class CustomTopo(Topo):
    "Simple Data Center Topology"

    def build_tree_topology(self, level=0):
        if level == self.host_level:
            self.host_count += 1
            host = self.addHost('h%s' % self.host_count)

            return host
            
        else:
            self.switch_count[level] += 1
            switch = self.addSwitch('%s%s' % (self.switch_prefixes[level],self.switch_count[level]))

            for i in range(0, self.fanout):
                child = self.build_tree_topology(level + 1)
                self.addLink(switch, child, **self.linkopts[level])

            return switch
        

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        tree_levels = ['core', 'aggregation', 'edge', 'host']
        num_levels = len(tree_levels)
        self.host_level = num_levels-1 # last level is of hosts
        self.host_count = 0
        self.fanout = fanout
	self.switch_prefixes = ['c','a','e']
        self.switch_count = [0, 0, 0]
	self.linkopts = [linkopts1, linkopts2, linkopts3]
    
	self.build_tree_topology()


topos = { 'custom': ( lambda: CustomTopo() ) }
