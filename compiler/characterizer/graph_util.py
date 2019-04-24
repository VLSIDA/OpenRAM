import os
from collections import defaultdict

import gdsMill
import tech
import math
import globals
import debug
from vector import vector
from pin_layout import pin_layout

class graph():
    """Implements a directed graph"""
    
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        """Adds edge to graph. Nodes added as well if they do not exist."""
        if v not in self.graph[u]:
            self.graph[u].append(v)

    def add_node(self, u):
        """Add node to graph with no edges"""
        if not u in self.graph:
            self.graph[u] = []
            
    def remove_edges(self, node):
        """Helper function to remove edges, useful for removing vdd/gnd"""
        self.graph[node] = []    
            
    def printAllPaths(self,s, d): 
  
        # Mark all the vertices as not visited 
        visited = set()
  
        # Create an array to store paths 
        path = [] 
        self.path_count = 0
  
        # Call the recursive helper function to print all paths 
        self.printAllPathsUtil(s, d,visited, path)     
        debug.info(1, "Paths found={}".format(self.path_count))
            
    def printAllPathsUtil(self, u, d, visited, path): 
  
        # Mark the current node as visited and store in path 
        visited.add(u)
        path.append(u) 
  
        # If current vertex is same as destination, then print 
        # current path[] 
        if u == d: 
            debug.info(1,"{}".format(path)) 
            self.path_count+=1
        else: 
            # If current vertex is not destination 
            #Recur for all the vertices adjacent to this vertex 
            for i in self.graph[u]: 
                if i not in visited: 
                    self.printAllPathsUtil(i, d, visited, path) 
                      
        # Remove current vertex from path[] and mark it as unvisited 
        path.pop() 
        visited.remove(u)        
            
    def __str__(self):
        """ override print function output """
        return "Nodes: {}\nEdges:{} ".format(list(self.graph), self.graph)  