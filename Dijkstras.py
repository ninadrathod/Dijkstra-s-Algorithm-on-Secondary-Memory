#!/usr/bin/env python
# coding: utf-8

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
cimport_cntr = 0

source = 0
destination = 0
outgoing_edges = {}

node_grid = {}      # maps the node id to grid/cell id
import_flag = {}    # if import_flag[grid id] == 1 : grid data is imported into alledges and allnodes list, 
                    # else : not imported

dist_tracker = {}   # target_node: (from_node,distance)

heap = heapdict.heapdict()


# reset_global_variables() function will reset the heap and all the concerned variables for next input

def reset_gloabal_variables():
    global scntr, cimport_cntr
    global source, destination
    global outgoing_edges, node_grid, import_flag, dist_tracker
    global heap

    scntr = 0
    cimport_cntr = 0

    source = 0
    destination = 0
    
    dist_tracker = {}   
    heap.clear()


def create_dtracker(src):
    global infinity, scntr
    
    dist_tracker[src] = [src,0]
    heap[src] = 0
    for i in node_grid.keys():

        if scntr == 150:
            time.sleep(0.001)
            scntr = 0

        scntr += 1
        if i != src:
            dist_tracker[i] = [-1,infinity]

    
#------------------------------------------------------------------------------------------

# import_data() function will import all the node and edge related info from given grid/cell
# and set the value of import_flag[grid id] flag from 0 to 1
    
def import_data(grid):
    global outgoing_edges
    global source, destination
    global alledges, allnodes
    global infinity, scntr
    global heap
    
    import_flag[grid] = 1
    traverse_through = []             # list of files from which data is to be imported
    data = []                         # all data from grid
    fname = grid+".txt"
    
    
    traverse_through.append(fname)
    dirstr = grid+"/"
    isDir = os.path.isdir(dirstr)     # is the directory named by grid ID present? / did the grid file overflow?
    
    if isDir == True:
        flist = os.listdir(grid)      # dir is your directory path
        fcount = len(flist)
    else:
        fcount = 0
    
    if fcount > 0:
         for i in range(1,fcount+1):
                traverse_through.append(grid+"/"+str(i)+".txt")
    
    ## print("\nlist of files to traverse: {}\n\n".format(traverse_through))
    
    for item in traverse_through:
        f = open(item,"r")
        blist = []
        blist = f.readlines()
        for itm in blist:

            if scntr == 150:
                time.sleep(0.001)
                scntr = 0
            scntr += 1

            if itm != '------------------\n' and itm.find("??") == -1:
                ins = itm.replace('\n','')
                data.append(ins)
    
    state = 0
    
    for item in data:

        if scntr == 150:
            time.sleep(0.001)
            scntr = 0
        scntr += 1
        
        if item == '##' or item == '**' or item == '%%':
            state += 1
        
        elif state%2 == 0:
            continue
            
        else:
            #'4 6 <3.81>'
            p,q,r = item.split(" ")
            s = r.replace("<","")
            t = s.replace(">","")
            snode = int(p)
            dnode = int(q)
            elen = float(t)
            #print("({} , {}) = {}\n".format(snode,dnode,elen))
            
            sgrid = node_grid[snode]
            dgrid = node_grid[dnode]
            if [dnode,elen] not in outgoing_edges[snode]:
                outgoing_edges[snode].append([dnode,elen])
            
    
#------------------------------------------------------------------------------------------

# This function will update the nearest distance in the heap dictionary
# with respect to the input node

def udictionary_wrt(nodeid):
    global outgoing_edges, scntr
    global cimport_cntr
    
    igrid = node_grid[nodeid]
    grid_import_flag = import_flag[igrid]
    
    if grid_import_flag == 0:
        cimport_cntr = cimport_cntr+1
        import_data(igrid) 

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
    ## print("\nsource = {}\ndestination = {}\n\n".format(src,dst))
    create_dtracker(src)
    
    while len(heap) > 0:
        tvar = heap.peekitem()
        if tvar[0] == destination:
            break
        ## print("In consideration: node {}".format(tvar[0]))
        udictionary_wrt(tvar[0])
        ## print("\nPopping: {}\n------------------------\n".format(tvar[0]))
        
        
        heap.popitem()
        
 
#------------------------------------------------------------------------------------------

def main2():
    
    global node_grid
    global import_flag
    global outgoing_edges, cimport_cntr

    steps = 0
    lst = []
    
    # This part of code will map the node_id to its respective grid/cell id as per data given in 'node_grid.txt'
    # This file is created when you partition the file using gridGraph.py script
    
    nfile = open("node_grid.txt","r")
    lst = nfile.readlines()             # lst serves as a temporary list to import data from 'node_grid.txt' file
    nfile.close()
    
    for item in lst:
        q = item.replace('\n','')
        a,grid = q.split(",")
        nid = int(a)
        node_grid[nid] = grid
        outgoing_edges[nid] = []
        
    
    ## print("node : grid ---> {}".format(node_grid))
    
    # This part of code will set the import_flag[grid_id] = 0 for all the grid ids
    # Which means that data from none of the grids is yet imported
    # 'grid_list.txt' file contains the list of all the grid_ids
    # This file is created when you partition the file using gridGraph.py script
    
    nfile = open("grid_list.txt","r")
    lst = nfile.readlines()             # lst serves as a temporary list to import data from 'grid_list.txt' file
    nfile.close()
    
    for item in lst:
        q = item.replace('\n','')
        import_flag[q] = 0
    
    ## print("\ngrid import status ---> {}\n".format(import_flag))
    
    #-----------

    flag = True
    while flag:

        inp = input("\nEnter source,destination nodes: ")
        a,b = inp.split(",")
        src = int(a)
        dst = int(b)

        if src in node_grid.keys() and dst in node_grid.keys():
            dijkstra(src,dst)
        
            #-------
            
            ## print("\nCreated dist_tacker : {}".format(dist_tracker))
            
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

            print("\nNumber of cells imported: {}".format(cimport_cntr))
        
        ## import_data("0_0")   # import_data function is called here for testing purpose. Comment it later
        ## import_data("0_1")   # import_data function is called here for testing purpose. Comment it later
        
        ## print("\ngrid import status ---> {}\n".format(import_flag))   # For testing purpose. Comment it later

        else:
            print("\nEnter valid source and destination nodeIDs")

        print("\n-------------------------------------------\n")
        num = int(input("Press 1 if you want to continue: "))
        if num != 1:
            print("Thank you. Have a nice day!")
            flag = False
        else:
            reset_gloabal_variables()


if __name__ == '__main__':
    main2()
