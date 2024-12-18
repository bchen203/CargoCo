import sys
sys.path.append('../CargoCo')
import manifest
import LogHandler

""""
(takes in a 2D array as an input)

    checks if move is legal function (container name, beginning location, end location - pass in these variables)
    calculating time to move container from point a to point b function (manhattan distance function)
    move/load/offload from the manifest.py (snag and alter them to work)

"""

class Instruction:
    
    def __init__(self, container_id, start_coords, end_coords, description=None):
        self.container_id = container_id
        self.starting_location = start_coords
        self.ending_location = end_coords
        self.description = description

    def print(self):
        print(f"Printing Instruction: ")
        print(f"Container Id: {self.container_id}")
        print(f"Starting Location: {self.starting_location[0]}, {self.starting_location[1]} ") 
        print(f"Ending Location: {self.ending_location[0]}, {self.ending_location[1]} ") 
        print(f"Container Description: {self.description} ") 

    def __lt__(self, other):
        return other
    
    def __gt__(self, other):
        return other
    

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
    

    # #calculates manhattan distance between start location (rowStart,colStart) and end location (rowEnd,colEnd) - FOR ONLY LOCATIONS INSIDE SHIP
    # def calculate_time(self,rowStart,colStart,rowEnd,colEnd):
    #     if (rowEnd == 8 and colEnd == 0) or (rowStart == 8 and colStart == 0):
    #         # +2 minutes to load/offload from a truck
    #         return abs(rowStart-rowEnd) + abs(colStart-colEnd) + 2
    #     else:
    #         # time cost to move containers within the ship
    #         return abs(rowStart-rowEnd) + abs(colStart-colEnd)
    

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

    def addLoadWeight(self, loadWeight, id):
        #print(f"{loadWeight} -> {id}")
        for r in range(8):
            for c in range(12):
                if self.ship_bay_array[r][c].id == id:
                    self.ship_bay_array[r][c].changeWeight(loadWeight)
                    #print(f"{self.ship_bay_array[r][c].description} has a weight of {self.ship_bay_array[r][c].weight}")

    # load containers onto the ship
    # containerDescription: the description of a container provided by the operator
    # [rowEnd][colEnd]: ending location of container <-- NOTE: in the final implementation, this parameter will be generated by the solution, not the operator
    def loadContainer(self, containerDescription, rowEnd, colEnd, id=None):
        if containerDescription != "UNUSED" and containerDescription != "NAN":
            if(self.is_end_legal(rowEnd,colEnd)):
                    # TODO: [LOG] container [name] was loaded onto the ship. It is located at [rowEnd][colEnd]
                    # NOTE: a weight of -1 is given as a placeholder weight since the weight of the container will not be determined until the operator picks up the container during the instruction phase of the program
                    if id == None:
                        conID = self.generateID()
                    else:
                        conID = id
                        if self.containerID < id:
                            self.containerID = id
                    self.ship_bay_array[rowEnd][colEnd] = manifest.Container(-1, containerDescription, conID, rowEnd, colEnd)
                    #LogHandler.logLoadUnloadOperation(containerDescription, True)
                
        else:
            print("[ERROR] cannot load a container with the name \"UNUSED\" or \"NAN\"")


    # offload containers onto the ship
    # [rowStart][colStart]: location of the container to be offloaded <-- NOTE: in the final implementation, this parameter will be generated by the solution, not the operator
    # ERROR CHECKING: a container can only be offloaded if the given location is in the 2D ship_bay_array range and the container being offloaded is NOT "UNUSED" nor "NAN"
    def offloadContainer(self, rowStart, colStart):
        if(self.is_start_legal(rowStart,colStart)):
                # TODO: [LOG] container [name] was offloaded from the ship.
                tempDescription = self.ship_bay_array[rowStart][colStart].description
                self.ship_bay_array[rowStart][colStart] = manifest.Container(0, "UNUSED",-1, rowStart, colStart)
                #LogHandler.logLoadUnloadOperation(tempDescription, False)

    # Searches the manifest 2D array for placeable slots (ie, the first available layer of open spaces in each column)
    # Returns a list of 2-element tuples that represent the indices of placeable slots
    def findPlaceableSlots(self):
        foundInColumn = False
        placeableSlots = []

        for column in len(self.ship_bay_array[0]):
            foundInColumn = False

            for row in len(self.ship_bay_array):
                if (row < len(self.ship_bay_array)):
                    if self.ship_bay_array[row][column].description != "UNUSED":
                        placeableSlots.append((row, column))
                        foundInColumn = True
                        break 

            if (foundInColumn):
                break
                
        



    # returns the next ID needed to uniquely identify a container and will update the manifest class's ID global containerID variable
    def generateID(self):
        self.containerID += 1
        return self.containerID
    
    def performInstruction(self, currInstruction):
        # needs to determine what operation is being performed:
        #currInstruction.print()
        currOperation = self.determineInstruction(currInstruction)
        #print(currOperation)
        if currOperation == "load":
            #TODO: replace description with container name derived from currInstruction.container_id if needed
            #TODO: make sure starting_location and ending_location are tuples in the form of (row,col)
            self.loadContainer(currInstruction.description, currInstruction.ending_location[0], currInstruction.ending_location[1], currInstruction.container_id)            
            #self.loadContainer(self.getContainerDescription(currInstruction.container_id), currInstruction.ending_location[0], currInstruction.ending_location[1])
            LogHandler.logLoadUnloadOperation(currInstruction.description, True)
        elif currOperation == "offload":
            self.offloadContainer(currInstruction.starting_location[0], currInstruction.starting_location[1])
            LogHandler.logLoadUnloadOperation(currInstruction.description, False)
        elif currOperation == "balance": # could also be any container movement
            self.moveContainer(currInstruction.starting_location[0], currInstruction.starting_location[1], currInstruction.ending_location[0], currInstruction.ending_location[1])
        else: 
            print("[ERROR] could not calculate instruction")
    
    # needs to determine what operation is being performed:
    #    load (loadContainer):          start position must be some invalid location
    #    offload (offloadContainer):    end position must be some invalid location
    #    balance (moveConatiner):       start and end position must be valid locations
    # NOTE: only thing we need to note in the future is whether we are loading or offloading from the buffer or a truck (could be done with an instruction flag for buffer)
    def determineInstruction(self, currInstruction):
        if currInstruction.starting_location[0] == 8 and currInstruction.starting_location[1] == 0:
            return "load"
        elif currInstruction.ending_location[0] == 8 and currInstruction.ending_location[1] == 0:
            return "offload"
        elif self.is_legal_ship_move(currInstruction.starting_location[0], currInstruction.starting_location[1], currInstruction.ending_location[0], currInstruction.ending_location[1]):
            return "balance"
        else:
            print("[ERROR] could not determine current instruction")
    
    def getNumAvailableSpaces(self):
        availableSpaces = 0
        for r in range(8):
            for c in range(12):
                if self.ship_bay_array[r][c].description == "UNUSED":
                    availableSpaces += 1
        return availableSpaces
    
    def getContainerDescription(self, id):
        for r in range(8):
            for c in range(12):
                if self.ship_bay_array[r][c].id == id:
                    return self.ship_bay_array[r][c].description
        print(f"[ERROR] could not find a container with id {id}. This could be a container that is being loaded onto the ship")
        return None


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
