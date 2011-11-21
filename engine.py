#!/usr/bin/env python

"""
Ruaridh Thomson
s0786036

Practical 4 - Link Analysis
"""

import string
from math import sqrt, pow

LAMBDA = 0.8
ITER_PR = 10
ITER_HITS = 9

class Node(object):
  def __init__(self, name, dest_nodes=None, source_nodes=None):
    self.name         = name
    self.dest_nodes   = dest_nodes
    self.source_nodes = source_nodes
    
    if not self.dest_nodes:
      self.dest_nodes = []
      
    if not self.source_nodes:
      self.source_nodes = []
    
  def getNumNodes(self):
    return len(self.dest_nodes)
  
  def getNumSource(self):
    return len(self.source_nodes)

class Analyser(object):
  def __init__(self, nodes_dict, nodes_num=None):
    self.nodes_dict = nodes_dict
    self.nodes_num  = len(self.nodes_dict)
    
  def _dictTopTen(self, d):
    items = [(v, k) for k, v in d.items()]
    items.sort()
    items.reverse()
    out = items[:10] #top ten
    return out
    
  def _writeOut(self, d, f_name):
    outList = self._dictTopTen(d)
    
    f = open(f_name, 'w')
    for line in outList:
      f.write(str( round(line[0],8) ) + " " + str(line[1]) + "\n")
    f.close()
    
    print ">>> Top 10 written to: ", f_name
  
  def _normalise(self,vector):
    sum = reduce(lambda s,el: s+el,vector.values())
    # incase sum is 0
    if not sum:
      sum = 1
    return dict([(u,float(c)/sum) for (u,c) in vector.items( )])
  
  def pagerank(self):
    print ">>> Starting PageRank..."
    # init pr_t and pr_t1 as dicts
    pr_t = {}
    # populate initial pr
    for node in self.nodes_dict: pr_t[node] = 1.0 / self.nodes_num

    # (1-lambda)/N
    pre_sum = (1.0 - LAMBDA)/self.nodes_num
    
    for i in xrange(ITER_PR):
      print ">>> Calculating iteration ", i, "..."
      pr_t1 = {}
      
      for node_x_name in self.nodes_dict:
        node_x = self.nodes_dict[node_x_name]
        pr_x = pre_sum
        
        sum_y = 0.0
        for node_y_name in node_x.source_nodes:
          node_y = self.nodes_dict[node_y_name]
          # If y doesn't point to x then move on to next y
          if (node_x_name in node_y.dest_nodes):
            pr_y = pr_t.get(node_y_name)
            out_y = node_y.getNumNodes()
          
            sum_y += pr_y/(out_y*1.0) # *1.0 to get float
          else:
            print "Node x not in node y dests"
        
        # if no nodes point to x then sum_y will be 0 and pr_x will be (1-lambda)/N
        pr_x += (LAMBDA*sum_y)
        pr_t1[node_x_name] = pr_x
      
      #pr_t = dict(pr_t1)
      pr_t = self._normalise(pr_t1)
    
    self._writeOut(pr_t, 'pr.txt')
  
  def hubs_auth(self):
    print ">>> Starting Hubs and Authorities..."
    hub = {}
    auth = {}
    
    # populate initial hubs and authorities
    for node in self.nodes_dict: 
      hub[node] = 1.0
      auth[node] = 1.0
    
    for i in xrange(ITER_HITS):
      print ">>> Calculating iteration ", i, "..."
      
      # update hubs
      norm = 0.0
      for node_x_name in self.nodes_dict:
        hub[node_x_name] = 0.0
        node_x = self.nodes_dict[node_x_name]
        
        for node_y_name in node_x.dest_nodes:
          hub[node_x_name] += auth[node_y_name]
        
        norm += pow(hub[node_x_name],2) #hub[node_x_name]*hub[node_x_name]
      norm = sqrt(norm)
      
      # normalise hubs
      for node_name in self.nodes_dict:
        hub[node_name] = hub[node_name]/norm
      
      # update authorities
      norm = 0.0
      for node_x_name in self.nodes_dict:
        auth[node_x_name] = 0.0
        node_x = self.nodes_dict[node_x_name]
        
        for node_y_name in node_x.source_nodes:
          auth[node_x_name] += hub[node_y_name]
        
        norm += pow(auth[node_x_name],2) #auth[node_x_name]*auth[node_x_name]
      norm = sqrt(norm)
      
      # normalise auths
      for node_name in self.nodes_dict:
        auth[node_name] = auth[node_name]/norm
    
    self._writeOut(hub, 'hubs.txt')
    self._writeOut(auth, 'auth.txt')
    
def graphAsNodes(edges):
  print ">>> Building nodes..."
  nodes = {}
  
  for ed in edges:
    n_from = ed[0]
    n_to = ed[1]
    
    # populate edges pointing from nodes
    if not nodes.has_key(n_from):
      nodes[n_from] = Node(n_from,[n_to])
    else:
      nodes[n_from].dest_nodes.append(n_to)
    
    if not nodes.has_key(n_to):
      nodes[n_to] = Node(n_to)
    
    # populate edges pointing to nodes
    if not nodes.has_key(n_to):
      nodes[n_to] = Node(n_to,[],[n_from])
    else:
      nodes[n_to].source_nodes.append(n_from)
      
    if not nodes.has_key(n_from):
      nodes[n_from] = Node(n_from)
  
  return nodes

def getGraphEdges():
  print ">>> Loading graph.txt..."
  graph = []
  
  f = open('graph.txt','r')
  lines = f.readlines()
  
  for line in lines:
    # 0=IDs 1=emailer 2=emailee
    lineSplit = string.split(line)
    
    # If the sender is emailing himself we should ignore
    if (lineSplit[1] == lineSplit[2]):
      continue
    
    graph.append( (lineSplit[1],lineSplit[2]) )
  f.close()
  
  return graph
  
def getPeople():
  print ">>> Loading graph.txt..."
  graph = []
  peeps = []
  dupes = []
  
  # Read 10-20 important people
  f = open('im_people.txt','r')
  lines = f.readlines()
  for line in lines:
    l = string.split(line)
    peeps.append(l[0])
  f.close()
  
  # Read whole graph.txt
  f = open('graph.txt','r')
  lines = f.readlines()
  for line in lines:
    lineSplit = string.split(line)
    p1 = lineSplit[1]
    p2 = lineSplit[2]
    # only add contact between important people
    if (p1 in peeps):
      if (p2 in peeps):
        graph.append( (p1,p2) )
  f.close()
  
  # reduce duplicates and count them
  set_graph = list(set(graph))
  for link in set_graph:
    dupes.append(graph.count(link))
  
  # write to graph.dot to render
  print ">>> Writing smaller graph"
  f = open('graph.dot','w')
  f.write("digraph G { \n")
  for i in xrange(len(set_graph)):
    (a,b) = set_graph[i]
    a = a.replace('@enron.com','')
    b = b.replace('@enron.com','')
    out = "  \"" + a + "\" -> \"" + b + "\" [label = \"" + str(dupes[i]) + "\"]; " + "\n"
    f.write(out)
  f.write("}")
  f.close()
  print ">>> Done preparing graph.dot"

def main():
  print ">>> Beginning Link Analysis"
  
  getPeople()
  
  """
  edges = getGraphEdges()
  nodes = graphAsNodes(edges)
  
  anna = Analyser(nodes)
  anna.pagerank()
  anna.hubs_auth()
  """
  print ">>> Goodbye."

if __name__ == "__main__":
  main()