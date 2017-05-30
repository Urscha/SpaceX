
import math
import matplotlib
import sys
from operator import itemgetter
import random
import copy
import time


# read data with additional values made in excell (ratio )
def read_data(input_file):
	data = []
	with open(input_file, 'r') as f:
		for line in f:
			i = line.split()
			for l in range(len(i)):
				if l%3==0:
					t = (int(i[l]), float(i[l+1]), float(i[l+2]), float(i[l+2])**4/float(i[l+1]), float(i[l+1])*float(i[l+2]))
					data.append(t)
	return data

def kg_left(s):
    return s[5] - sum(item[1] for item in s[4])


def m3_left(s):
    return s[6] - sum(item[2] for item in s[4])


def update_ship(s):
    s[1] = kg_left(s)
    s[2] = m3_left(s)
	
def fill_cargo_random(ships, data):
	for i in data:
		s = random.randint(0,len(ships)-1)
		ships[s][4].append(i)
	for sh in ships:
		update_ship(sh)
	return ships

# TODO :: define score
def cost(ships):
	totalkgleft = 0
	totalm3left = 0
	for s in ships:
		s[4].sort(key=itemgetter(4), reverse=True)
		#print s[4][4]
		m3left = s[6]
		kgleft = s[5]
		for item in s[4]:
			if (m3left - item[2]) > 0 and (kgleft - item[1]) > 0:
				m3left -= item[2]
				kgleft -= item[1]
		totalkgleft += kgleft
		totalm3left += m3left
	return (totalkgleft/11900 + totalm3left/53.6)/2

# TODO
def random_swap(ships):
	swapcount = random.randint(1,3)
	for i in range(swapcount):
		s1 = random.randint(0,3)
		s2 = random.randint(0,3)
		len1 = len(ships[s1][4]) - 1
		len2 = len(ships[s2][4]) - 1
		p1 = random.randint(0, len1)
		p2 = random.randint(0, len2)
		ships[s1][4][p1],ships[s2][4][p2] = ships[s2][4][p2], ships[s1][4][p1]
		update_ship(ships[s1])
		update_ship(ships[s2])
	return ships

# TODO
def acceptance_probability(old_cost, new_cost, T):
	return math.exp((old_cost - new_cost)/T) #2.71828

# TODO
def simulated_annealing(solution):
	# define variables for annealing
	T = 1.0
	T_min = 0.00001
	alpha = 0.9
	# save the current solution as the old solution
	old_solution = copy.deepcopy(solution)
	old_cost = cost(old_solution)
	# keep track of best solution
	best_solution = copy.deepcopy(solution)
	while T > T_min:
		i = 1
		while i <= 300:
			temp = copy.deepcopy(old_solution)
			new_solution = random_swap(temp)
			new_cost = cost(new_solution)
			ap = acceptance_probability(old_cost, new_cost, T)
			if ap > round(random.uniform(0.1, 1.0), 10):
				old_solution = copy.deepcopy(new_solution)
				old_cost = cost(old_solution)
			i += 1
		T = T * alpha
		print ("Temperature: %.5f" % T)
		print "Overall lowest cost: ", cost(best_solution)
		print "Current cost: ", old_cost ,"\n"
		# check if this solution should be saved as the overall best solution
		if old_cost < cost(best_solution):
			print("Updated best solution \n")
			best_solution = copy.deepcopy(old_solution)
	return best_solution

# prints ships
def print_ships(ships, score=True, cargo=False, errorcheck=False):
	svalue = 0
	for i in ships:
		print i[0],"item: ", len(i[4]), "\t kg: ", kg_left(i), "\t m3: ", m3_left(i)
		if(cargo):
			print "cargo: ", i[3], "\n"
		if(errorcheck):
			print i[1], i[2], "\n"
		if(score):
			svalue += (i[1]/i[5] + i[2]/i[6])*(100/2)
	if(score):
		print "average percentage filled: ",100 - svalue/float(len(ships)),"%\n"

# prints the cargo that is left
def print_cargoleft(ships, cargolist):
	item_left = len(cargolist) - sum(len(ships[i][4]) for i in range(len(ships)))
	print "Number of items left: ", item_left

# initializes the ships and data per ship
def init_ships():
	ships = [["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9],
			 ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1],
			 ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6],
			 ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]]

	for s in ships:
		update_ship(s)
	return ships


#						   _____MAIN_____
def main():
	# initiate ships
	ships = init_ships()
	cargolist = read_data("CargoList2.txt")
	print("Empty ships:")
	print_ships(ships)
	ships = fill_cargo_random(ships, cargolist)
	print("Randomly filled ships:")
	print_ships(ships)
	ships = simulated_annealing(ships)
	print("Ships filled:")
	print_ships(ships)
	print "Score ", 1 - cost(ships)
	print "Runtime ", time.clock() - start_time, "seconds"

if __name__ == "__main__":
	start_time = time.clock()
	main()
