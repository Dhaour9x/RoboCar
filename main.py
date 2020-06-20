#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:54:34 2019

@author: marvin_burges
"""


#import conti_sign_and_roadblock_detection.sign_and_roadblock_detection as sign
import conti_image_to_graph.image_to_graph as I2G
import conti_robot_control.robot_control as RC
import numpy as np
from math import atan2
import sys
sys.path.append('/home/pi/Conti_S2F/')

from conti_path_planning.graph import Graph
'''
def standard_procedure():
    g = I2G.get_graph()
    path = g.shortest_path()

    while True:
        RC.follow_path()    # drive forward; automatically breaks when it's on a node
        
        path.advance()
        if path.current_node() == g.finish_node:
            break

        dir = path.get_direction()
        RC.turn_to_direction(dir) # rotate robot from current to target direction
        
'''

def standard_procedure(path, graph):
    path.advance()
    for i in range(len(path.nodes)-1):
        print (path.get_direction())
        print ("currentNumber: " + str(path.nodes[0].number))
        RC.turn_to_direction(path.get_direction())
        while(True):
            if RC.check_if_turned():
                break
        surrounding = "test" #sign.check_surroundings()
        if surrounding == "roadblock":
            newgraph = I2G.deletLineFromGraph(graph, path.nodes[0].number, path.nodes[1].number)
            newgraph.current_node = path.nodes[0]
            path = newgraph.shortest_path()
        elif surrounding == "stopsign":
            RC.set_stopsign()
        path.advance()
        if len(path.nodes) == 1:
            RC.finish()
            break
        else:
            RC.drive_straight()
            while(True):
                if RC.check_if_on_a_node():
                    break
        
        

if __name__ == "__main__":
    graph = I2G.get_graph(sys.argv[1])
    path = graph.shortest_path()
    standard_procedure(path, graph)
   
        
        
        
        
    
