import sys
sys.path.append('../CargoCo')
import manifest

""""
(takes in a 2D array as an input)

    checks if move is legal function (container name, beginning location, end location - pass in these variables)
    calculating time to move container from point a to point b function (manhattan distance function)
    move/load/offload from the manifest.py (snag and alter them to work)

"""

class Instruction:
    
    def __init__(self, container_id, start_coords, end_coords):
        self.container_id = container_id
        self.starting_location = start_coords
        self.ending_location = end_coords

    def print(self):
        print(f"Printing Instruction: ")
        print(f"Container Id: {self.container_id}")
        print(f"Starting Location: {self.starting_location[0]}, {self.starting_location[1]} ") 
        print(f"Ending Location: {self.ending_location[0]}, {self.ending_location[1]} ") 
    

class Calculate:
    containerID = -1
    
    def __init__(self,manifest_array,containerID):
        self.ship_bay_array = manifest_array
        self.containerID = containerID


    #adapted from manifest.py code by Jake Blackwell (group decided to move implementation here)
    #checks if a move: passing in start location (rowStart,colStart) and end location (rowEnd,colEnd)
    def is_start_legal(self,rowStart,colStart):

        if(rowStart < 0 or rowStart >= 8 or colStart < 0 or colStart >= 12): #checks if position is out of bounds
             print("[ERROR] start position is out of bounds")
             return False
        
        containerMoving = self.ship_bay_array[rowStart][colStart]
        if(rowStart >= 7 or self.ship_bay_array[rowStart+1][colStart].description == "UNUSED"): #checks if container's start pos has a container above it

            if containerMoving.description != "UNUSED" and containerMoving.description != "NAN": #checks if start pos has a container
                return True

            else:
                print("[ERROR] cannot move a container with the name \"UNUSED\" or \"NAN\"")

        else:
            print("[ERROR] cannot move container because there is container above starting position")
        
        return False
    

    def is_end_legal(self,rowEnd,colEnd):

        if(rowEnd < 0 or rowEnd >= 8 or colEnd < 0 or colEnd >= 12): #checks if position is out of bounds
             print("[ERROR] end position is out of bounds")
             return False
        
        if self.ship_bay_array[rowEnd][colEnd].description == "UNUSED": #checks if end pos is empty
                    if rowEnd == 0 or self.ship_bay_array[rowEnd-1][colEnd].description != "UNUSED": #DAVID: checks to see if container would be floating at end pos
                        return True
                    else:
                        print("[ERROR] cannot move container to location where it is floating")
        else:
            print("[ERROR] cannot move a container to an occupied location")
        
        return False


    def is_legal_ship_move(self,rowStart,colStart,rowEnd,colEnd):
        return self.is_start_legal(rowStart,colStart) and self.is_end_legal(rowEnd,colEnd)
    

    #calculates manhattan distance between start location (rowStart,colStart) and end location (rowEnd,colEnd) - FOR ONLY LOCATIONS INSIDE SHIP
    def calculate_time(self,rowStart,colStart,rowEnd,colEnd):
        return abs(rowStart-rowEnd) + abs(colStart-colEnd)
    

    # move containers that already exist on the ship
    # [rowStart][colStart]: starting location of container (to be replaced with "UNUSED")
    # [rowEnd][colEnd]: ending location of container (to be replaced with the moved container)
    def moveContainer(self, rowStart, colStart, rowEnd, colEnd):
        containerMoving = self.ship_bay_array[rowStart][colStart]

        if(self.is_legal_ship_move(rowStart,colStart,rowEnd,colEnd)):
            # TODO: [LOG] container [name] was moved from [startLocation] to [endLocation]
            self.ship_bay_array[rowStart][colStart] = manifest.Container(0, "UNUSED",-1, rowStart, colStart)
            self.ship_bay_array[rowEnd][colEnd] = containerMoving
            containerMoving.changeCoords(rowEnd, colEnd)


    # load containers onto the ship
    # containerDescription: the description of a container provided by the operator
    # [rowEnd][colEnd]: ending location of container <-- NOTE: in the final implementation, this parameter will be generated by the solution, not the operator
    def loadContainer(self, containerDescription, rowEnd, colEnd):
        if containerDescription != "UNUSED" and containerDescription != "NAN":
            if(self.is_end_legal(rowEnd,colEnd)):
                    # TODO: [LOG] container [name] was loaded onto the ship. It is located at [rowEnd][colEnd]
                    # NOTE: a weight of -1 is given as a placeholder weight since the weight of the container will not be determined until the operator picks up the container during the instruction phase of the program
                    self.ship_bay_array[rowEnd][colEnd] = manifest.Container(-1, containerDescription, self.generateID(), rowEnd, colEnd)
                
        else:
            print("[ERROR] cannot load a container with the name \"UNUSED\" or \"NAN\"")


    # offload containers onto the ship
    # [rowStart][colStart]: location of the container to be offloaded <-- NOTE: in the final implementation, this parameter will be generated by the solution, not the operator
    # ERROR CHECKING: a container can only be offloaded if the given location is in the 2D ship_bay_array range and the container being offloaded is NOT "UNUSED" nor "NAN"
    def offloadContainer(self, rowStart, colStart):
        if(self.is_start_legal(rowStart,colStart)):
                # TODO: [LOG] container [name] was offloaded from the ship.
                self.ship_bay_array[rowStart][colStart] = manifest.Container(0, "UNUSED",-1, rowStart, colStart)


    # returns the next ID needed to uniquely identify a container and will update the manifest class's ID global containerID variable
    def generateID(self):
        self.containerID += 1
        return self.containerID
    

#inside the column of an array, returns topmost container
def get_top_container(array,column):
    current_row = 7
    while(current_row >= 0):
        if array[current_row][column].description == "UNUSED":
            pass 
            #when current location is empty
        elif array[current_row][column].description == "NAN":
            #print("returned NAN")
            return False
            #when current space has NAN
            #idk figure out a way to make it work
        else:
            #print("returned container")
            return array[current_row][column]
        current_row -= 1
    #print("returned unused")
    return False
    

#finds a suitable destination space (returns container class with 'UNUSED') for a container in a given column
def get_supported_empty_space(array,column):
    current_row = 7
    while(current_row >= 0):
        if array[current_row][column].description == "UNUSED":
            pass 
            #when current location is empty
        else:
            if(current_row < 7):
                return array[current_row+1][column]
            else:
                return False
        current_row -= 1

    return array[0][column]
    #when column is empty

#finds the time cost of an instruction
def get_time(startRow,startCol,endRow,endCol):
    time = 0
    if(startRow == 8 and startCol == 0):
        time += 2 #time to move from ship to truck
    elif(endRow == 8 and endCol == 0):
        time += 2 #time to move from truck to ship

    time += abs(startRow-endRow) + abs(startCol-endCol)
    return time