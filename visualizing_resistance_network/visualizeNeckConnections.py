"""
@author: Obehi Georgina Dibua

Given a file that contains a network of resistors in an electronics circuit, 
this script plots the resistance network 
to show what the connections in the resistance network looks like
"""

import matplotlib.pyplot as plt
from math import ceil


class makeQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue = [value] + self.queue     
    
    def dequeue(self):
        return self.queue.pop()

# This function creates a graph from the connections input
# Inputs:
# connections is a list which contains all the connections in the network
#             stored as strings such as 10-11, which shows nodes 10 and 11 are connected
# start is a string which denotes the node that should be treated as the head of the graph  
# endNode is the node that is considered the end of the resistance network 
# For example, for a resistance network where the potential difference is applied around nodes
# 0 and 1, then start could be '0' and endNode '1', the reverse is also acceptable
# Outputs:
# neckDic is the dictionary containing the connections each key is paired with a list
# that outlines all the nodes that key is connected to
# newc is a list containing whatever connections in the input connections are not connected
# to either the start or endNode. These are denoted as floating connections in the rest of the script     
def mapFromStart(start, connections, endNode):
    # Initiate the dictionary with the first key being the start node
    neckDic = {start:[]}
    
    # Queue up the nodes
    keyQueue = makeQueue()
    keyQueue.enqueue(start)
    
    # Make a copy of the connections
    newc = connections[:]
    
    while keyQueue.queue:
        # dequeue
        key = keyQueue.dequeue()
        
        #Find all necks with key in them
        key_necks = []
        for neck in newc:
            neckParts = neck.split('-')
            if key in neckParts:
                key_necks.append(neck)
                
        # Place necks with key into the dictionary connected to it
        # Need to do this in a seperate loop because the necks found are being
        # removed from newc list. To prevent missing elements in newc, removing 
        # from the list can't happen while iterating through it in a for loop
        for neck in key_necks:
            neckParts = neck.split('-')
            if neckParts[0] == key:
                entry = neckParts[1]
            elif neckParts[1]==key:
                entry = neckParts[0]
            else:
                print("I SHOULDN'T SEE THIS!")
            
            if (entry != endNode) and (entry not in keyQueue.queue):
                neckDic[entry] = []
                #enqueue new nodes
                keyQueue.enqueue(entry) 
                
            #update dictionary with neck connections then remove neck as it's been considered
            neckDic[key].append(entry)
            newc.remove(neck)
                    
    return neckDic, newc

# Given a dictionary of connections (input dicConnections) this function 
# Maps the nodes to vertical and horizontal positions in the graph
# The startNode would be at a vertical level of 0 and the nodes connected to
# 0 directly will be at vertical levels of 1, and so on, till the end is reached
# Within the same level horizontal_level sets the breadth position of the nodes
# These vertical and horizontal levels are then translated to positions in a 2D
# cartesian plane for plotting
# These positions are stored in the level_posDic output
# levelDic is the dictionary that maps between nodes and the untranslated vertical and 
# horizontal levels
# Finally the height and width of the graph are returned. The width is defined as the 
# maximum number of nodes in any level of the graph
def getNodePositions(dicConnections, startNode = '0', endNode = '1'):
    # Initiate the dictionaries
    levelDic = {}
    height_to_width = {} # This dictionary stores the relationship between each level and the number of nodes in that level of the graph
    
    level = 0
    buds = [startNode]

    nodeList = list(dicConnections.keys())
    
    while nodeList:
        # find all the nodes connected to key (all buds/children of node key)
        next_bud = []
        
        # horizontal_level adds horizontal count
        for horizontal_level, bud in enumerate(buds):
            # connect level to node
            levelDic[bud] = [level, horizontal_level]
            
            # find all children
            children = dicConnections[bud][:]
            # remove 1 since that's the last node
            if endNode in children:
                children.remove(endNode)
            
            # Add next children to the next_bud list
            for child in children:
                if child not in next_bud:
                    next_bud.append(child)
                    
            nodeList.remove(bud)
    
        # Update the buds list for next level
        buds = next_bud[:]
        
        # Increment horizontal_level by 1 to give it length (as opposed to position)
        horizontal_level += 1 
        
        height_to_width[level] = horizontal_level
        
        # Increment vertical level
        level += 1
    
    levelDic[endNode] = [level, 0]
    height_to_width[level] = 1
 
    width = max(height_to_width.values())
    height = level + 1
    
    # This part of the function
    # maps each node to a spatial coordinate in the 2D grid
    level_posDic = {}
    
    # Defines how much seperation to have between nodes in the same level
    axis_sep = 5
    
    height_1 = height - 1
    # Calculate the center of the graph
    x_center = ceil(width*axis_sep - width/2) + 4
    
    for key, pos in levelDic.items():
        depth_level = pos[0]
        horizontal_level = pos[1]
        width_of_level = height_to_width[depth_level]
        
        # translate horizontal and vertical levels to actual positions
        y_position = (height_1 - int(depth_level))*axis_sep + 2
        x_position = x_center - (ceil(width_of_level/2) - horizontal_level)*axis_sep
    
        level_posDic[key] = [x_position, y_position]
        
    return levelDic, height, width, level_posDic

# This function takes in the dictionary which maps nodes to positions
# as well as the list of the resistance connections, and the floating connections
# and plots all resistance connections that are not floating, that is that are connected to 
# either the start or end node
def plotConnections(level_posDic, connection, floatCon, figName = 'plotResistanceNetwork.jpg'):    
    #remove floating connections before plotting
    for floating_connection in floatCon:
        connection.remove(floating_connection)
    
    # For each connection in the list plot the line that connects the nodes
    fig1 = plt.figure()
    for con in connection:
        nodes = con.split('-')
        
        # Get the x and y positions for both nodes that make up the connection
        xArray = [level_posDic[key][0] for key in nodes]
        yArray = [level_posDic[key][1] for key in nodes]
        
        # Plot the line connecting both nodes
        plt.plot(xArray,yArray,'k-', 
                 linewidth = 0.25)
    
    # Plot all the nodes in the resistance network
    for node, pos in level_posDic.items():
        plt.text(pos[0], pos[1], node,
                 bbox = {"boxstyle" : "circle", "color":"lightcyan"},
                 fontsize = 'x-small')
    
    # Save the figure
    fig1.savefig(figName)
    plt.close()
            

# Main implementation
if __name__ == '__main__':
    # Define the name of the file which contains the information for the 
    # resistance network
    fileName = 'nodeFile2.cir' 
    
    # Read in the file
    networkList = []
    with open(fileName,'r') as fileIn:
        allLines = fileIn.read()
    
    # Build connections between nodes to the form '0-2', '3-4', etc
    for line in allLines.split('\n'):
        if line and 'R' == line[0]:
            inline = line.split()
            networkList.append(inline[1]+'-'+inline[2])

    # Build the graph from the connections
    dicConnectionsFrom0, floating_connections = mapFromStart('0', networkList, '1')       

    # Convert the nodes of the graph into positions for visualization
    levelDic, height, width, level_posDic = getNodePositions(dicConnectionsFrom0)
    print('Tree dimensions:', height, 'x', width)
 
    # Plot connections
    figure_name = 'ResistanceNetworkPlotOf_' + fileName[:-4] + '.jpg'
    print('Plotting connections')
    plotConnections(level_posDic, networkList[:], floating_connections, figName = figure_name)  