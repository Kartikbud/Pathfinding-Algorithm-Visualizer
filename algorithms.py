import heapq

def heuristic(node, end):
    dx = end.pos[0] - node.pos[0]
    dy = end.pos[1] - node.pos[1]
    return dx**2 + dy**2

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREY = (127,127,127)
PURPLE = (255, 0, 255)

#each algorithm is going step by step as they are being called in the game loop under the condition that the frontier isnt empty

def dfs(start, end, grid, frontier, closed, path): #with memoization as i am caching the visited nodes and not revisting
    currentNode = frontier.pop()
    closed.add(currentNode)


    neighbours = currentNode.findNeighbours(grid)

    for node in neighbours:
        if (node == end): 
            end.parent = currentNode
            while node != None:
                path.append(node)
                node = node.parent
            
            return path        
        
        if (node.color == BLACK or node in closed): #skip node if its an obstacle or if its already been visited
            continue

        temp_g = currentNode.g + 1
        if temp_g < node.g and temp_g < end.g:
            node.g = temp_g
            node.parent = currentNode
            frontier.append(node)

def bfs(start, end, grid, frontier, closed, path): #this is esesntially the exact same as dfs except it usees a queue instead of stack
    currentNode = frontier.get()
    closed.add(currentNode)


    neighbours = currentNode.findNeighbours(grid)

    for node in neighbours:
        if (node == end): 
            end.parent = currentNode
            while node != None:
                path.append(node)
                node = node.parent
            
            return path        
        
        if (node.color == BLACK or node in closed): #skip node if its an obstacle or if its already been visited
            continue

        temp_g = currentNode.g + 1
        if temp_g < node.g and temp_g < end.g:
            node.g = temp_g
            node.parent = currentNode
            frontier.put(node)

def a_star(start, end, grid, frontier, closed, path):

    currentNode = heapq.heappop(frontier)[3]
    closed.add(currentNode)

    neighbours = currentNode.findNeighbours(grid)

    for node in neighbours:
        if (node == end): 
            end.parent = currentNode
            while node != None:
                path.append(node)
                node = node.parent
            
            return path        
        
        if (node.color == BLACK or node in closed): #skip node if its an obstacle or if its already been visited
            continue

        temp_g = currentNode.g + 1
        if temp_g < node.g and temp_g < end.g:
            node.g = temp_g
            node.parent = currentNode
            node.h = heuristic(node, end)
            node.f = node.g + node.h
            heapq.heappush(frontier, (node.f, -node.g, node.pos, node))
    
    return []
