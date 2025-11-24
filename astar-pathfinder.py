import pygame
from pygame.locals import *

pygame.init()

winWidth = 800

rows = 24

screen = pygame.display.set_mode((winWidth, winWidth))
clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
grey = (127,127,127)
purple = (255, 0, 255)

class Node:

    def __init__(self, pos, size, parent=None):
        self.parent = parent #node that this node comes from
        self.pos = pos #position in the grid data, pos[0] = row, pos[1] = col
        self.size = size #px size

        self.x = self.pos[0] * size
        self.y = self.pos[1] * size

        self.g = 0 #distance to start node
        self.h = 0 #distance to end node
        self.f = 0 #sum of g and h
        
        self.color = white
    
    def findNeighbours(self, grid, rows):
        neighbours = []
        if self.pos[0] > 0: #making sure the node is not at the very left side of grid
            left = grid[self.pos[0] - 1][self.pos[1]]
            neighbours.append(left)
        if self.pos[0] < (rows-1): #making sure the node is not at the very right of grid
            right = grid[self.pos[0] + 1][self.pos[1]]
            neighbours.append(right)
        if self.pos[1] > 0: #making sure the node is not at the very bottom of grid
            top = grid[self.pos[0]][self.pos[1] - 1]
            neighbours.append(top)
        if self.pos[1] < (rows-1): #making sure the node is not at the very top of grid
            bottom = grid[self.pos[0]][self.pos[1] + 1]
            neighbours.append(bottom)

        return neighbours
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

#def algorithm(start, end)

def makeGrid(width, rows):
    grid = []
    nodeSize = width / rows #px size of each node (float keeps full coverage)

    for i in range(rows): #rows
        grid.append([])
        for j in range(rows): #columns
            node = Node((i, j), nodeSize) #creating a node object for every grid square
            grid[i].append(node)
    
    return grid

def drawGrid(width, rows): #drawing lines to make up the grid
    size = width / rows
    
    for i in range(rows):
        pygame.draw.aaline(screen, grey, (0, i * size), (width, i * size)) #rows
    for j in range(rows):
        pygame.draw.aaline(screen, grey, (j * size, 0), (j * size, width)) #columns

def drawNodes(grid): 
    for row in grid:
        for node in row:
            node.draw()

def lowest(openList): #finds the node with the lowest f value 
    minList = []
    for obj in openList:
        minList.append(obj.f) #adds each element of the open list into a different list
    lowestX = min(minList) #finds the lowest value in the new list
    for obj in openList: #matches the lowest value from new list with a value in open list and returns it
        if obj.f == lowestX:
            lowestNode = obj
    return lowestNode

def getNodePos(mousePos, rows, width): #getting position of the node clicked within the grid by finding the pixel coordinates of the mouse position and converting it to the index coordinates of the node
    size = width / rows
    x, y = mousePos

    row = int(x // size)
    col = int(y // size)

    return row, col

def findPath(endNode): #once the end node is reached it back tracks its parents and appends each parent into a list
    pathList = []
    node = endNode

    while node is not None:
        pathList.append(node.pos)
        node = node.parent
    return pathList[::-1] #it then reverses the order of the grid to go back to the start


def algorithm(startNode, endNode, grid):
    openList = [] #initializing 2 empty lists of nodes
    closedList = []
    
    openList.append(startNode) #only adding the startnode passed thorugh the paremeter into the openList
    
    while len(openList) > 0: #loops through the openList until the end node is found

        currentNode = lowest(openList) #returns the element with the lowest f cost

        openList.remove(currentNode) #takes the element out of the open List and puts it in closed list meaning it has been calculated for already
        closedList.append(currentNode) 

        if currentNode == endNode: #if the end node is found then the find path function is called on the node
            pathList = findPath(currentNode)
            return pathList
        
        currentNeighbours = currentNode.findNeighbours(grid, rows) #finds the neighbours for the current node being looked at
        for neighbour in currentNeighbours:
            if neighbour.color == black: # checks if one of the nodes is an obstacle or has already been calculated for and skips forward to the other nodes
                continue
            if neighbour in closedList:
                continue 

            neighbour.parent = currentNode #defining the parent node as the current node so that the calculations can be made in reference to that
            neighbour.g = currentNode.g + 1 #g cost is distance between the neighbour and the current node
            neighbour.h = ((neighbour.pos[0] - endNode.pos[0])**2) + ((neighbour.pos[1] - endNode.pos[1])**2) #h cost is the distance between the neighbour and the end node
            neighbour.f = neighbour.g + neighbour.h #f cost is the h cost and g cost added up
            
            if neighbour not in openList: #if the neighbour is not in the open list it is appended into it so that it can be calaculated for later on
                openList.append(neighbour)
        

def main():
    
    grid = makeGrid(winWidth, rows) #defining the grid

    start = None #creating blank objects for start and end nodes
    end = None

    run = True
    while run: #game loop
        clock.tick(60)
        screen.fill(black)

        drawNodes(grid) #drawing grids
        drawGrid(winWidth, rows)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit() 
            

            if pygame.mouse.get_pressed()[0]: #when left mouse button is clicked
                mousePos = pygame.mouse.get_pos()
                r, c = getNodePos(mousePos, rows, winWidth) #getting the coords of node based on mouse position
                node = grid[r][c]
                if not start and node != end: #if the start node isn't defined and the node being hovered over is not ==end node it makes the node the start node
                    start = node
                    start.color = red
                elif not end and node != start: #same logic used for the start node
                    end = node
                    end.color = blue
                elif node != end and node != start: #after statr and end node are defined the new nodes clicked are obstacles
                    node.color = black
            
            if event.type == pygame.KEYDOWN:    #once space bar is pressed algorithm is run
                if event.key == K_SPACE:    
                    if start and end :

                        path = algorithm(start, end, grid) #running function

                        path.pop(0) #removing the first element of the path and the last ebcause it is the start node and end node
                        path.pop(len(path) - 1)
                        print(path)
                        print(grid)

                        for row in grid: #for each node in the path list the color become purple
                            for node in row:
                                for pos in path:
                                    if node.pos == pos:
                                        node.color = purple

        
        pygame.display.flip()

main()



