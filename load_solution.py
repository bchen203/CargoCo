import manifest
import calculate
import load_list_editor
import heapq
import copy
class Tree_Node:
    def __init__(self, array, loader,instruction,parent,instruction_num):
        self.current_array = array #state of the manifest
        self.current_list = loader #transfer list minus already completed directions
        self.instruction = instruction #last instruction that results in the current state of manifest
        self.parent = parent # parent tree node
        self.instruction_num = instruction_num

#TO DO LIST:
#convert it to a class
#paramater - one should be a calculate class
#paramater - one should store an instruction list
#make a start function that makes load_instruction easier to call
#change load_instructions() to return a list of instructions, rather than list of Tree_Nodes

#root node has no instruction and no parent
#instruction num of -1
def load_instructions(root_node): #should output a list of INSTRUCTIONS
    successor_number = 0
    cost = 0
    unvisited_nodes = [(cost, successor_number, root_node)]
    successor_number += 1
    heapq.heapify(unvisited_nodes)
    once = 1
    visited_nodes = []
    #check if is_finished
    while(unvisited_nodes):
        #current_cost,v,current_node = heapq.heappop(unvisited_nodes)
        current_cost,v,current_node = unvisited_nodes[0]
        unvisited_nodes.pop(0)

        if(is_finished(current_node)):
            #MAKE THE LIST OF NODES/INSTRUCTIONS THAT IS CORRECT
            current_instruction_num = current_node.instruction_num
            #print(current_instruction_num)
            node_list = [None]*current_instruction_num
            while(current_instruction_num > 0):
                node_list[current_instruction_num-1] = current_node
                current_node = current_node.parent
                current_instruction_num -= 1
            return node_list #returns list of nodes which in order, contains every instruction and array state


        for start_column in range(12): #selecting starting pos
            start_space = get_top_container(current_node.current_array, start_column)
            if(start_space != False):
                
                for dest_column in range(12): #selecting end pos
                    
                    if(start_column != dest_column):
                        end_space = get_supported_empty_space(current_node.current_array,dest_column)
                        if(end_space != False):
                            #creating a successor with an instruction moves a container within ship
                            #ADD DOUBLE CHECKING THAT ARRAY STATE IS NOT REPEATED
                            '''
                            if(once):
                                for col2 in range(8):
                                    for row2 in range(12):
                                        print(current_node.current_array[col2][row2].description, end=' ')
                                    print()
                                print('{},{},{} start space'.format(start_space.y,start_space.x,start_space.description))
                                print()
                                print()
                            '''
                            successor_array = copy.deepcopy(current_node.current_array)
                            calculator = calculate.Calculate(successor_array,0)

                            
                        
                            calculator.moveContainer(start_space.y,start_space.x,end_space.y,end_space.x)
                            


                            successor_instruction = calculate.Instruction(0,(start_space.y,start_space.x),(end_space.y,end_space.x)  )
                            successor = Tree_Node(successor_array,current_node.current_list,successor_instruction,current_node,current_node.instruction_num + 1)
                            successor_cost = get_time(start_space.y,start_space.x,end_space.y,end_space.x)
                            if(not is_repeated_move(successor,visited_nodes)):
                                heapq.heappush(unvisited_nodes,(current_cost + successor_cost,successor_number,successor))
                                
                                successor_number += 1
                           
                            
                if(start_space.description in current_node.current_list.offload_list):
                    #creating successor moving from ship to truck (only requires a start_column)
                    #end pos for a ship to truck pos is (8,0)
                    #change start_space to grab a description
                    successor_array = copy.deepcopy(current_node.current_array)
                    calculator = calculate.Calculate(successor_array,0)

                    
                    calculator.offloadContainer(start_space.y,start_space.x)
                    successor_instruction = calculate.Instruction(0,(start_space.y,start_space.x),(8,0))
                    successor_list = current_node.current_list.copy()
                    successor_list.remove_offload_list(start_space.description)
                    successor = Tree_Node(successor_array,successor_list,successor_instruction,current_node,current_node.instruction_num + 1)
                    successor_cost = get_time(start_space.y,start_space.x,8,0)
                    if(once):
                        print(current_cost+successor_cost)
                        print(successor.instruction.starting_location[0])
                        print(successor.instruction.starting_location[1])
                    heapq.heappush(unvisited_nodes,(current_cost + successor_cost,successor_number,successor))
                    
                        
                        
                        
                    successor_number += 1
        
        #creating a successor where we move a container from truck to ship
        
        for dest_column in range(0,12):
            end_space = get_supported_empty_space(current_node.current_array,dest_column)
            container_to_load = get_truck_container(current_node.current_list)
            if(end_space != False):
                successor_array = copy.deepcopy(current_node.current_array)
                calculator = calculate.Calculate(successor_array,0)
                calculator.loadContainer(container_to_load,end_space.y,end_space.x)
                successor_instruction = calculate.Instruction(0,(8,0),(end_space.y,end_space.x))
                successor_list = current_node.current_list.copy()
                successor_list.remove_pending_loads(container_to_load)
                successor = Tree_Node(successor_array,successor_list,successor_instruction,current_node,current_node.instruction_num + 1)
                successor_cost = get_time(8,0,end_space.y,end_space.x)
                heapq.heappush(unvisited_nodes,(current_cost+successor_cost,successor_number,successor) )
                successor_number += 1
        
        #stuff after making all the successors
        visited_nodes.append(current_node)
        once = 0

        #TEST STUFF
        if(once):
            for unvisited in unvisited_nodes:
                unvisited_instruction = unvisited[2].instruction
               # print('{} goes to {}'.format(unvisited_instruction.starting_location, unvisited_instruction.ending_location))
            once = 0
        


    return False #for when no solution is possible (should probably never happen)


                            




   



#looks at the transfer list and checks whether we are in finished state
def is_finished(tree_node):
    containers_left = 0
    for key in tree_node.current_list.pending_loads:
        containers_left += tree_node.current_list.pending_loads[key]
    
    for key in tree_node.current_list.offload_list:
        containers_left += tree_node.current_list.offload_list[key]
    
    #print(containers_left)

    if(containers_left == 0):
        return True
    else:
        return False

#checks if a given container is in the current offloads list
def is_in_offloads(current_transfer_list,container):
    if container.description in current_transfer_list.offload_list:
        return True
    else:
        return False

#checks if the current tree node's array matches any visited nodes' array (duplicate checking)
def is_repeated_move(tree_node,visited_nodes):
    for node in visited_nodes:
        visited_array = node.current_array
        is_identical = True
        for row in range(8):
            for column in range(12):
                if tree_node.current_array[row][column].description != visited_array[row][column].description:
                    is_identical = False

        if(is_identical):
            return True
    return False

#inside the column of an array, returns topmost container
def get_top_container(array,column):
    current_row = 7
    while(current_row >= 0):
        #print(current_row)
        #print(column)
        
        if array[current_row][column].description == "UNUSED":
            pass 
            #when current location is empty
        elif array[current_row][column].description == "NAN":
            #print("returned NAN")
            return False
            #when current space has NAN
            #idk figure out a way to make it work
        else:
            
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

#gets the name of a container that needs to be moved from truck to ship
def get_truck_container(transfer_list):
    load_list = transfer_list.get_pending_loads()
    if(load_list):
        for key in load_list:
            return key
    else:
        return False

