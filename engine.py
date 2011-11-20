#!/usr/bin/env python

"""
Ruaridh Thomson
s0786036

Practical 4 - Link Analysis
"""

import string

LAMBDA = 0.8
ITERATIONS = 10

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

class PageRank(object):
  def __init__(self, nodes_dict, nodes_num = None):
    self.nodes_dict = nodes_dict
    self.nodes_num  = len(self.nodes_dict)
    
  def writeOut(self):
    f = open('pr.txt','w')
    for rank in self.allRanks:
      f.write(rank + "\n")
    f.close()
    print ">>> Top 10 PageRanks written to: pr.txt"
  
  def normalise(self,vector):
    sum = reduce(lambda s,el: s+el,vector.values())
    # incase sum is 0
    if not sum:
      sum = 1
    return dict([(u,float(c)/sum) for (u,c) in vector.items( )])
  
  def rank(self):
    print ">>> Beginning PageRank..."
    # init pr_t and pr_t1 as dicts
    pr_t = {}
    # populate initial pr
    for n_name in self.nodes_dict: pr_t[n_name] = 1.0 / self.nodes_num

    # (1-lambda)/N
    pre_sum = (1.0 - LAMBDA)/self.nodes_num
    
    for i in xrange(ITERATIONS):
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
      pr_t = self.normalise(pr_t1)
      print pr_t.get('jeff.dasovich@enron.com')
    
    return pr_t
    
def graphAsNodes(edges):
  print ">>> Loading graph.txt..."
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


def main():
  print ">>> Beginning Link Analysis"
  
  edges = getGraphEdges()
  nodes = graphAsNodes(edges)
  
  page = PageRank(nodes)
  page.rank()
  
  print ">>> Goodbye."

if __name__ == "__main__":
  main()