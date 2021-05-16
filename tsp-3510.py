#################################################
# CS 3510 TSP Project
# Contributers: Tucker von Holten, Tim Slanschek
#################################################

import math
import numpy as np
import sys
import time

# File input Stage
# Read all node information in this section
fileInputPath = ''
fileOutputPath = ''

if len(sys.argv) < 4:
    print ('CS3510-TSP.py <inputfile> <outputfile> <time>')
    sys.exit()
elif sys.argv[1] == "help":
    print ('CS3510-TSP.py <inputfile> <outputfile> <time>')
    sys.exit()

fileInputPath = sys.argv[1]
fileOutputPath = sys.argv[2]
numSeconds = int(sys.argv[3])

print ("Input file is ", fileInputPath)
print ("Output file is ", fileOutputPath)

try:
    inputFile = open(fileInputPath, "r")
except FileNotFoundError:
    print("No such file or directory: ", fileInputPath)
    sys.exit(2)

# Setup

# Set timer to run a certain amount of seconds
stopTime = time.time_ns() #Stopping time is the current time + given seconds in nanoseconds (1E+9)

stopTime += numSeconds * 1000000000
# We can index the list with the node number. The 0th index is not an actual node!
nodeList = []
lines = inputFile.readlines()
for line in lines:
    nodeList.append(line.split()[1:])
inputFile.close()
numNodes = len(nodeList)

# Precalculation Stage
# All node distances are calculated here and put into a 2d array
distanceArray = [([0] * numNodes) for _ in range(numNodes)]
for x in range(0, numNodes):
    for y in range(x, numNodes):
        if x != y:
            xsq = math.pow(float(nodeList[y][0]) - float(nodeList[x][0]), 2)
            ysq = math.pow(float(nodeList[y][1]) - float(nodeList[x][1]), 2)
            dist = round(math.sqrt(xsq + ysq))
            if (dist == 0):
                dist = 1
            distanceArray[x][y] = dist
            distanceArray[y][x] = dist

# print("distanceArray")
# print(distanceArray)


def sample_from_pmf(pmfList):
    cdf = np.cumsum(pmfList)
    rand = 1 - np.random.rand()
    for x in range(len(cdf)):
        if rand <= cdf[x]:
            return x

minTotalDistance = -1
minPath = []

nodePheromoneFrequency = [[1 for _ in range(numNodes)] for _ in range(numNodes)] 

# Run algorithm cycle
print("Algorithm is running for the next " + str(numSeconds) + " seconds. Please wait.")

antNum = 5
iter = 0
scale = 0.5
while stopTime > time.time_ns():
    # print(minTotalDistance)

    antCurrValidPaths = [list(range(0, numNodes)) for _ in range(antNum)]
    antCurrNode = []
    antDistanceTravelled = [0 for _ in range(antNum)]
    # print("antDistanceTravelled")
    # print(antDistanceTravelled)
    antPath = [[] for _ in range(antNum)]

    for ant in range(antNum):
        randStart = np.random.randint(0, numNodes)
        antCurrValidPaths[ant].remove(randStart)
        # print("antCurrValidPaths")
        # print(antCurrValidPaths)
        antCurrNode.append(randStart)
        # print("antCurrNode")
        # print(antCurrNode)
        antPath[ant].append(randStart + 1)
        # print("antPath")
        # print(antPath)

    while antCurrValidPaths[0]:
        for ant in range(antNum):
            # Get proportionally random node
            distances = [distanceArray[antCurrNode[ant]][x] for x in antCurrValidPaths[ant]]
            sumVal = sum(distances)
            inverse_distance = [1 / (distance / sumVal) for distance in distances]
            sum_perc = sum(inverse_distance)
            inverse_perc =  [perc / sum_perc for perc in inverse_distance]

            # Get pheromone values
            raw_pheromones = [nodePheromoneFrequency[antCurrNode[ant]][x] for x in antCurrValidPaths[ant]]
            
            # Combine values            
            percentages = [(raw_pheromones[x] * inverse_perc[x]) for x in range(len(antCurrValidPaths[ant]))]

            sum_percentages = sum(percentages)
            total_perc = [val / sum_percentages for val in percentages]
            
            # Sample
            randNode_index = sample_from_pmf(total_perc)
            randNode = antCurrValidPaths[ant][randNode_index]

            # Traverse graph
            antDistanceTravelled[ant] += distances[randNode_index]
            antPath[ant].append((randNode + 1))
            del antCurrValidPaths[ant][randNode_index]
            antCurrNode[ant] = randNode

    for ant in range(antNum):
        firstNode = antPath[ant][0] - 1
        antDistanceTravelled[ant] += distanceArray[antCurrNode[ant]][firstNode]
        # antPath[ant].append(firstNode)

    minDistances = np.array(antDistanceTravelled)
    sorted_indices = np.argsort(minDistances)

    # Ant work
    if minTotalDistance == -1:
        minTotalDistance = minDistances[sorted_indices[0]]
        minPath = antPath[sorted_indices[0]]
    elif minDistances[sorted_indices[0]] < minTotalDistance:
        minTotalDistance = minDistances[sorted_indices[0]]
        minPath = antPath[sorted_indices[0]]

    if ((iter % 100) == 0): 
        # print(nodePheromoneFrequency)
        print(minTotalDistance, minDistances[sorted_indices[0]], scale)
    # print(minPath)
    # print(antPath[sorted_indices[0]])

    for x in range(len(nodePheromoneFrequency)):
        for y in range(len(nodePheromoneFrequency)):
            nodePheromoneFrequency[x][y] = (nodePheromoneFrequency[x][y] + scale) * 0.98

    scale = scale * 0.9995

    curr_add = 1
    count = 0
    for currMin in sorted_indices:
        for i in range(len(antPath[currMin]) - 1):
            currPathNode = antPath[currMin][i] - 1
            nextPathNode = antPath[currMin][i + 1] - 1
            nodePheromoneFrequency[currPathNode][nextPathNode] = nodePheromoneFrequency[currPathNode][nextPathNode] + (curr_add - count)
            nodePheromoneFrequency[nextPathNode][currPathNode] = nodePheromoneFrequency[nextPathNode][currPathNode] + (curr_add - count)
        count += 0.2
    iter += 1

print("The final minimum distance found is: " + str(minTotalDistance))
print("The calculation ran for " + str(numSeconds) + " seconds.")

def compute_path_string(path):
    string = ""
    length = len(path)
    index = path.index(1)
    for i in range(length):
        string += str(path[(i + index) % length]) + " -> "    
    string += str(path[index])
    return string

# Make file output to file
outputFile = open(fileOutputPath, "w")
outputFile.write("The minimum computed distance over all " + str(numNodes) + " nodes was " + str(minTotalDistance) + ".\n")
outputFile.write("The minimum computed path:\n " + compute_path_string(minPath) + "\n")
outputFile.write("The calculation ran for " + str(numSeconds) + " seconds.\n")
outputFile.close()