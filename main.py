import pygame
from pygame.locals import *
from algorithms import dfs, bfs, a_star

from queue import Queue
import heapq

pygame.init()

winWidth = 800
ROWS = 24

screen = pygame.display.set_mode((winWidth, winWidth))
clock = pygame.time.Clock()

WHITE = (255,255,255) #baseline grid color
BLACK = (0,0,0) #obstacle color
RED = (255,0,0) #end
BLUE = (0,0,255) #start
GREY = (127,127,127) #lines
PURPLE = (255, 0, 255) #final path
FRONTIER = (0, 200, 0) #frontier/open set
CLOSED = (255, 140, 0) #closed/visited set

class Node:

    def __init__(self, pos, size, parent=None, cost=1000000):
        self.parent = parent #node that this node comes from
        self.pos = pos #position in the grid data, pos[0] = row, pos[1] = col
        self.size = size #px size

        self.x = self.pos[0] * size
        self.y = self.pos[1] * size

        self.g = cost #distance to start node (cost to arrive); have to initialize high

        ##for a star specifically
        self.h = 0 #distance to end node (cost to go)
        self.f = self.g + self.h #sum of the two
        
        self.color = WHITE
    
    def findNeighbours(self, grid):
        neighbours = []
        if self.pos[0] > 0: #making sure the node is not at the very left side of grid
            left = grid[self.pos[0] - 1][self.pos[1]]
            neighbours.append(left)
        if self.pos[0] < (ROWS-1): #making sure the node is not at the very right of grid
            right = grid[self.pos[0] + 1][self.pos[1]]
            neighbours.append(right)
        if self.pos[1] > 0: #making sure the node is not at the very bottom of grid
            top = grid[self.pos[0]][self.pos[1] - 1]
            neighbours.append(top)
        if self.pos[1] < (ROWS-1): #making sure the node is not at the very top of grid
            bottom = grid[self.pos[0]][self.pos[1] + 1]
            neighbours.append(bottom)

        return neighbours
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


def makeGrid(width):
    grid = []
    nodeSize = width / ROWS #px size of each node (float keeps full coverage)

    for i in range(ROWS): #rows
        grid.append([])
        for j in range(ROWS): #columns
            node = Node((i, j), nodeSize) #creating a node object for every grid square
            grid[i].append(node)
    
    return grid

def drawGrid(width): #drawing lines to make up the grid
    size = width / ROWS
    
    for i in range(ROWS):
        pygame.draw.aaline(screen, GREY, (0, i * size), (width, i * size)) #rows
    for j in range(ROWS):
        pygame.draw.aaline(screen, GREY, (j * size, 0), (j * size, width)) #columns

def drawNodes(grid): 
    for row in grid:
        for node in row:
            node.draw()

def getNodePos(mousePos, width): #getting position of the node clicked within the grid by finding the pixel coordinates of the mouse position and converting it to the index coordinates of the node
    size = width / ROWS
    x, y = mousePos

    row = int(x // size)
    col = int(y // size)

    return row, col

def heuristic(node, end):
        dx = end.pos[0] - node.pos[0]
        dy = end.pos[1] - node.pos[1]
        return dx**2 + dy**2

def updateColors(grid, start, end, frontier, closed, path):
    if hasattr(frontier, "queue"):
        frontier_items = list(frontier.queue)
    else:
        frontier_items = list(frontier)
    frontier_nodes = []
    for item in frontier_items:
        if isinstance(item, tuple):
            frontier_nodes.append(item[-1])
        else:
            frontier_nodes.append(item)
    frontier_set = set(frontier_nodes)
    path_set = set(path)
    for row in grid:
        for node in row:
            if node == start:
                node.color = RED
                continue
            if node == end:
                node.color = BLUE
                continue
            if node.color == BLACK and node not in frontier_set and node not in closed and node not in path_set:
                continue
            if node in path_set:
                node.color = PURPLE
            elif node in closed:
                node.color = CLOSED
            elif node in frontier_set:
                node.color = FRONTIER
            else:
                node.color = WHITE

def main():
    
    grid = makeGrid(winWidth) #defining the grid

    start = None #creating blank objects for start and end nodes
    end = None
    finalized = False
    awaiting_algorithm = False
    path_positions = []
    path_index = 0
    animating_path = False
    frontier = []
    closed = set()
    path = []
    algorithm_running = False
    algorithm = None
    step_delay_frames = 3
    step_counter = 0

    run = True
    while run: #game loop
        clock.tick(60)
        screen.fill(BLACK)

        drawNodes(grid) #drawing grids
        drawGrid(winWidth)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit() 
            

            if not finalized and pygame.mouse.get_pressed()[0]: #when left mouse button is clicked
                mousePos = pygame.mouse.get_pos()
                r, c = getNodePos(mousePos, winWidth) #getting the coords of node based on mouse position
                node = grid[r][c]
                if not start and node != end: #if the start node isn't defined and the node being hovered over is not ==end node it makes the node the start node
                    start = node
                    start.color = RED
                elif not end and node != start: #same logic used for the start node
                    end = node
                    end.color = BLUE
                elif node != end and node != start: #after statr and end node are defined the new nodes clicked are obstacles
                    node.color = BLACK
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    if start and end and not finalized:
                        finalized = True
                        awaiting_algorithm = True
                elif awaiting_algorithm and event.key in (K_1, K_2, K_3):
                    if event.key == K_1:
                        algorithm = dfs
                    elif event.key == K_2:
                        algorithm = bfs
                    else:
                        algorithm = a_star

                    #INITIALIZATION
                    start.g = 0
                    if (algorithm == dfs):
                        frontier = [] #treating this list as a stack with LIFO, will only use append and pop (both O(1))
                        frontier.append(start)
                    elif (algorithm == bfs):
                        frontier = Queue() #using queue as bfs is FIFO, will only use put and get which are O(1)
                        frontier.put(start)
                    else:
                        frontier = [] #this is the heap
                        start.h = heuristic(start, end)
                        start.f = start.g + start.h
                        heapq.heappush(frontier, (start.f, -start.g, start.pos, start))


                    #initing the path
                    path = []

                    closed = set() #if node was visited, using a set so lookup is only O(1) to check if node is in it rather than list which is O(n)
                    algorithm_running = True
                    awaiting_algorithm = False

        if algorithm_running:
            if frontier and algorithm:
                step_counter += 1
                if step_counter >= step_delay_frames:
                    step_counter = 0
                    algorithm(start, end, grid, frontier, closed, path)
                    if path:
                        algorithm_running = False
            else:
                algorithm_running = False
                step_counter = 0

        if finalized and (frontier or closed or path):
            updateColors(grid, start, end, frontier, closed, path)
        pygame.display.flip()

main()
