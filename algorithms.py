WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREY = (127,127,127)
PURPLE = (255, 0, 255)

def dfs(start, end, grid, frontier, closed, path): #with memoization as i am caching the visited nodes and not revisting
    currentNode = frontier.pop()
    closed.add(currentNode)

    #add color for closed set here later

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

def bfs(start, end, grid, frontier, closed, path):
    return []

def a_star(start, end, grid, frontier, closed, path):
    return []
