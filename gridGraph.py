#!/usr/bin/env python
# coding: utf-8
#new code

import os
import time

counter = 0
grid_count = 0
grid_overflow = {}
node_grid = {}
allNodes = []               # Node details are stored in allNodes list as node_id int, x-coordiante float, y-coordinate float 
node_coord = {}


xmx = 0
ymx = 0
xmn = 0
ymn = 0
gdim = 0
#========fincord() function will help fetch the coordinates of resp node and save it to a dictionary=========

def fincoord(nodeid):
    global allNodes
    global node_coord
    for item in allNodes:
        if item[0] == nodeid:
            x = item[1]
            y = item[2]
            node_coord[nodeid] = [x,y]
            break
    return x,y

#=============================append special characters at end of files=======================================

def append_special_chars(string):
    for itm in grid_overflow.keys():
        fname = grid_overflow[itm][1]
        nfile = open(fname,'a')
        nfile.write(string+"\n")
        nfile.close()
        time.sleep(0.001)

#=====================================Creating a grid text file===============================================

def create_grid(gridname):
    global grid_overflow
    global grid_count
    global counter
    fptr = open(gridname+".txt",'w')
    fptr.write("------------------\n")
    fptr.close()
    grid_overflow[gridname] = [0,gridname+".txt"]
    grid_count += 1
    counter += 1
    
#create_grid("0_1.txt")
#print(grid_overflow)

#===================insert_record() function will enter our records into concerned file=======================

def insert_record(data,gridname,m):
    temp = grid_overflow[gridname]
    global counter
    #global m
    #print("{}\n{}".format(temp[0],temp[1]))
    if temp[0] == m:
        if temp[1].find("/") == -1:
            # if the first file in the bucket overflows
            name,extension = temp[1].split(".")
            os.mkdir(name)
            filename = name+"/1.txt"
            new_file = open(filename,'w+')
            metadata = "?? "+gridname+".txt\n"
            new_file.write("{}".format(metadata))
            new_file.write(data+"\n")
            new_file.close()
            prev = open(temp[1],'a')
            prev.write("?? "+filename+"\n")
            prev.close()
            grid_overflow[gridname] = [1,filename]
        else:
            # if an extension file of the bucket overflows
            directory,remainder = temp[1].split("/")
            name,extension = remainder.split(".")
            file = int(name)
            file += 1
            filename = directory+"/"+str(file)+".txt"
            new_file = open(filename,'w+')
            metadata = "?? "+gridname+".txt\n"
            new_file.write("{}".format(metadata))
            new_file.write(data+"\n")
            new_file.close()
            prev = open(temp[1],'a')
            prev.write("?? "+filename+"\n")
            prev.close()
            grid_overflow[gridname] = [1,filename]
        counter += 1
    else:
        new_file = open(temp[1],'a')
        new_file.write(data+"\n")
        new_file.close()
        cntr = temp[0]
        cntr += 1
        fname = temp[1]
        grid_overflow[gridname] = [cntr,fname]

#============================================Main Code========================================================

def coord_cell_mapping(m,n):
        
        global xmx, ymx, xmn, ymn, gdim
        k = gdim
        x_min = xmn
        y_min = ymn
        x_max = xmx
        y_max = ymx
        
        if m < x_min or m > x_max or n > y_max or n < y_min:
            print("Out of Bounds\n")
        else:
            i=0
            hor = x_min
            while hor != x_max:
                if (m > hor and m <= (hor+k)) or (m == x_min):
                    break
                i = i+1
                hor = hor + k

            j=0
            ver = y_min
            while ver != y_max:
                if (n > ver and n <= (ver+k)) or (n == y_min):
                    break
                j = j+1
                ver = ver + k

            tstr = str(i)+"_"+str(j)
            print("Input node will map to cell {}\n".format(tstr))

def maincode(k,bucksize):
    global xmx, ymx, xmn, ymn, gdim
    global grid_overflow
    global node_grid
    global allNodes
    global node_coord
    
    scntr = 0
    gdim = k
    in_grid_edges = []
    inter_grid_edges = []
    allRows = []                # Input Node file is read into the allRows list line-by-line
     
    # copying all the data from input file to 'allRows' variable
    tempFile = open('nodes.txt','r')
    allRows = tempFile.readlines()
    tempFile.close()
    
    #------------------ calculate x_min, y_min, x_max, y_max-----------------------------
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0
    
    i = 1
    node_rec = []
    for row in allRows:
        
        if scntr == 150:
            time.sleep(0.001)
            scntr = 0
        scntr += 1
        
        x = row.replace("\n","")
        a,b,c = x.split(" ")
        nodenum = int(a)
        x_coordinate = float(b)
        y_coordinate = float(c)
        
        if (nodenum in node_rec):
            continue
        
        node_rec.append(nodenum)
        allNodes.append([nodenum,x_coordinate,y_coordinate])
        node_coord[nodenum] = [x_coordinate,y_coordinate]
        #print("Node{} :({},{})".format(nodenum,x_coordinate,y_coordinate))
        
        if i == 1:
            x_min = x_coordinate
            y_min = y_coordinate
            i = 100
        
        if x_coordinate > x_max:
            x_max = x_coordinate
        if x_coordinate < x_min:
            x_min = x_coordinate
        if y_coordinate > y_max:
            y_max = y_coordinate
        if y_coordinate < y_min:
            y_min = y_coordinate
         
    #print(allNodes)
    #print("x_min: {}\ny_min: {}\nx_max: {}\ny_max: {}".format(x_min,y_min,x_max,y_max))
    
    #------------------------------------Creating Grid files--------------------------------------------
    i = x_min
    j = y_min
    
    grid_xc = 0
    
    grid = []
    xaxis = []
    
    while i < x_max:
        #xyg = ""                                                        # erase if not necessary
        j = y_min
        grid_yc = 0
        
        while j < y_max:
            gname = str(grid_xc)+"_"+str(grid_yc)
            xaxis.append([gname,i,j,i+k,j+k])
            create_grid(gname)                                   # Creating grid text files
            #xyg = xyg + str(grid_xc)+","+str(grid_yc) + "  "            # erase if not necessary
            grid_yc = grid_yc + 1
            j = j+k
        
        grid.append(xaxis)                                              # erase if not necessary
        #print("{}\n".format(xyg))
        xaxis = []
        grid_xc = grid_xc + 1
        i = i+k
    
    x_max = i
    y_max = j
    
    print("x_min: {}\ny_min: {}\nx_max: {}\ny_max: {}".format(x_min,y_min,x_max,y_max)) ##### Think over later
    xmn = x_min
    ymn = y_min
    xmx = x_max
    ymx = y_max

    #----------------------Inserting nodes into concerning files---------------------------------
    for item in allNodes:
        nodeid = item[0]
        m = item[1]
        n = item[2]
        
        i=0
        hor = x_min
        while hor != x_max:
            if (m > hor and m <= (hor+k)) or (m == x_min):
                break
            i = i+1
            hor = hor + k
        
        j=0
        ver = y_min
        while ver != y_max:
            if (n > ver and n <= (ver+k)) or (n == y_min):
                break
            j = j+1
            ver = ver + k
        
        #print("Node {} maps to grid ({},{})".format(nodeid,i,j))
        tstr = str(i)+"_"+str(j)
        insert_record(str(nodeid)+" <"+str(m)+" ,"+str(n)+">",tstr,bucksize)
        node_grid[nodeid] = tstr
        if scntr == 150:
            time.sleep(0.001)
            scntr = 0
        scntr += 1
    

    print("\n=========\n")
    
    #-------------------Inserting ## in concerned files----------------------------------
    #----------------Signifies end of feeding node data into grids-----------------------
    
    append_special_chars("##")
    #print("\n##\n")
    
    #--------------------Entering edges into the grids-----------------------------------
    
    #------------------------<edges within cell>-----------------------------------------
    
    fname = open('edges.txt','r')
    edge_data= []
    edge_data = fname.readlines()
    fname.close()
    
    edge_info = {}
    
    external_edge_info = []       # node_1, node_2, len, grid_number (both source and destination)
    external_node_info = []       # node_id, x, y, grid_number (of external node)
    
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
        #eow = b+"-"+a
        if (ewo in edge_info.keys()):# or (eow in edge_info.keys())):
            continue
        
        edge_info[ewo] = elen
        #edge_info[eow] = elen

        t1 = node_grid[snode]
        t2 = node_grid[enode]
        #-----------------------main logic---------------------------------
        if t1 == t2:
            insert_record(a+" "+b+" <"+c+">",t1,bucksize)
        elif t1 != t2:
            external_edge_info.append([snode,enode,elen,t1])
            external_edge_info.append([snode,enode,elen,t2])

            if (snode in node_coord.keys()):
                xc = node_coord[snode][0]
                yc = node_coord[snode][1]
            else:
                xc,yc = fincoord(snode)
            if(not([snode,xc,yc,t2] in external_node_info)):
                external_node_info.append([snode,xc,yc,t2])

            if (enode in node_coord.keys()):
                xc = node_coord[enode][0]
                yc = node_coord[enode][1]
            else:
                xc,yc = fincoord(enode)
            
            if [enode,xc,yc,t1] not in external_node_info:
                external_node_info.append([enode,xc,yc,t1])

    #----------------Signifies end of feeding edge data into grids-----------------------
    
    append_special_chars("**")
    #print("\n**\n")
    
    #-----------------Entering external node data into the grids-------------------------
    for item in external_node_info:
        a = item[0]
        b = item[1]
        c = item[2]
        t = item[3]
        insert_record(str(a)+" <"+str(b)+", "+str(c)+">",t,bucksize)
        if scntr == 150:
            time.sleep(0.01)
            scntr = 0
        scntr += 1
    
    #----------------Signifies end of feeding external node data into grids-----------------------
    
    append_special_chars("%%")
    #print("\n%%\n")
    
    #-----------------Entering external edge data into the grids-------------------------
    
    for item in external_edge_info:
        a = item[0]
        b = item[1]
        c = item[2]
        t = item[3]
        insert_record(str(a)+" "+str(b)+" <"+str(c)+">",t,bucksize)
        if scntr == 150:
            time.sleep(0.001)
            scntr = 0
        scntr += 1
        
    #----------------Signifies end of feeding external edge data into grids-----------------------
    
    append_special_chars("------------------")
    #print("\n----------------\n")
    
    #print("x-min: {}\ny-min: {}\nx-max: {}\ny-max: {}".format(x_min,y_min,x_max,y_max))

    
def main1():
    global counter, grid_count
    global grid_overflow, node_grid, node_coord
    global allNodes

    inp = input("Enter k (grid dimension) and m (max records in single file) as k,m: ")
    kk,mm = inp.split(",")
    k = int(kk)
    m = int(mm)
    maincode(k,m)                                                           # input parameters k,m : 2000,100 / 3,10 / 150,10
    print("File count: {}\nGrid count: {}".format(counter,grid_count))
    
    new_file = open('node_grid.txt','w')
    
    for item in node_grid.keys():
        ipstring = str(item)+','+node_grid[item]+'\n'
        new_file.write(ipstring)
    
    new_file.close()
     
    nfile = open('grid_list.txt','w')
    
    glst = grid_overflow.keys()
    for item in glst:
        nfile.write(item+"\n")
    
    nfile.close()
    
    print("\n\n--------------------------------\n\n")
    
    question = "Select one from the below options:\n 1. Find co-ordinates of a Node ID\n 2. Map specific co-ordinates to Cell number\n 3. View the list of files corresponding to a certain cell\n Press any other number to run Dijkstra's Algorithm\n"
    
    opt = int(input(question))
    while opt == 1 or opt == 2 or opt == 3:
        
        if opt == 1:
            nid = int(input("Enter you node ID: "))
            if(nid in node_coord.keys()):
                print("<{},{}>\n".format(node_coord[nid][0],node_coord[nid][1]))
            else:
                print("Node does not exist\n")
        
        elif opt == 2:
            sss = input("Enter coordinates in this format x,y:")
            a,b = sss.split(",")
            x = float(a)
            y = float(b)
            coord_cell_mapping(x,y)
            #print("Option 2 selected")
        elif opt == 3:
            sss = input("Enter a Cell ID: ")
            if (sss in grid_overflow.keys()):
                
                lstf = grid_overflow[sss][1]
                #print(lstf)
                print("\nList of files:")
                print("{}.txt".format(sss))
                if (lstf.find("/") != -1):
                    a,b = lstf.split("/")
                    c,ext = b.split(".")
                    num = int(c)
                    for i in range(1,num+1):
                        print("{}/{}.txt".format(a,str(i)))
            else:
                print("\nInvalid Cell ID")
                
            print("\n")
            #print("Option 3 selected")
            
            
        opt = int(input(question))

if __name__ == '__main__':
    main1()


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
