import sys
import copy

if len(sys.argv) <= 1:
	print "Please specify the mdp file"

file_name = sys.argv[1]
# print file_name

file = open(file_name, "r")

line1 = file.readline()
# print line1
total_states = int(line1.split(" ")[-1])
# print total_states

line2 = file.readline()
total_actions = int(line2.split(" ")[-1])
# print total_actions

line3 = file.readline()
start_state = int(line3.split(" ")[-1])
# print start_state

line4 = file.readline()[:-1]
no_terminal_states = False
end_states = line4.split(" ")
if end_states[1] == "-1":
	# print "No terminal states"
	no_terminal_states = True
else:
	end_states = end_states[1:]
	# print end_states
	end_states = [int(x) for x in end_states]
	# print end_states

################# Transitions ##################

# Dict contains (state1, action) : (state2, reward, probability)
dictionary = dict()

gamma = 0.0

while True:
	line = file.readline()
	line = line[:-1]
	line = line.split(" ")
	if line[0] == "discount":
		# print line[2]
		gamma = float(line[2])
		break
	else:
		line = line[1:]
		# print line
		# line = [int(x) for x in line]
		key = (int(line[0]),int(line[1]))
		value = (int(line[2]), float(line[3]), float(line[4]))
		if key in dictionary.keys():
			val = dictionary[key]
			val.append(value)
			dictionary[key] = val
		else:
			dictionary[key] = [value]

	if line == "":
		print "End of file : Gamma not specified"
		exit(0)
		break
file.close()

# print gamma
# print dictionary
value_function_current = []
value_function_previous = []
policy = []

completed_states = []

if not no_terminal_states:
	for end_state in end_states:
		completed_states.append(end_state)

for i in range(total_states):
	value_function_current.append(0)
	value_function_previous.append(0)
	policy.append(-1)

# print value_function
# print dictionary
iterations = 0
# print total_states
while True:
	# copy_value_function = copy.deepcopy(value_function)
	for i in range(total_states):
		if i in completed_states:
			continue
		max_value = -1 * float("inf")
		new_policy = -1
		for j in range(total_actions):
			key = (i,j)
			new_reward = 0.0
			if key in dictionary.keys():
				# print "Key found"
				state_reward_prob_list = dictionary[key]

				for k in range(len(state_reward_prob_list)):
					reached_state = state_reward_prob_list[k][0]
					reward = state_reward_prob_list[k][1]
					prob = state_reward_prob_list[k][2]
					new_reward = new_reward + prob*(reward + (gamma * value_function_previous[reached_state]))
					
				if new_reward >= max_value:
					max_value = new_reward
					new_policy = j
					# max_value = max(prob*(reward + (gamma * value_function[reached_state])), max_value)

			else:
				continue

		
		value_function_current[i] = max_value
		if abs(value_function_previous[i] - value_function_current[i]) <= 1e-16:
			completed_states.append(i)
		policy[i] = new_policy

	# print len(completed_states)
	iterations = iterations + 1
	# print completed_states
	value_function_previous = copy.deepcopy(value_function_current)
	if len(completed_states) == len(value_function_current):
		break

for i in range(len(value_function_current)):
	print value_function_current[i], policy[i]

print "iterations", iterations
# print iterations
# print dictionary

# tot_len = 0
# for key, value in dictionary:
# 	s = dictionary[(key,value)]
# 	tot_len += len(s)

# print tot_len