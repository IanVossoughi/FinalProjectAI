from PIL import Image
import random, time, copy, math
from random import randint, randrange, choice

def initMatrix(matrix, xSize, ySize):
    for i in range(ySize):
        matrix.append(list())
        for j in range(xSize):
            matrix[i].append(0)

def weightMap(weight):
    # if weight > 0:
#         return 0
#     return 255
    return int(round(255/(math.exp(float(weight)/2)), 0))            

def getRandLine(xSize, ySize):
    return (random.uniform(-1, 1), randint(0,xSize), randint(0,ySize), randint(0,1))

def randomizeLines(numLines, xSize, ySize):
    result = list();
    for i in range(numLines):
        result.append(getRandLine(xSize, ySize))
    return result
    
def getPixel(img, x, y):
    return img.getpixel((x,y))

def setPixel(img, x, y, value):
    img.putpixel((x, y), weightMap(value))
        
def fastDrawLines(lines, matrix, xSize, ySize):
    for line in lines:
        if(line[3] == 0): #(m, x0, y0, inverted)
            #not inverted
            for x in range(xSize): # y = m(x-x0) + y0
                yVal = int(round((x - line[1])*line[0] + line[2], 0))
                if(yVal >= 0 and yVal < ySize):
                    matrix[yVal][x] += 1
        else:
            #inverted
            for y in range(ySize): # x = m(y - y0) + x0
                xVal = int(round((y - line[2])*line[0] + line[1], 0))
                if(xVal >= 0 and xVal < xSize):
                    matrix[y][xVal] += 1

def getError(img, matrix, x, y):
    return abs(weightMap(matrix[y][x]) - getPixel(img, x, y))
                
def calcError(img, matrix, xSize, ySize):
    error = 0
    for y in range(ySize):
        for x in range(xSize):
            error += getError(img, matrix, x, y)
    return error

#adds a line and returns the change in total error that this action results in
def addLine(line, matrix, image, xSize, ySize):
    change = 0
    if(line[3] == 0): #(m, x0, y0, inverted)
        #not inverted
        for x in range(xSize): # y = m(x-x0) + y0
            y = int(round((x - line[1])*line[0] + line[2], 0))
            if(y >= 0 and y < ySize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] += 1
                change += getError(image, matrix, x, y) - oldErr
    else:
        #inverted
        for y in range(ySize): # x = m(y - y0) + x0
            x = int(round((y - line[2])*line[0] + line[1], 0))
            if(x >= 0 and x < xSize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] += 1
                change += getError(image, matrix, x, y) - oldErr
    return change

#adds a line and returns the change in total error that this action will results in
def removeLine(line, matrix, image, xSize, ySize):
    change = 0
    if(line[3] == 0): #(m, x0, y0, inverted)
        #not inverted
        for x in range(xSize): # y = m(x-x0) + y0
            y = int(round((x - line[1])*line[0] + line[2], 0))
            if(y >= 0 and y < ySize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] = max(matrix[y][x] - 1, 0)
                change += getError(image, matrix, x, y) - oldErr
    else:
        #inverted
        for y in range(ySize): # x = m(y - y0) + x0
            x = int(round((y - line[2])*line[0] + line[1], 0))
            if(x >= 0 and x < xSize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] = max(matrix[y][x] - 1, 0)
                change += getError(image, matrix, x, y) - oldErr
    return change
    
def drawMatrix(matrix, xSize, ySize):
    image = Image.new('L', (xSize, ySize))
    for y in range(ySize):
        for x in range(xSize):
            setPixel(image, x, y, matrix[y][x])
    image.show()

def main():
    matrix = list()
    img = Image.open("img/eye.jpg")
    xSize, ySize = img.size
    img.draft('L', img.size)
    
    initMatrix(matrix, xSize, ySize)
    lines = randomizeLines(100, xSize, ySize)
    fastDrawLines(lines, matrix, xSize, ySize)
    error = calcError(img, matrix, xSize, ySize)
    drawMatrix(matrix, xSize, ySize)

main()
