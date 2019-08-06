import os, copy
from collections import defaultdict

import gdsMill
import tech
import math
import globals
import debug
from vector import vector
from pin_layout import pin_layout
    
class timing_graph():
    """
    Implements a directed graph
    Nodes are currently just Strings.
    """
    
    def __init__(self):
        self.graph = defaultdict(set)
        self.all_paths = []

    def add_edge(self, src_node, dest_node):
        """Adds edge to graph. Nodes added as well if they do not exist."""
        
        src_node = src_node.lower()
        dest_node = dest_node.lower()
        self.graph[src_node].add(dest_node)

    def add_node(self, node):
        """Add node to graph with no edges"""
        
        node = node.lower()
        if not node in self.graph:
            self.graph[node] = set()
            
    def remove_edges(self, node):
        
        """Helper function to remove edges, useful for removing vdd/gnd"""
        node = node.lower()
        self.graph[node] = set()    
            
    def get_all_paths(self, src_node, dest_node, remove_rail_nodes=True, reduce_paths=True): 
        """Traverse all paths from source to destination"""
        
        src_node = src_node.lower()
        dest_node = dest_node.lower()
        
        # Remove vdd and gnd by default
        # Will require edits if separate supplies are implemented.
        if remove_rail_nodes:
            # Names are also assumed.
            self.remove_edges('vdd')
            self.remove_edges('gnd')
        
        # Mark all the vertices as not visited 
        visited = set()
  
        # Create an array to store paths 
        path = [] 
        self.all_paths = []
  
        # Call the recursive helper function to print all paths 
        self.get_all_paths_util(src_node, dest_node, visited, path)     
        debug.info(2, "Paths found={}".format(len(self.all_paths)))

        if reduce_paths:
            self.reduce_paths()
        
        return self.all_paths     

    def reduce_paths(self):
        """ Remove any path that is a subset of another path """
        
        self.all_paths = [p1 for p1 in self.all_paths if not any(set(p1)<=set(p2) for p2 in self.all_paths if p1 is not p2)]
            
    def get_all_paths_util(self, cur_node, dest_node, visited, path): 
        """Recursive function to find all paths in a Depth First Search manner"""
        
        # Mark the current node as visited and store in path 
        visited.add(cur_node)
        path.append(cur_node) 
  
        # If current vertex is same as destination, then print 
        # current path[] 
        if cur_node == dest_node: 
            self.all_paths.append(copy.deepcopy(path))
        else: 
            # If current vertex is not destination 
            # Recur for all the vertices adjacent to this vertex 
            for node in self.graph[cur_node]: 
                if node not in visited: 
                    self.get_all_paths_util(node, dest_node, visited, path) 
                      
        # Remove current vertex from path[] and mark it as unvisited 
        path.pop() 
        visited.remove(cur_node)        
            
    def __str__(self):
        """ override print function output """

        return "Nodes: {}\nEdges:{} ".format(list(self.graph), self.graph)  
