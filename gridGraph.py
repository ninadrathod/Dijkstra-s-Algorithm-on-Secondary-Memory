#!/usr/bin/env python
# coding: utf-8
#new code

import os
import time
import shutil
import traceback

class gridGraph:

    def __init__(self):
        self._reset_state()
        #self.prepare_grids_directory(self.grid_directory)
    
    # -----------------------------------
    # Reinitializes all internal state variables to their starting values.
    # This is called by __init__ and prepare_grids_directory.
    # -----------------------------------

    def _reset_state(self):
        self.counter = 0
        self.grid_count = 0
        self.grid_overflow = {} # grid_overflow['grid_id'] returns [overflow_counter,grid_file.txt]
        self.node_grid = {} #node_grid['node_id'] returns parent_grid_id
        self.allNodes = []
        self.node_coord = {}
        self.xmx,self.ymx,self.xmn,self.ymn,self.gdim = 0,0,0,0,0
        self.grid_directory = "grids"
        

    # ---------------------------------
    # Checks for the existence of a specified directory (default: 'grids/').
    # If the directory exists, it deletes the entire directory (like 'rm -rf').
    # Then, it creates the directory.
    # ---------------------------------

    def prepare_grids_directory(self):
        
        self._reset_state()
        directory_name = self.grid_directory
        
        # 1. Check if the directory exists and delete it (equivalent to rm -rf)
        if os.path.exists(directory_name):
            print(f"Directory '{directory_name}/' found. Deleting and recreating...")
            try:
                # Use shutil.rmtree for the 'rm -rf' effect
                shutil.rmtree(directory_name)
                print(f"  - Successfully deleted old directory: {directory_name}")
            except Exception as e:
                print(f"Error deleting directory '{directory_name}/': {e}")
                return # Exit function if deletion fails

        # 2. Create the directory (either because it was just deleted or never existed)
        try:
            # Use os.makedirs for safe creation; it handles intermediate directories if needed
            os.makedirs(directory_name)
            print(f"Directory '{directory_name}/' created successfully.")
        except Exception as e:
            print(f"Error creating directory '{directory_name}/': {e}")
            return # Exit function if creation fails

    # -----------------------------------
    # map input co-ordinates m and n to grid
    # -----------------------------------

    def coord_cell_mapping(self,m,n):
        
        #global xmx, ymx, xmn, ymn, gdim
        k = self.gdim
        
        if m < self.xmn or m > self.xmx or n > self.ymx or n < self.ymn:
            print("Out of Bounds\n")
        else:
            i=0
            hor = self.xmn
            while hor != self.xmx:
                if (m > hor and m <= (hor+k)) or (m == self.xmn):
                    break
                i = i+1
                hor = hor + k

            j=0
            ver = self.ymn
            while ver != self.ymx:
                if (n > ver and n <= (ver+k)) or (n == self.ymn):
                    break
                j = j+1
                ver = ver + k

            tstr = str(i)+"_"+str(j)
            print("Input node will map to cell {}\n".format(tstr))


    # -----------------------------------
    # fincord() function will help fetch the coordinates of resp node and save it to a dictionary
    # -----------------------------------

    def fincoord(self,nodeid):
        for item in self.allNodes:
            if item[0] == nodeid:
                x = item[1]
                y = item[2]
                self.node_coord[nodeid] = [x,y]
                break
        return x,y

    # -----------------------------------
    # append special characters at end of files
    # -----------------------------------

    def append_special_chars(self,string):
        for itm in self.grid_overflow.keys():
            fname = self.grid_overflow[itm][1]
            nfile = open(fname,'a')
            nfile.write(string+"\n")
            nfile.close()
            time.sleep(0.001)

    # -----------------------------------
    # insert_record() function will enter our records into concerned file
    # -----------------------------------

    def insert_record(self,data,gridname,m):
        temp = self.grid_overflow[gridname]
        # global counter
        # global m
        # print("{}\n{}".format(temp[0],temp[1]))
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
                self.grid_overflow[gridname] = [1,filename]
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
                self.grid_overflow[gridname] = [1,filename]
            self.counter += 1
        else:
            new_file = open(temp[1],'a')
            new_file.write(data+"\n")
            new_file.close()
            cntr = temp[0]
            cntr += 1
            fname = temp[1]
            self.grid_overflow[gridname] = [cntr,fname]

    # -----------------------------------
    # Creating a grid text file
    # -----------------------------------

    def create_grid(self,gridname):
        fptr = open(gridname+".txt",'w')
        fptr.write("------------------\n")
        fptr.close()
        self.grid_overflow[gridname] = [0,gridname+".txt"]
        self.grid_count += 1
        self.counter += 1
    
    # -----------------------------------
    # Inserting data into grids
    # -----------------------------------

    def insert_into_grids(self,k,bucksize):
        
        scntr = 0
        self.gdim = k
        allRows = []                # Input Node file is read into the allRows list line-by-line
        
        # copying all the data from input file to 'allRows' variable
        tempFile = open('../nodes.txt','r')
        allRows = tempFile.readlines()
        tempFile.close()
        
        #------------------ calculate x_min, y_min, x_max, y_max-----------------------------
        x_min,y_min,x_max,y_max = 0,0,0,0
        first_node = True
        node_rec = set() # To store all the node ids we have seen thus far
        
        for row in allRows:
            
            if scntr == 150:
                time.sleep(0.001)
                scntr = 0
            scntr += 1
            
            x = row.replace("\n","")
            try:
                a,b,c = x.split(" ")
                nodenum = int(a)
                x_coordinate = float(b)
                y_coordinate = float(c)
            except Exception as e:
                print(f"{e}: Invalid input in nodes.txt in this line: {x}\n")
                raise
            
            if (nodenum in node_rec):
                continue
            
            node_rec.add(nodenum)
            self.allNodes.append([nodenum,x_coordinate,y_coordinate])
            self.node_coord[nodenum] = [x_coordinate,y_coordinate]
            #print("Node{} :({},{})".format(nodenum,x_coordinate,y_coordinate))
            
            if first_node:
                x_min,y_min = x_coordinate,y_coordinate
                first_node = False
            
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
        
        #------------------------------------
        # Creating Grid files
        # -----------------------------------
        i,j = x_min,y_min
        grid_xc = 0
        
        grid = []
        
        while i < x_max:
            j = y_min
            grid_yc = 0
            xaxis = []
            
            while j < y_max:
                gname = str(grid_xc)+"_"+str(grid_yc)
                xaxis.append([gname,i,j,i+k,j+k])
                self.create_grid(gname)                                   # Creating grid text files
                grid_yc = grid_yc + 1
                j = j+k
            
            grid.append(xaxis)                                              # erase if not necessary
            grid_xc = grid_xc + 1
            i = i+k
        
        x_max,y_max = i,j
        
        print("x_min: {}\ny_min: {}\nx_max: {}\ny_max: {}".format(x_min,y_min,x_max,y_max)) ##### Think over later
        self.xmn,self.ymn,self.xmx,self.ymx = x_min,y_min,x_max,y_max
        
        #----------------------Inserting nodes into concerning files---------------------------------
        for item in self.allNodes:
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
            self.insert_record(str(nodeid)+" <"+str(m)+" ,"+str(n)+">",tstr,bucksize)
            self.node_grid[nodeid] = tstr
            if scntr == 150:
                time.sleep(0.001)
                scntr = 0
            scntr += 1
        

        print("\nInserted node data into the grids\n")
        
        #-------------------Inserting ## in concerned files----------------------------------
        #----------------Signifies end of feeding node data into grids-----------------------
        
        self.append_special_chars("##")
        
        #--------------------Entering edges into the grids-----------------------------------
        
        #------------------------<edges within cell>-----------------------------------------
        
        fname = open('../edges.txt','r')
        edge_data= []
        edge_data = fname.readlines()
        fname.close()
        
        edge_info = {}
        
        external_edge_info = []       # node_1, node_2, len, grid_number (both source and destination)
        external_node_info = set()       # node_id, x, y, grid_number (of external node)
        
        for item in edge_data:
            if scntr == 150:
                time.sleep(0.001)
                scntr = 0
            scntr += 1
            tp = item.replace("\n","")
            try:
                a,b,c = tp.split(" ")
                snode = int(a)
                enode = int(b)
                elen = float(c)
            except Exception as e:
                print(f"{e}: Invalid input in edges.txt in this line: {tp}\n")
                raise

            ewo = a+"-"+b
            if (ewo in edge_info.keys()):# or (eow in edge_info.keys())):
                continue
            
            edge_info[ewo] = elen
  
            t1 = self.node_grid[snode]
            t2 = self.node_grid[enode]
            #-----------------------main logic---------------------------------
            if t1 == t2:
                self.insert_record(a+" "+b+" <"+c+">",t1,bucksize)
            elif t1 != t2:
                external_edge_info.append([snode,enode,elen,t1])
                external_edge_info.append([snode,enode,elen,t2])

                if (snode in self.node_coord.keys()):
                    xc = self.node_coord[snode][0]
                    yc = self.node_coord[snode][1]
                else:
                    xc,yc = self.fincoord(snode)
                
                if(not((snode,xc,yc,t2) in external_node_info)):
                    external_node_info.add((snode,xc,yc,t2))

                if (enode in self.node_coord.keys()):
                    xc = self.node_coord[enode][0]
                    yc = self.node_coord[enode][1]
                else:
                    xc,yc = self.fincoord(enode)
                
                if((enode,xc,yc,t1) not in external_node_info):
                    external_node_info.add((enode,xc,yc,t1))

        #----------------Signifies end of feeding edge data into grids-----------------------
        
        self.append_special_chars("**")
        
        #-----------------Entering external node data into the grids-------------------------
        for item in external_node_info:
            a,b,c,t = item
            self.insert_record(str(a)+" <"+str(b)+", "+str(c)+">",t,bucksize)
            if scntr == 150:
                time.sleep(0.01)
                scntr = 0
            scntr += 1
        
        #----------------Signifies end of feeding external node data into grids-----------------------
        
        self.append_special_chars("%%")
        #print("\n%%\n")
        
        #-----------------Entering external edge data into the grids-------------------------
        
        for item in external_edge_info:
            a,b,c,t = item
            self.insert_record(str(a)+" "+str(b)+" <"+str(c)+">",t,bucksize)
            if scntr == 150:
                time.sleep(0.001)
                scntr = 0
            scntr += 1
            
        #----------------Signifies end of feeding external edge data into grids-----------------------
        
        self.append_special_chars("------------------")
            
    # -----------------------------------
    # Trigger grid creation and try
    # certain operations on the created grids
    # -----------------------------------
    def trigger_grid_partition(self):
        
        self.prepare_grids_directory()
        os.chdir(self.grid_directory)

        try:
            inp = input("Enter k (grid dimension) and m (max records in single file) as k,m: ")
            kk,mm = inp.split(",")
            k = int(kk)
            m = int(mm)
        except Exception as e:
            print(f"{e}: Invalid input for grid partition, Integer input is expected\n")
            os.chdir("../")
            return 0
        
        try:
            self.insert_into_grids(k,m)
        except Exception as e:
            print(f"{e}: Failed to create grids\n Check you input files\n")
            traceback.print_exc()
            os.chdir("../")
            return 0
        
        print("File count: {}\nGrid count: {}".format(self.counter,self.grid_count))
    
        new_file = open('node_grid.txt','w')
    
        for item in self.node_grid.keys():
            ipstring = str(item)+','+self.node_grid[item]+'\n'
            new_file.write(ipstring)
        
        new_file.close()
        
        nfile = open('grid_list.txt','w')
        
        glst = self.grid_overflow.keys()
        for item in glst:
            nfile.write(item+"\n")
        
        nfile.close()
        
        print("\n\n--------------------------------\n\n")
        
        question = "Select one from the below options:\n 1. Find co-ordinates of a Node ID\n 2. Map specific co-ordinates to Cell number\n 3. View the list of files corresponding to a certain cell\n Press any other number to run Dijkstra's Algorithm\n"
        
        try:
            opt = int(input(question))
        except Exception as e:
            print(f"{e}: User did not enter a valid integer value between 1 and 3\n")
            opt = 0
        
        while opt == 1 or opt == 2 or opt == 3:
            
            if opt == 1:
                nid = int(input("Enter you node ID: "))
                if(nid in self.node_coord.keys()):
                    print("<{},{}>\n".format(self.node_coord[nid][0],self.node_coord[nid][1]))
                else:
                    print("Node does not exist\n")
            elif opt == 2:
                xy_str = input("Enter coordinates in this format x,y:")
                xstr,ystr = xy_str.split(",")
                x = float(xstr)
                y = float(ystr)
                self.coord_cell_mapping(x,y)
            elif opt == 3:
                cell_id = input("Enter a Cell ID: ")
                if (cell_id in self.grid_overflow.keys()):
                    
                    lstf = self.grid_overflow[cell_id][1]
                    print("\nList of files:")
                    print("{}.txt".format(cell_id))
                    if (lstf.find("/") != -1):
                        a,b = lstf.split("/")
                        c,ext = b.split(".")
                        num = int(c)
                        for i in range(1,num+1):
                            print("{}/{}.txt".format(a,str(i)))
                else:
                    print("\nInvalid Cell ID")
                    
                print("\n")
            try:
                opt = int(input(question))
            except Exception as e:
                print(f"{e}: User did not enter a valid integer value between 1 and 3\n")
                opt = 0
        
        os.chdir("../")
        return 1

