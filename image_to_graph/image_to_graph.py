#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import cv2
sys.path.append('/home/pi/Conti_S2F/conti_path_planning')

#sys.path.append('../conti_image_to_graph')
from graph import Graph, Node
import numpy as np

imgCounter = 1

class graphList():
    def __init__(self,start=0,finish=0):
        self.start = start
        self.finish = finish
        self.nodes = []
        self.coord = []


def graphList_to_Graph(gl : graphList):
    return Graph(gl.nodes[gl.start], gl.nodes[gl.finish])


def printNode(g1,nmb):
    print(g1.nodes[nmb].north,g1.nodes[nmb].east,g1.nodes[nmb].south,g1.nodes[nmb].west)


def printGraph(filename,g1):
    # Read png
    imgIN = cv2.imread(filename,1)


    # Rescale
    scal_factor = 4
    img2 = cv2.resize(imgIN, (0,0), fx=scal_factor, fy=scal_factor) 

    # Write some Text
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 0.8
    fontColor              = (255,0,0)
    lineType               = 2

    # Print Text next to each node with number
    for idx,ii in enumerate(g1.coord):
        cv2.putText(img2,str(idx), 
            (ii[1]*scal_factor,ii[0]*scal_factor), 
            font, 
            fontScale,
            fontColor,
            lineType)

        # Indicate connection

        for nn in range(0,4):
            if g1.nodes[idx].north != None:
                cv2.circle(img2, 
                    (ii[1]*scal_factor,ii[0]*scal_factor - 7*scal_factor), 
                    8, 
                    (255,0,0), 
                    thickness=3, 
                    lineType=8, 
                    shift=0)
            if g1.nodes[idx].east != None:
                cv2.circle(img2, 
                    (ii[1]*scal_factor + 7*scal_factor,ii[0]*scal_factor), 
                    8, 
                    (255,0,0), 
                    thickness=3, 
                    lineType=8, 
                    shift=0)
            if g1.nodes[idx].south != None:
                cv2.circle(img2, 
                    (ii[1]*scal_factor,ii[0]*scal_factor + 7*scal_factor), 
                    4, 
                    (255,255,0), 
                    thickness=3, 
                    lineType=8, 
                    shift=0)
            if g1.nodes[idx].west != None:
                cv2.circle(img2, 
                    (ii[1]*scal_factor - 7*scal_factor,ii[0]*scal_factor), 
                    4, 
                    (255,255,0), 
                    thickness=3, 
                    lineType=8, 
                    shift=0)

    #cv2.imshow("img2",img2)
    string2 = "".join(['C:/Users/ThomasH/Desktop/Hackathon/img/out/',str(imgCounter),'_out.png'])
    cv2.imwrite(string2, img2)





######################################################################################
# MAIN FUNCTIONALITY
######################################################################################
def get_graphList(filename='C:/Users/ThomasH/Desktop/demo.png',debugMode=0):
    '''Calculates a graph from a maze png input'''
    
    print ("PATH_TO_IMAGE: " + filename)
    img = cv2.imread(filename,1)
    

    # Build graph
    g1 = graphList()

    # Find start position (search red dot)
    raster_start = 0
    red_start = 0
    redCol = np.array([0,0,255])
    for r_idx,row in enumerate(img):
        for c_idx,px in enumerate(row):
            if (px == redCol).all():
                raster_start = (r_idx+17,c_idx+2)
                red_start = (r_idx+3,c_idx+2)
                break
        else:
            continue
        break
    #TODO break2

    # Find end position (search green dot)
    green_start = 0
    raster_end = 0
    greenCol = np.array([0,255,0])


    #down = img[-20:]
    #cv2.imshow('img',down)
    start_from_bottom = -20
    for r_idx,row in enumerate(img[start_from_bottom:]):
        for c_idx,px in enumerate(row):
            if (px == greenCol).all():
                raster_end = (r_idx+img.shape[0]+start_from_bottom-12,c_idx+2)
                green_start = (r_idx+img.shape[0]+start_from_bottom+3,c_idx+2)
                break
        else:
            continue
        break

    # Calculate border
    #border = 0
    #for r_idx,col in enumerate(img.T):
        #for val in enumerate(col): 
        

    # Calculate pattern (where all possible notes exist)
    raster_top_left = (raster_start[0], raster_start[1] % 14)
    raster_botom_right = (raster_end[0]+1, img.shape[1]-raster_top_left[1]-2) # right&Left same border(-2)
    if debugMode == 1:
        print('Top left:    ', raster_top_left)
        print('Bottom right:', raster_botom_right)
    raster_width = int((raster_botom_right[1] - raster_top_left[1]) / 14 + 1)
    raster_height = int((raster_botom_right[0] - raster_top_left[0]) / 14 + 1)

    # Create all Nodes (still without connection)
    g1.nodes = [Node() for ii in range(raster_width*raster_height + 2)] # +2 for start and finish

    if debugMode == 1:
        g1.coord = [0 for ii in range(raster_width*raster_height + 2)]

    # Find all nods
    black = np.array([0,0,0])
    gray = np.array([30,30,30])
    node_couter = 0
    # loop rows
    for aa in range(raster_top_left[0],raster_botom_right[0]+14,14):
        #loop columns
        for bb in range(raster_top_left[1],raster_botom_right[1]+14,14):

            # Is here a dot? = normaly there should be - who knows finals maze...
            if  1:# not all are black !!!(img[aa,bb] == black).all():
                # Find connections
                # Add node to graph
                north = None
                east = None
                south = None
                west = None

                if aa > raster_top_left[0]:
                    if (img[aa-7,bb] < gray).all(): north = node_couter - raster_width
                if bb < raster_botom_right[1]:
                    if (img[aa,bb+7] < gray).all(): east = node_couter + 1
                if aa < raster_botom_right[0]:
                    if (img[aa+7,bb] < gray).all(): south = node_couter + raster_width
                if bb > raster_top_left[1]:
                    if (img[aa,bb-7] < gray).all(): west = node_couter - 1

                if 0:
                    print(node_couter)
                    print('\t',img[aa-7,bb],img[aa,bb+7],img[aa+7,bb],img[aa,bb-7])
                    print('\t',north,east,south,west)

                # Get Node objects
                north_Node = None if north == None else g1.nodes[north]
                east_Node = None if east == None else g1.nodes[east]
                south_Node= None if south== None else g1.nodes[south]
                west_Node = None if west == None else g1.nodes[west]

                g1.nodes[node_couter].insertNodes(north_Node,east_Node,south_Node,west_Node)
                g1.nodes[node_couter].number = node_couter

                if debugMode == 1:
                    g1.coord[node_couter] = (aa,bb)

                node_couter += 1

    # Add start(only south) and finish(only north)
    south = int((red_start[1] - raster_top_left[1]) / 14)
    north = len(g1.nodes) - raster_width + int((green_start[1] - raster_top_left[1]) / 14) - 2 #-2 start&finish

    # START NODE
    g1.nodes[node_couter].insertNodes(None,None,g1.nodes[south],None)
    g1.nodes[node_couter].number = node_couter
    g1.start = len(g1.nodes) - 2 # Mark start node
    node_couter += 1

    # FINISH NODE
    g1.nodes[node_couter].insertNodes(g1.nodes[north],None,None,None)
    g1.nodes[node_couter].number = node_couter
    g1.finish = len(g1.nodes) - 1 # Mark finish node

    # ADD lost connections to start and finish
    g1.nodes[south].north = g1.nodes[len(g1.nodes) - 2] # Add start to node in path
    g1.nodes[north].south = g1.nodes[len(g1.nodes) - 1] # Add start to node in path

    if debugMode == 1:
        g1.coord[len(g1.nodes) - 2] = red_start
        g1.coord[len(g1.nodes) - 1] = green_start

        printGraph(filename,g1)
    return g1


def deletLineFromGraph(g1,number1,number2):
    '''One connection between 2 nodes is deleted'''

    # e.g. 30.est and 31.west are now None
    if g1.nodes[number1].east != None and g1.nodes[number1].east.number == number2:
        g1.nodes[number1].east = None
        g1.nodes[number2].west = None
    
    if g1.nodes[number1].south != None and g1.nodes[number1].south.number == number2:
        g1.nodes[number1].south = None
        g1.nodes[number2].north = None
    
    if g1.nodes[number1].west != None and g1.nodes[number1].west.number == number2:
        g1.nodes[number1].west = None
        g1.nodes[number2].east = None
    
    if g1.nodes[number1].north != None and g1.nodes[number1].north.number == number2:
        g1.nodes[number1].north = None
        g1.nodes[number2].south = None

    return g1

def get_graph(filename="conti_image_to_graph/demo.png"):
    gl = get_graphList(filename)
    g = graphList_to_Graph(gl)
    return g

# tests
if 0:
    imgCounter = 201
    #get_graphList('C:/Users/ThomasH/Desktop/Hackathon/img/101.png',debugMode=1)

    if 0:
        for ii in range(1,101):
            string1 = "".join(['C:/Users/ThomasH/Desktop/Hackathon/img/',str(imgCounter),'.png'])
            get_graphList(string1,debugMode=1)
            print('grafic',ii,'ready')
            imgCounter += 1
    
if __name__=="__main__":
    gl = get_graphList()
    # New start: gl.start = 56
    # Delte connection: gl = deletLineFromGraph(gl,72,81)
    g = graphList_to_Graph(gl)
    erg = g.shortest_path()
    g.display_path( g.shortest_path() )
