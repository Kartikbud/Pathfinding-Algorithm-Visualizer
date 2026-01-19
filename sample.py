import math
import pygame
from pygame.locals import *
from sample_algorithms import rrt, rrt_star
import random

pygame.init()

winWidth = 800
NODE_RADIUS = 15

screen = pygame.display.set_mode((winWidth, winWidth))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)  # baseline node color
BLACK = (0, 0, 0)  # obstacle color
RED = (255, 0, 0)  # end
BLUE = (0, 0, 255)  # start
GREY = (127, 127, 127)  # outlines
FRONTIER = (0, 200, 0)  # nodes/edges
PURPLE = (255, 0, 255)  # final path
BACKGROUND = (245, 245, 245)


class Node:
    def __init__(self, pos, radius=NODE_RADIUS, parent=None, cost=1000000):
        self.parent = parent  # node that this node comes from
        self.x = pos[0]
        self.y = pos[1]
        self.radius = radius
        self.is_obstacle = False

        self.color = WHITE

    def draw(self):
        center = (int(self.x), int(self.y))
        pygame.draw.circle(screen, self.color, center, self.radius)
        pygame.draw.circle(screen, GREY, center, self.radius, 1)

    def overlap(self, node): #checks if theres overlap between a sampled node and any other nodes
        dx = self.x - node.x
        dy = self.y - node.y
        return math.hypot(dx, dy) <= (self.radius + node.radius)

    def distance(self, node): #calculates the distance between 2 nodes
        dx = self.x - node.x
        dy = self.y - node.y
        return math.hypot(dx, dy)

    def obstacle_between(self, node, nodes): #determines if the edge between 2 nodes is collision free or not
        ax, ay = self.x, self.y
        bx, by = node.x, node.y
        dx = bx - ax
        dy = by - ay
        seg_len_sq = dx * dx + dy * dy

        for obs in nodes:
            if obs is self or obs is node:
                continue
            if obs.color != BLACK:
                continue
            cx, cy = obs.x, obs.y
            if seg_len_sq == 0:
                if math.hypot(cx - ax, cy - ay) <= obs.radius:
                    return True
                continue

            t = ((cx - ax) * dx + (cy - ay) * dy) / seg_len_sq
            if t < 0:
                closest_x, closest_y = ax, ay
            elif t > 1:
                closest_x, closest_y = bx, by
            else:
                closest_x = ax + t * dx
                closest_y = ay + t * dy

            if math.hypot(cx - closest_x, cy - closest_y) <= obs.radius:
                return True

        return False


def drawNodes(nodes, start, end, path):
    path_set = set(path)
    for node in nodes:
        if node.is_obstacle:
            node.color = BLACK
        elif node == start:
            node.color = RED
        elif node == end:
            node.color = BLUE
        elif node in path_set:
            node.color = PURPLE
        else:
            node.color = FRONTIER
        if node.parent:
            line_color = (
                PURPLE
                if node in path_set and node.parent in path_set
                else FRONTIER
            )
            pygame.draw.line(
                screen,
                line_color,
                (int(node.x), int(node.y)),
                (int(node.parent.x), int(node.parent.y)),
                2,
            )
        node.draw()

def sampleNode(nodes): #only returning a node if it is a valid node and not colliding with anything
    x = random.randint(0, 799)
    y = random.randint(0, 799)
    n = Node([x,y])
    for node in nodes:
        if (n.overlap(node)):
            return sampleNode(nodes)
    
    return n

def main():
    nodes = []

    start = None  # creating blank objects for start and end nodes
    end = None
    finalized = False
    awaiting_algorithm = False
    algorithm = None
    algorithm_running = False
    tree = []
    path = []
    algorithm_step_delay_frames = 6
    algorithm_step_counter = 0

    dragging_obstacle = None

    run = True
    while run:  # game loop
        clock.tick(60)
        screen.fill(BACKGROUND)

        drawNodes(nodes, start, end, path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not finalized:
                mousePos = event.pos
                if not start:  # if the start node isn't defined
                    start = Node(mousePos)
                    start.color = RED
                    nodes.append(start)
                elif not end:  # same logic used for the start node
                    end = Node(mousePos)
                    end.color = BLUE
                    nodes.append(end)
                else:  # after start and end node are defined the new nodes clicked are obstacles
                    dragging_obstacle = Node(mousePos, radius=1)
                    dragging_obstacle.color = BLACK
                    dragging_obstacle.is_obstacle = True
                    nodes.append(dragging_obstacle)

            if event.type == pygame.MOUSEMOTION and dragging_obstacle:
                mousePos = event.pos
                dx = mousePos[0] - dragging_obstacle.x
                dy = mousePos[1] - dragging_obstacle.y
                dragging_obstacle.radius = max(5, int(math.hypot(dx, dy)))

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_obstacle = None

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE and start and end and not finalized:
                    finalized = True
                    awaiting_algorithm = True
                elif awaiting_algorithm and event.key in (K_1, K_2):
                    if event.key == K_1:
                        algorithm = rrt
                    else:
                        algorithm = rrt_star
                    awaiting_algorithm = False
                    algorithm_running = True
                    tree = [start]
                    path = []
                    start.parent = None

        if algorithm_running and algorithm:
            algorithm_step_counter += 1
            if algorithm_step_counter >= algorithm_step_delay_frames:
                algorithm_step_counter = 0
                sampled = sampleNode(nodes)
                result = algorithm(end, sampled, tree, path, nodes)
                if result:
                    algorithm_running = False

        pygame.display.flip()


main()
