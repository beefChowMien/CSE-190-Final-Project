# astar implementation needs to go here
import rospy
from std_msgs.msg import Bool
import json
from math import *
from cse_190_assi_3.msg import AStarPath
from read_config import read_config
import numpy as np
import Queue


class Node():
	def __init__(self, node, pos):
		self.parent = node
		self.pos = pos


def AStarSearch(start, goal, board):
		config = read_config()
		move_list = config["move_list"]
		mapWidth = config["map_size"][1]
		mapHeight = config["map_size"][0]	
		obstacles = []
		for i in range(mapHeight):
			for j in range(mapWidth):
				if board[i][j] == "WALL" or board[i][j] == "PIT":# or board[i][j] == "1" or board[i][j] == "2":
					obstacles.append([i, j])

		visited = []

		q = Queue.PriorityQueue()
		root = Node(None, start)
		q.put((manhattan_distance(start, goal), 0, root))
		

		while not q.empty():

			current = q.get()
			
			visited.append(current[2].pos)

			for move in move_list:
				next_move = [current[2].pos[0] + move[0], current[2].pos[1] + move[1]]
			
				if not is_valid(next_move, mapWidth, mapHeight, obstacles) or next_move in visited:
					continue
				new_node = Node(current[2], next_move)
				if next_move == goal:
					path = []
					while new_node != None:
						path.append(new_node.pos)
						new_node = new_node.parent

					path.reverse()
					
					return path

				q.put((current[1] + 1 + manhattan_distance(next_move, goal), current[1] + 1, new_node))
				
		
		return False


def is_valid(pos, mapWidth, mapHeight, obstacles):
		return pos[0] >= 0 and pos[0] < mapHeight and pos[1] >= 0 and pos[1] < mapWidth and pos not in obstacles
			

def manhattan_distance(pos, goal):
		return (abs(goal[0] - pos[0]) + abs(goal[1] - pos[1]))

