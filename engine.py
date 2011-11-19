#!/usr/bin/env python

"""
Ruaridh Thomson
s0786036

Practical 4 - Link Analysis
"""

import re
import math
import time
import string

LAMBDA = 0.8
ITERATIONS = 10 #should be 10

class PageRank(object):
  def __init__(self):
    self.graph       = [] # This may just be a waste of memory...
    self.senders     = []
    self.receivers   = []
    self.uniqueNodes = []
    self.uLen        = 0  # this is N and is used many times
    self.pr_t        = []
    self.pr_t1       = []
    
  def writeOut(self):
    f = open('pr.txt','w')
    for rank in self.allRanks:
      f.write(rank + "\n")
    f.close()
    print ">>> Top 10 PageRanks written to: pr.txt"
    
  def _loadGraph(self):
    print ">>> Loading graph.txt..."
    f = open('graph.txt','r')
    lines = f.readlines()
    for line in lines:
      # 0=IDs 1=emailer 2=emailee
      lineSplit = string.split(line)
      
      # If the sender is emailing himself we should ignore
      if (lineSplit[1] == lineSplit[2]):
        continue
      
      self.graph.append(lineSplit) # populate graph.txt to array
      self.senders.append(lineSplit[1]) # populate senders
      self.receivers.append(lineSplit[2]) # populate receivers
      
      # Do we count emailees in the node graph?
      self.uniqueNodes.append(lineSplit[1])
      self.uniqueNodes.append(lineSplit[2])
    f.close()
    
    # Remove duplicates from the unique list
    self.uniqueNodes = list(set(self.uniqueNodes))
    self.uLen = len(self.uniqueNodes)
  
  def _stats(self):
    print "Graph size: ", len(self.graph)
    print "Unique nodes: ", len(self.uniqueNodes)
    print "Num senders: ", len(self.senders)
    print "Num receivers: ", len(self.senders)
    
  # For x, return the indices in senders for all y for y->x
  def _all_indices(self, item):
    indices = []
    idx = -1
    while 1:
      try:
        idx = self.receivers.index(item,idx+1)
        indices.append(idx)
      except ValueError:
        break
    return indices
  
  def _sum_for_node(self, ni):
    s = 0.0
    inds = self._all_indices(ni)
    
    # y to follow slide notation
    # say y sends multiple emails to x, we will do this loop unneccesarily more
    for ind in inds:
      y = self.senders[ind]
      y_out = self.senders.count(y)
      pr_y = self.pr_t[self.uniqueNodes.index(y)]
      s += float(pr_y)/float(y_out)
      
    return s
  
  def _pr(self):
    one_m_lambda_n = (1.0 - LAMBDA)/self.uLen
    for node_index in range(self.uLen):
      sum_node = self._sum_for_node(node_index)
      self.pr_t1[node_index] = one_m_lambda_n + (LAMBDA*sum_node)
    self.pr_t = list(self.pr_t1)
      
  def _pr_iters(self):
    for i in range(ITERATIONS):
      print ">>> Calculating PR for iteration ", i, " ..."
      self._pr()
  
  def getRanks(self):
    self._loadGraph()
    
    self.pr_t = [1.0/self.uLen]*self.uLen
    self.pr_t1 = [1.0/self.uLen]*self.uLen #just to initialise it
    print "uLen: ", self.uLen
    self._pr()
    
    self._stats()
    

def main():
  print ">>> Beginning Link Analysis"
  
  pr = PageRank()
  pr.getRanks()
  
  print ">>> Goodbye."

if __name__ == "__main__":
  main()