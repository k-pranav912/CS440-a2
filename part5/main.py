from ast import Num
from http.client import NON_AUTHORITATIVE_INFORMATION
from turtle import color

import matplotlib.pyplot as plt
import numpy as np
import math

GRID_SIZE_COLS = 50
GRID_SIZE_ROWS = 100
GRID_SIZE = GRID_SIZE_COLS * GRID_SIZE_ROWS
NUM_WORLDS = 10
NUM_DATA = 10
NUM_ITERATIONS = 100
ITERATION_SCALE = 10

def main():
    userinput = input("Enter U to run UI, E to run error calculations, P to run probabilities calculations, Q to quit: ")
    if userinput == "U": UI()
    elif userinput == "E": errorCalc()
    elif userinput == "P": probabilityCalc()
    else: return
    
def UI():
    while(True):
        userinput = input("Enter the name of the world file, followed by a space, then the name of the data file to parse, or Q to quit: ")
        if userinput == "Q": return
        try: 
             parseFiles(userinput, displayUI=True)
        except:
             print("Invalid Path")
             continue
        break
    
def errorCalc():
    errors = []
    errorAvgs = []
    x = []
    for i in range(NUM_WORLDS):
        for j in range(NUM_DATA):
            temp = parseFiles("world" + str(i+1) + ".txt world" + str(i+1) + "_data" + str(j+1) + ".txt", calculateError=True)
            for m in range(len(temp)):
                errors.append(temp[m])

    for l in range(6, NUM_ITERATIONS):
        x.append(l)
        sum = 0
        for k in range(NUM_WORLDS*NUM_DATA):
            sum+= errors[(l-6) + (k*(NUM_ITERATIONS - 5))]
        errorAvgs.append(sum/(NUM_WORLDS * NUM_DATA))

    plt.scatter(x, errorAvgs, vmin=0, vmax=100)
    plt.show()

def probabilityCalc():
    x = []
    probabilities = []
    probabilitiesAvg = []
    for i in range(NUM_WORLDS):
        for j in range(NUM_DATA):
            temp = parseFiles("world" + str(i+1) + ".txt world" + str(i+1) + "_data" + str(j+1) + ".txt", calculateProbability=True)
            for m in range(len(temp)):
                probabilities.append(temp[m])

    for a in range(1, NUM_ITERATIONS):
        x.append(a)
        sum = 0
        for k in range(NUM_WORLDS*NUM_DATA):
            sum+= probabilities[a-1 + (k*(NUM_ITERATIONS))]
        probabilitiesAvg.append(sum/(NUM_WORLDS*NUM_DATA))
    
    plt.scatter(x, probabilitiesAvg, vmin=0, vmax=100)
    plt.show()

def parseFiles(fileName, displayUI=False, calculateError=False, calculateProbability=False):
    files = fileName.split()
    matWorld, matN, matH, matT, numNonBlocked = createReadingMatrices(str(files[0]))
    mat = createInitialMatrix(matWorld, numNonBlocked)
    values = []

    with open(str(files[1])) as data:
        positions = []
        for iteration in range(NUM_ITERATIONS + 1):
            positions.append(data.readline().split())

        actions = []
        for iteration in range(NUM_ITERATIONS):
            actions.append(str(data.readline()))
            
        readings = []
        for iteration in range(NUM_ITERATIONS):
            readings.append(str(data.readline()))
    
    for iteration in range(NUM_ITERATIONS):
        if actions[iteration] == "R\n": temp = rightMove(mat, matWorld)
        elif actions[iteration] == "L\n": temp = leftMove(mat, matWorld)
        elif actions[iteration] == "U\n": temp = upMove(mat, matWorld)
        else: temp = downMove(mat, matWorld)
        
        if readings[iteration] == "N\n": evidence = matN
        elif readings[iteration] == "H\n": evidence = matH
        else: evidence = matT
        mat = pointwiseMultiplication(temp, evidence)
        normalize(mat)
        
        if displayUI and (iteration == 0 or (iteration+1) % ITERATION_SCALE == 0):
            plt.title("Iteration " + str(iteration + 1))
            plt.imshow(mat, cmap='hot', interpolation='nearest')
            plt.show()

        if calculateError and iteration > 4:
            maxVal, coords = getMaxValue(mat)
            values.append(calcDistance(coords, positions[iteration+1]))

        if calculateProbability:
            i = int(positions[iteration+1][0])
            j = int(positions[iteration+1][1])
            values.append(mat[i][j])
    
    return values

def createInitialMatrix(matWorld, numNonBlocked):
    mat = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)]
    probabilityNonBlocked = 1 / numNonBlocked
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            if matWorld[i][j] < 3:
                mat[i][j] = probabilityNonBlocked
    return mat

def createReadingMatrices(worldName):
    numN = 0
    numH = 0
    numT = 0
    matWorld = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    matN = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    matH = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    matT = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 

    with open(worldName) as world:
        for i in range(GRID_SIZE_ROWS):
            line = world.readline()
            temp = line.split()
            for j in range(GRID_SIZE_COLS):
                if temp[j] == "N": 
                    numN+=1
                    matWorld[i][j] = 0
                elif temp[j] == "H": 
                    numH+=1
                    matWorld[i][j] = 1
                elif temp[j] == "T": 
                    numT+=1
                    matWorld[i][j] = 2
                else:
                    matWorld[i][j] = 3
            
            numNonBlocked = numN + numH + numT

        for i in range(GRID_SIZE_ROWS):
            for j in range(GRID_SIZE_COLS):
                if matWorld[i][j] == 0:
                    matN[i][j] = 0.9 / numN
                    matH[i][j] = 0.05 / numH
                    matT[i][j] = 0.05 / numT
                elif matWorld[i][j] == 1:
                    matN[i][j] = 0.05 / numN
                    matH[i][j] = 0.9 / numH
                    matT[i][j] = 0.05 / numT
                elif matWorld[i][j] == 2:
                    matN[i][j] = 0.05 / numN
                    matH[i][j] = 0.05 / numH
                    matT[i][j] = 0.9 / numT

    return matWorld, matN, matH, matT, numNonBlocked

def calcDistance(coords1, coords2):
    x1 = int(coords1[0])
    y1 = int(coords1[1])
    x2 = int(coords2[0])
    y2 = int(coords2[1])
    return math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))

def normalize(mat):
    sum = summation(mat)
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            mat[i][j] /= sum

def getMaxValue(mat):
    result = 0
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            temp = max(result, mat[i][j])
            if temp == mat[i][j]:
                result = temp
                coordinates = (i, j)
    return result, coordinates
    
def summation(mat):
    sum = 0
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            sum += mat[i][j]
    return sum

def pointwiseMultiplication(mat1, mat2):
    result = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            result[i][j] = mat1[i][j] * mat2[i][j]
    return result

def rightMove(mat, matWorld):
    result = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            if (matWorld[i][j] != 3):
                if (j == GRID_SIZE_COLS - 1) or (matWorld[i][j+1] == 3):
                    if (j == 0): result[i][j] = mat[i][j]
                    else: result[i][j] = mat[i][j] + mat[i][j-1] * 0.9

                elif (j == 0) or (matWorld[i][j-1] == 3):
                    result[i][j] = mat[i][j] * 0.1

                else:
                    result[i][j] = mat[i][j] * 0.1 + mat[i][j-1] * 0.9

    return result

def leftMove(mat, matWorld):
    result = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            if (matWorld[i][j] != 3):
                if (j == 0) or (matWorld[i][j-1] == 3):
                    if (j == GRID_SIZE_COLS - 1): result[i][j] = mat[i][j]
                    else: result[i][j] = mat[i][j] + mat[i][j+1] * 0.9

                elif (j == GRID_SIZE_COLS - 1) or (matWorld[i][j+1] == 3):
                    result[i][j] = mat[i][j] * 0.1

                else:
                    result[i][j] = mat[i][j] * 0.1 + mat[i][j+1] * 0.9

    return result

def upMove(mat, matWorld):
    result = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            if (matWorld[i][j] != 3):
                if (i == 0) or (matWorld[i-1][j] == 3):
                    if (i == GRID_SIZE_ROWS - 1): result[i][j] = mat[i][j]
                    else: result[i][j] = mat[i][j] + mat[i+1][j] * 0.9

                elif (i == GRID_SIZE_ROWS - 1) or (matWorld[i+1][j] == 3):
                    result[i][j] = mat[i][j] * 0.1

                else:
                    result[i][j] = mat[i][j] * 0.1 + mat[i+1][j] * 0.9

    return result

def downMove(mat, matWorld):
    result = [[0 for x in range(GRID_SIZE_COLS)] for y in range(GRID_SIZE_ROWS)] 
    for i in range(GRID_SIZE_ROWS):
        for j in range(GRID_SIZE_COLS):
            if (matWorld[i][j] != 3):
                if (i == GRID_SIZE_ROWS - 1) or (matWorld[i+1][j] == 3):
                    if (i == 0): result[i][j] = mat[i][j]
                    else: result[i][j] = mat[i][j] + mat[i-1][j] * 0.9

                elif (i == 0) or (matWorld[i-1][j] == 3):
                    result[i][j] = mat[i][j] * 0.1

                else:
                    result[i][j] = mat[i][j] * 0.1 + mat[i-1][j] * 0.9

    return result

if __name__ == "__main__":
    main()