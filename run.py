from gridGraph import *
#from Dijkstras import *


if __name__ == '__main__':
    
    grid_directory = "grids"
    if os.path.exists(grid_directory):
        try:
            inp = int(input("Do you want to re-run grid partition for the current graph?\nPress 1: YES\nAny other number: NO\n"))
        except Exception as e:
            print(f"{e}: User did not enter a valid integer input. Script is exiting\n")
            exit()
    else:
        inp = 1
    
    if inp:
        gridObj = gridGraph()
        gridStatus = gridObj.trigger_grid_partition()
        print(f"Grid partition status: {gridStatus}")

        # if gridStatus:
        #     main2()
    
# inp = int(input("Want to run partitioning algorithm on the graph?\nPress 1: YES\nAny other number: NO\n"))
# if(inp == 1):
#     main1()

#main2()