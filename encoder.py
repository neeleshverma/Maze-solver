import sys

if len(sys.argv) <= 1:
	print "Please specify the grid file"
	exit(0)

file_name = sys.argv[1]

probability = 1.0
if len(sys.argv) == 3:
	# print "probability specified"
	probability = float(sys.argv[2])

# print file_name
# print probability

file = open(file_name, "r")

grid = []
while True:
	line = file.readline()
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

total_states = width * height
# print total_states
# L = 0, R = 1, U = 2, D = 3
total_actions = 4 

# dictionary = dict()
start_state = -1
end_state = []
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

# print actual_states

# for key, val in actual_states:
# 	print key, val,
# 	print actual_states[(key,val)]

# print actual_states

dictionary = [[[] for _ in range(total_actions)] for _ in range(total_states)]

for i in range(height):
	for j in range(width):
		if grid[i][j] == 1:
			# total_states -=1
			continue
		elif grid[i][j] == 2:
			start_state = actual_states[(i,j)]
		elif grid[i][j] == 3:
			end_state.append(actual_states[(i,j)])
			continue

		actions = []
		states = []
		cur_row = []
		cur_col = []

		if i > 0:
			if (grid[i-1][j] != 1):
				actions.append(2)
				# print "U"
				# print i, j
				# print actual_states[(i-1,j)]
				states.append(actual_states[(i-1,j)])
				cur_row.append(i-1)
				cur_col.append(j)

		if i < height-1:
			if (grid[i+1][j] != 1):
				actions.append(3)
				# print "D"
				# print i, j
				# print actual_states[(i+1,j)]
				states.append(actual_states[(i+1,j)])
				cur_row.append(i+1)
				cur_col.append(j)

		if j > 0:
			if (grid[i][j-1] != 1):
				actions.append(0)
				# print "L"
				# print i, j
				# print actual_states[(i,j-1)]
				states.append(actual_states[(i,j-1)])
				cur_row.append(i)
				cur_col.append(j-1)

		if j < width-1:
			if (grid[i][j+1] != 1):
				actions.append(1)
				# print "R"
				# print i, j
				# print actual_states[(i,j+1)]
				states.append(actual_states[(i,j+1)])
				cur_row.append(i)
				cur_col.append(j+1)

		total_act_cur_state = len(actions)

		for k in range(total_act_cur_state):
			for l in range(total_act_cur_state):
				if k==l:
					if grid[cur_row[k]][cur_col[l]] == 3:
						dictionary[i*width+j][actions[k]].append((states[k], 1.0, probability+(1.0-probability)/total_act_cur_state))
					else:
						dictionary[i*width+j][actions[k]].append((states[k], -1.0, probability+(1.0-probability)/total_act_cur_state))

				else:
					if probability == 1.0:
						continue
					if grid[cur_row[k]][cur_col[l]] == 3:
						dictionary[i*width+j][actions[k]].append((states[l], 1.0, (1.0-probability)/total_act_cur_state))
					else:
						dictionary[i*width+j][actions[k]].append((states[l], -1.0, (1.0-probability)/total_act_cur_state))

print "numStates", total_actual_states + 1
print "numActions", total_actions
print "start", start_state
print "end",
for i in range(len(end_state)):
	if i == len(end_state) - 1:
		print end_state[i]
	else:
		print end_state[i], 

# print ""

for i in range(total_states):
	for j in range(total_actions):
		for transition in dictionary[i][j]:
			x_coord = int(i/width)
			y_coord = i - x_coord * width
			print "transition", actual_states[(x_coord,y_coord)], j, transition[0], transition[1], transition[2]

# print dictionary
# for i in range(total_actions):
# 	for j in range(total_states):
# 		if dictionary[i][j] == []:
# 			print "Empty"

print "discount ", discount