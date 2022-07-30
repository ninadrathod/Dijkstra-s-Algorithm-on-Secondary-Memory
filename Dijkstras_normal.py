#!/usr/bin/env python
# coding: utf-8

# Conventional implementation of Diijkstra's algorithm

# Pre condition:
# 1. Value of infinity is considered to be 100000000 in this code.
# 2. No negative weight edges allowed
# 3. Enter the source and destination with comma separation without any space into the input.
#    example : 0,4

import heapdict
import os
import time

scntr = 0
infinity = 100000000

source = 0
destination = 0
outgoing_edges = {}

dist_tracker = {}   # target_node: (from_node,distance)

heap = heapdict.heapdict()

#------------------------------------------------------------------------------------------

# This function will update the nearest distance in the heap dictionary
# with respect to the input node

def udictionary_wrt(nodeid):
    global outgoing_edges, scntr
    global cimport_cntr
    
    tmp = outgoing_edges[nodeid]
    ## print(tmp)
    
    for itm in tmp:

        if scntr == 150:
            time.sleep(0.001)
            scntr = 0
        scntr += 1

        tar = itm[0]
        dst = itm[1]
        relaxed = heap[nodeid] + dst
        if dist_tracker[tar][1] > relaxed:
            temp = [nodeid,relaxed]
            dist_tracker[tar] = temp
            heap[tar] = relaxed
            
    ## abc = list(heap.items())  
    ## print("heap : {}\n".format(abc))

#------------------------------------------------------------------------------------------

# Running Dijktra's algorithm

def dijkstra(src,dst):
    
    global source, destination
    global outgoing_edges
    
    source = src
    destination = dst
    
    while len(heap) > 0:
        tvar = heap.peekitem()
        if tvar[0] == destination:
            break
        udictionary_wrt(tvar[0])
        heap.popitem()
        
#------------------------------------------------------------------------------------------
def main():
    global heap
    global outgoing_edges, scntr
    global source, destination, dist_tracker
    #int flag_src, flag_dst

    flag_src = 0
    flag_dst = 0

    snctr = 0

    inp = input("\nEnter source,destination nodes: ")
    a,b = inp.split(",")
    src = int(a)
    dst = int(b)

    tempFile = open('nodes.txt','r')
    allRows = tempFile.readlines()
    tempFile.close()

    node_rec = []

    #-------------Getting nodes------------------------------

    for row in allRows:

        if scntr == 150:
            time.sleep(0.001)
            scntr = 0
        scntr += 1

        x = row.replace("\n","")
        a,b,c = x.split(" ")
        nodenum = int(a)

        if (nodenum in node_rec):
            continue
        
        node_rec.append(nodenum)

        if nodenum == src:
            flag_src = 1
            heap[nodenum] = 0
            dist_tracker[nodenum] = [nodenum,0]
            if dst == src:
                flag_dst = 1
        elif nodenum == dst:
            flag_dst = 1
            dist_tracker[nodenum] = [-1,infinity]
            heap[nodenum] = infinity
        else:
            heap[nodenum] = infinity
            dist_tracker[nodenum] = [-1,infinity]

        outgoing_edges[nodenum] = []
        
    edge_info = {}
    
    if flag_src == 0 or flag_dst == 0:
        print("Invalid node entries")
    else:
        fname = open('edges.txt','r')
        edge_data = []
        edge_data = fname.readlines()
        

        #-------Fetching edge info-----------------
        for item in edge_data:
            if scntr == 150:
                time.sleep(0.001)
                scntr = 0
            scntr += 1

            tp = item.replace("\n","")
            a,b,c = tp.split(" ")
            snode = int(a)
            enode = int(b)
            elen = float(c)

            ewo = a+"-"+b
            if (ewo in edge_info.keys()):
                continue
            
            edge_info[ewo] = elen
            outgoing_edges[snode].append([enode,elen])

        dijkstra(src,dst)
        if dist_tracker[dst][1] < 100000000:
            steps = 0
            ans_list = []
            ans_list.append(dst)
            path = dist_tracker[dst][0]
            while path != src:
                ans_list.append(path)
                path = dist_tracker[path][0]
                steps+=1

            ans_list.append(path)
            print("\nDistance from {} to {} = {}\nNumber of steps from source to destnation: {}".format(src,dst,dist_tracker[dst][1],steps+1))
            print("Path from source to destination: ")
            print(ans_list[::-1])
        else:
            print("\nNo path from {} to {}\n".format(src,dst))
        
            

if __name__ == '__main__':
    main()
