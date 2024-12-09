import manifest
import calculate
import heapq

#TODO: Change the implementation of global variables

class BalanceOperator():

    def __init__(self, calculator, manifestObject):
        self.calculator = calculator
        self.manifestObject = manifestObject
        self.instructionList = []

    def perform_balance_operation(self, manifest_array): #given a 2D array of the manifest, perform the balance operation
        # First: Check if already balanced. If so, do nothing!
        if (self.is_ship_balanced(manifest_array)):
            return [] #empty set of instructions

        #First-Point-Five: Check if balanceable
        if (not self.is_ship_balanceable(manifest_array)):
            return None

        # Second: Calculate the solution
        solution_array = self.perform_balance_operation_uniform_cost(self.calculator.ship_bay_array)
        
        # Third: Making the moves (updating 2D array through calculate.py)
        # for instruction in solution_array:
        #     self.calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0],  instruction.ending_location[1])
        #     pass
        self.instructionList = solution_array

        return solution_array

    def perform_balance_operation_uniform_cost(self, manifest_array):
        #Need a heapqueue that has tuples (Total Time, [Array of instructions])
        instruction_heap = []

        heapq.heappush(instruction_heap, (0, [])) #Getting started, I'd like to write it so that the loop can handle it w/o special setup

    # First, check if balanced (done in the function that calls this)
    # Then, explore every single possible move, generating an instruction and pushing that and it's total time to the heapqueue
    # For each tuple in the heapqueue, do the following loop:
    # Pop move with least time. A
    # Apply imstructions to the grid based on the list of instructions
    # Find all possible moves, push all of them to the heapqueue, based on the old list of instructions
    # Move on
        counter = 0
        while(True): #break on finding a solution
            current_state = heapq.heappop(instruction_heap)
            temp_array = manifest_array #saving array.
            curInstructionTime = current_state[0]
            curInstructionsArray = current_state[1]
            
            for instruction in curInstructionsArray: #applying current instructions, will need to reverse after
                self.calculator.moveContainer(instruction.starting_location[0], instruction.starting_location[1], instruction.ending_location[0], instruction.ending_location[1])

            if self.is_ship_balanced(self.calculator.ship_bay_array): #break if balanced
                reverseInstructions = list(curInstructionsArray)
                reverseInstructions.reverse()
                for instruction in reverseInstructions:
                    self.calculator.moveContainer(instruction.ending_location[0], instruction.ending_location[1], instruction.starting_location[0], instruction.starting_location[1])
                return curInstructionsArray

            #Find each possible move, from each possible container:
            movable_containers = []
            for column in range(len(self.calculator.ship_bay_array[0])):
                curContainer = calculate.get_top_container(self.calculator.ship_bay_array, column)
                if not curContainer == False: #False if none in that column
                    movable_containers.append(curContainer)

            for container in movable_containers:
                for column in range(len(self.calculator.ship_bay_array[0])):
                    if container.x == column: #making sure that you cannot put a container on top of itself:
                        continue
                    current_goal_slot = calculate.get_supported_empty_space(self.calculator.ship_bay_array, column)
                    if not current_goal_slot == False: #False if none exists in that column

                        curInstruction = calculate.Instruction(container.id, (container.y, container.x), (current_goal_slot.y, current_goal_slot.x))
                        instructionTime = calculate.get_time(curInstruction.starting_location[0], curInstruction.starting_location[1], curInstruction.ending_location[0], curInstruction.ending_location[1])
                        newInstructions = list(curInstructionsArray)
                        newInstructions.append(curInstruction)
                        heapq.heappush(instruction_heap, (curInstructionTime + instructionTime, newInstructions)) #Pushing updated time and instruction array.
            
            #Reversing the changes:
            curInstructionsArray.reverse()
            for instruction in curInstructionsArray:
                self.calculator.moveContainer(instruction.ending_location[0], instruction.ending_location[1], instruction.starting_location[0], instruction.starting_location[1])

            counter += 1
        pass

    #Will return a solution
    def perform_balance_operation_brute_force_helper(self, current_left_containers, current_right_containers, current_weight, remaining_containers): #recursive brute force :')
        
        #base case
        if len(remaining_containers) == 0:
            if self.is_balanced(current_weight[0], current_weight[1]):
                return (current_left_containers, current_right_containers) #Insert correct solution, where each container is sorted to left or right
            else:
                return None
        else:
            if self.is_balanceable(remaining_containers, current_weight):
                current_container = remaining_containers.pop()

                #Left
                new_left_containers = current_left_containers
                new_left_containers.append(current_container)
                left = self.perform_balance_operation_brute_force_helper(new_left_containers, current_right_containers, (current_weight[0]+current_container.weight, current_weight[1]), remaining_containers) 

                #right
                new_right_containers = current_right_containers
                new_right_containers.append(current_container)
                right = self.perform_balance_operation_brute_force_helper(current_left_containers, new_right_containers, (current_weight[0], current_weight[1]+current_container.weight), remaining_containers) 
                
                if (right == None and not left == None):
                    return left
                elif (left == None and not right == None):
                    return right
                else:
                    return None
            else:
                return None    

    def get_partition(self, array): #Get the partition line (considering which side is left/right) returns last index of left side (inclusive)
        return len(array[0])/2 - 1

    #Given a list of containers and a tuple with the left and right side weights, figure out if everything is still sortable in the current state
    def is_balanceable(self, containers, current_weight): 
        container_weights = []
        for container in containers:
            container_weights.append(container.weight)

        sorted_weights = (sorted(container_weights))
        sorted_weights.reverse()
        
        for container in sorted_weights:
            if current_weight[0] > current_weight[1]:
                current_weight[1] += container
            else:
                current_weight[0] += container

        if (self.is_balanced(current_weight[0], current_weight[1])):
            return True
        else:
            return False

    #Given a manifest, checks whether the ship is balanceable:
    def is_ship_balanceable(self, manifest_array):
        list_of_containers = []

        for row in manifest_array:
            for container in row: 
                if not (container.description == "UNUSED" or container.description ==  "NAN"):
                    list_of_containers.append(container)


        current_weight = [0,0]

        return self.is_balanceable(list_of_containers, current_weight)

    # Given a left-side and right-side weight, returns True if balanced, False if not balanced.
    def is_balanced(self, port_weight, starboard_weight):

        if(port_weight < 1 or starboard_weight < 1): #catching 0 and below
            return False

        return (max(port_weight, starboard_weight) / min(port_weight , starboard_weight) < 1.1)

    #Checks if a ship is balanced
    def is_ship_balanced(self, manifest_array): #manifest is a 2D array
        left_partition_inclusive = self.get_partition(manifest_array) 

        port_weight = 0
        starboard_weight = 0

        for row in manifest_array: #assumign row-column?
            i = 0
            for container in row:
                #skip if not a container (IE NAN or UNUSED)

                if i <= left_partition_inclusive:
                    port_weight += container.weight
                else:
                    starboard_weight += container.weight
                i += 1
        
        return self.is_balanced(port_weight, starboard_weight)   

    #returns instruction list, matching call to load/offload solution
    def get_instruction_list(self):
        #TODO: Add a check for whether a solution has been generated?
        return self.instructionList