MAX_BRANCH = 70

def rrt(end, sampled, tree, path, nodes):
    
    #determining which node in the tree is closest
    nearest_node = None
    nearest_distance = 10000000 #intializing high value
    for q in tree:
        if (sampled.distance(q) < nearest_distance):
            nearest_node = q
            nearest_distance = sampled.distance(nearest_node)
    
    #if the node exceeds max branch length than pick a point on the line between them two
    if (nearest_distance > MAX_BRANCH):
        scale = MAX_BRANCH/nearest_distance
        dx = sampled.x - nearest_node.x
        dy = sampled.y - nearest_node.y
        sampled.x = nearest_node.x + (scale*dx)
        sampled.y = nearest_node.y + (scale*dy)
    
    if (not sampled.obstacle_between(nearest_node, nodes)):
        sampled.parent = nearest_node
        tree.append(sampled)
        nodes.append(sampled)
    
    #if the end node is reasonably close, return the path
    if (end.distance(sampled) < MAX_BRANCH):
        end.parent = sampled
        path.append(end)
        while sampled != None:
            path.append(sampled)
            sampled = sampled.parent
        return path
        

def rrt_star(end, sampled, tree, path, nodes):
    pass
