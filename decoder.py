import sys
import numpy as np
from copy import deepcopy

grid_file = sys.argv[1]
value_policy_file = sys.argv[2]

probability = 1.0
if len(sys.argv) == 4:
	probability = float(sys.argv[3])

gridFile = open(grid_file,"r")

grid = []

while True:
	line = gridFile.readline()
	if line == "":
		break
	else:
		line = line[:-1]
		line = line.split(" ")
		line = [int(x) for x in line]
		grid.append(line)

# print len(grid[1])
height = len(grid)
width = len(grid[0])

# L = 0, R = 1, U = 2, D = 3
total_actions = 4 

# dictionary = dict()
start_state = -1
end_state = -1
discount = 0.9

actual_states = dict()
total_actual_states = -1

for i in range(height):
	for j in range(width):
		if grid[i][j] == 1:
			continue
		else:
			total_actual_states += 1
			key = (i,j)
			value = total_actual_states
			actual_states[key] = value

for i in range(height):
	for j in range(width):
		if grid[i][j] == 2:
			start_state = i*width + j
		elif grid[i][j] == 3:
			end_state = i*width + j

# print actual_states
val_pol_file = open(value_policy_file, "r")
policy = []

for i in range(total_actual_states+1):
	line = val_pol_file.readline()
	line = line[:-1]
	line = line.split(" ")
	policy.append(int(line[1]))

# print policy
current = start_state
my_moves = []

while True:
	if current == end_state:
		break
	x_coord = int(current/width)
	y_coord = int(current%width)

	actions = []
	states = []

	if grid[x_coord][y_coord] != 1:
		# print grid[x_coord-1][y_coord]
		if y_coord > 0:
			if grid[x_coord][y_coord-1] != 1:
				actions.append(0)
				# states.append(actual_states[(i,j-1)])

		if y_coord < width-1:
			if grid[x_coord][y_coord+1] != 1:
				actions.append(1)
				# states.append(actual_states[(i,j+1)])

		if x_coord > 0:
			if grid[x_coord-1][y_coord] != 1:
				actions.append(2)
				# states.append(actual_states[(i-1,j)])

		if x_coord < width-1:
			if grid[x_coord+1][y_coord] != 1:
				actions.append(3)
				# states.append(actual_states[(i+1,j)])

		# print x_coord, y_coord
		probabilities = []
		# print current
		# print actions
		for action in actions:
			if policy[actual_states[x_coord,y_coord]] == action:
				probabilities.append(probability+(1-probability)/len(actions))

			else:
				probabilities.append((1-probability)/len(actions))
		# print probabilities
		stochast_move = np.random.choice(actions, 1, p=probabilities)
		my_moves.append(stochast_move)
		if stochast_move == 0:
			current-=1
		elif stochast_move == 1:
			current+=1
		elif stochast_move == 2:
			current-=width
		elif stochast_move == 3:
			current += width


for i in range(len(my_moves)):
	if my_moves[i] == 0:
		my_moves[i] = "W"
	elif my_moves[i] == 1:
		my_moves[i] = "E"
	elif my_moves[i] == 2:
		my_moves[i] = "N"
	elif my_moves[i] == 3:
		my_moves[i] = "S"

print " ".join(my_moves)