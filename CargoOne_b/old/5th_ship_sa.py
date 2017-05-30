'''
This is the simulated annealing algorithm to solve problemB of the Space Freight case
By team SpaceX: Rico, Ellen, Urscha
'''
import math
import matplotlib
import sys
from operator import itemgetter
import random
import copy
import time

# ships indices
NAME, KG, M3, RATIO, CARGO, SIZE_KG, SIZE_M3 = 0, 1, 2, 3, 4, 5, 6

# available ships
Cygnus    = ["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9]
Verne_ATV = ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1]
Progress  = ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6]
Kounotori = ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]

# total values
CARGO_KG = 0
CARGO_M3 = 0
SHIPS_KG = 0
SHIPS_M3 = 0

# read data with additional values made in excell (ratio )
def read_data(input_file):
	global CARGO_KG, CARGO_M3
	data = []
	with open(input_file, 'r') as f:
		for line in f:
			i = line.split()
			for l in range(len(i)):
				if l%3==0:
					t = (int(i[l]), float(i[l+1]), float(i[l+2]))
					data.append(t)
	CARGO_KG = sum(item[1] for item in data)
	CARGO_M3 = sum(item[2] for item in data)
	return data


def kg_left(s):
	return s[5] - sum(item[1] for item in s[4])


def m3_left(s):
	return s[6] - sum(item[2] for item in s[4])


# Takes sigle ship and updates the kg's and m3's that are left
def update_ship(s):
	s[1] = kg_left(s)
	s[2] = m3_left(s)

# Takes  a ship & item as aguments. Returns True if item fits, else False
def fits(ship, item):
	return (ship[1] - item[1] >= 0 and ship[2] - item[2] >= 0)


# Fills ships randomly
def fill_cargo_random(ships, data):
    random.shuffle(data)
    for item in data:
        random.shuffle(ships[0:-1])
        for ship in ships:
            if fits(ship, item):
                ship[CARGO].append(item)
                update_ship(ship)

# Takes all ships and returns average percentage that is not taken
def cost(ships):
    kgs_taken = sum(ship[KG] for ship in ships[0:-1])
    m3s_taken = sum(ship[M3] for ship in ships[0:-1])
    percentage_kg_filled = kgs_taken / SHIPS_KG
    percentage_m3_filled = m3s_taken / SHIPS_M3
    return (percentage_kg_filled + percentage_m3_filled) / 2

def random_swap(ships):
	s = random.randint(0,len(ships)-2)
	l = len(ships[s][4]) - 1
	weigth = 0
	while weigth < 0.02:
		item = random.randint(0,l)
		ships[-1][4].append(ships[s][4][item])
		l -= 1
		weigth += (ships[s][4][item][1]/11895 + ships[s][4][item][2]/53.6)/2
		del ships[s][4][item]

	update_ship(ships[s])
	counter = 0
	l = len(ships[-1][4]) - 1
	while counter < 5:
		item = random.randint(0,l)
		if fits(ships[s], ships[-1][4][item]):
			ships[s][4].append(ships[-1][4][item])
			del ships[-1][4][item]
			l -= 1
			update_ship(ships[s])
		else:
			counter += 1

	update_ship(ships[-1])
	return ships

# acceptance probability
def acceptance_probability(old_cost, new_cost, T):
	return math.exp((old_cost - new_cost)/T)

# simulated annealing
def simulated_annealing(solution):
	T, T_min, alpha = 1.0, 1e-4, .9 # SA variables

	# save the current solution as the old solution
	old_solution = copy.deepcopy(solution)
	old_cost = cost(old_solution)
	best_solution = copy.deepcopy(solution)
	
	while T > T_min:
		i = 1
		while i <= 100:
			temp = copy.deepcopy(old_solution)
			new_solution = random_swap(temp)
			new_cost = cost(new_solution)
			ap = acceptance_probability(old_cost, new_cost, T)
			if ap > round(random.uniform(0.1, 1.0), 10):
				old_solution = copy.deepcopy(new_solution)
				old_cost = copy.deepcopy(new_cost)
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

def print_ships(ships):
    for s in ships:
        print s[NAME],"item: ", len(s[CARGO]), "\tkg: ", s[KG], "\tm3: ", s[M3]

def print_cargoleft(ships, cargolist):
    item_left = len(cargolist) - sum(len(ships[i][CARGO]) for i in range(len(ships)))
    print "Number of items left: ", item_left

def init_ships():
	global _sWEIGTH, SHIPS_M3
	ships = [["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9],
			 ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1],
			 ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6],
			 ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0],
			 ["5th_ship ", 1.e5  , 1.e4, 0.0, [],   1.e5, 1.e4]]
	for s in ships:
		update_ship(s)
 	_sWEIGTH = sum(s[1] for s in ships[0:-1])
	SHIPS_M3 = sum(s[2] for s in ships[0:-1])
	return ships

#						   _____MAIN_____
def main():
	# initiale ships
	ships = init_ships()
	cargolist = read_data("CargoList1.txt")
	print_ships(ships)
	fill_cargo_random(ships, cargolist)
	# print ships
	print_ships(ships)
	ships = simulated_annealing(ships)
	#print_cargoleft(ships, cargolist)
	print_ships(ships)
	print "cargo in 5th ship: weight =", sum(s[1] for s in ships[-1][4]), ",\tvolume = ",sum(s[2] for s in ships[-1][4])
	print _cWEIGTH, CARGO_M3, _sWEIGTH, SHIPS_M3
	print 1 - cost(ships)
	print "Runtime ", time.clock() - start_time, "seconds"

if __name__ == "__main__":
	start_time = time.clock()
	main()
