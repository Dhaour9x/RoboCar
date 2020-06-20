#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

class Node:
    def __init__(self, north=None, east=None, south=None, west=None,number=0):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.number = number
        self.coordinates = np.array([0,0])

        if self.north is not None:
            self.north.south = self
        if self.east is not None:
            self.east.west = self 
        if self.south is not None:
            self.south.north = self
        if self.west is not None:
            self.west.east = self

    def get_neighbours(self):
        return [self.north, self.east, self.south, self.west]
    
    def insertNodes(self, north=None, east=None, south=None, west=None):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

class Path:
    def __init__(self, nodes):
        self.nodes = nodes
    
    def get_direction(self):
        dir = self.nodes[0].coordinates - self.nodes[1].coordinates
        if np.array_equal(dir,np.array([0,1])):
            return 0
        if np.array_equal(dir,np.array([1,0])):
            return 1
        if np.array_equal(dir,np.array([0,-1])):
            return 2
        if np.array_equal(dir,np.array([-1,0])):
            return 3
    
    def check_for_longer_straight(self):
        counter = 0
        while(True):
            if counter == len(self.nodes)-2:
                break
            if len([n for n in self.nodes[counter+1].get_neighbours() if n is not None])==2 and np.array_equal(self.nodes[counter].coordinates - self.nodes[counter+1].coordinates, self.nodes[counter+1].coordinates - self.nodes[counter+2].coordinates):
                counter += 1
            else:
                break
        return counter+1
    
    def advance(self):
        nodes_count = self.check_for_longer_straight()
        self.nodes = self.nodes[nodes_count:]

    def current_node(self):
        return self.nodes[0]
    
    def next_node(self):
        return self.nodes[1]
        
class Graph:
    def __init__(self, current_node : Node, finish_node : Node):
        self.current_node = current_node
        self.finish_node = finish_node
        self.__calculate_coordinates()

    def iter_recursively(self, fct):
        visited = set({})
        stack = [self.current_node]
        while len(stack) > 0:
            top = stack.pop()
            visited.add(top)
            for i,n in enumerate(top.get_neighbours()):
                if n is None or n in visited:
                    continue
                stack.append(n)
                fct(top,i,n)
    
    def __calculate_coordinates(self):
        def __iter(top, i, n):
            offset = np.array([0,0])
            if i==0:
                offset = np.array([0,1])
            if i==1:
                offset = np.array([1,0])
            if i==2:
                offset = np.array([0,-1])
            if i==3:
                offset = np.array([-1,0])
            n.coordinates = top.coordinates + offset 

        self.iter_recursively(__iter)

    def shortest_path(self):
        '''
        returns a list of Nodes [start,next,...,finish]
        '''
        # nodes are equidistant so simple breadth first search is enough
        queue = [ self.current_node ]
        visited = set({})
        parents = {}

        found_finish = False

        while len(queue) > 0 or not found_finish:
            first = queue[0]

            if first is self.finish_node:
                found_finish = True
                break

            queue = queue[1:]
            visited.add(first)
            
            for n in first.get_neighbours():
                if n is None or n in visited:
                    continue
                parents[n] = first
                queue.append(n)

        if not found_finish:
            print("cannot find the finish")
            return None
        
        cur = self.finish_node
        ret = [cur]
        while cur in parents:
            cur = parents[cur]
            ret.insert(0,cur)
        # print(ret)
        return Path(ret)

    def display_path(self, path):
        connections = []
        for i in range(len(path.nodes)-1):
            connections.append( [ path.nodes[i].coordinates, path.nodes[i+1].coordinates])
        lc = mc.LineCollection(connections, linewidths=2)
        self.__display_lines(lc)


    def display(self):
        # depth-first search
        stack = [ self.current_node ]
        visited = set({})
        connections = []

        while len(stack) > 0:
            top = stack.pop()
            visited.add(top)
            for n in top.get_neighbours():
                if n is None or n in visited:
                    continue
                stack.append(n)
                connections.append( [n.coordinates, top.coordinates] )
        
        lc = mc.LineCollection(connections, linewidths=2)
        # plt.plot(self.current_node.coordinates[0],self.current_node.coordinates[1],"g*")
        # plt.plot(self.finish_node.coordinates[0], self.finish_node.coordinates[1],"r*")
        self.__display_lines(lc)
        
    
    def __display_lines(self, line_collection : mc.LineCollection):
        _, ax = plt.subplots()
        ax.add_collection(line_collection)
        ax.set_xlim(-10,10)
        ax.set_ylim(-10,10)
        plt.axis("equal")
        ax.margins(0.1)
        plt.show()

if __name__ == "__main__":
    b = Node()
    c = Node()
    d = Node()
    a = Node( north=Node( north=Node(west=b, east=Node(north=Node()))))
    g = Graph(a,b)
    # g.display_path( g.shortest_path() )
    g.display()
