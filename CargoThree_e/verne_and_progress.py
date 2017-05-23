import math
import sys
from operator import itemgetter
import copy

TOTAL_CARGO_WEIGTH = 0 # total cargo weight
TOTAL_CARGO_VOLUME = 0 # total cargo volume
TOTAL_SHIPS_WEIGTH = 0 # total ships weight
TOTAL_SHIPS_VOLUME = 0 # total ships volume
number_of_progress  = 5
number_of_vernes = 91
NAME, KG, M3, RATIO, CARGO = 0, 1, 2, 3, 4

#					   _____FUNCTIONS_____

# read data with additional values made in excell (ratio )
def read_data(input_file):
	global _TOTAL_CARGO_WEIGTH, _TOTAL_CARGO_VOLUME
	data = []
	with open(input_file, 'r') as f:
		for line in f:
			i = line.split()
			for l in range(len(i)):
				if l%3==0:
					index = int(i[l])
					kg = float(i[l+1])
					m3 = float(i[l+2])
					ratio = int(kg/m3)
					data.append((index, kg, m3, ratio))
	TOTAL_CARGO_WEIGTH = sum(item[KG] for item in data)
	TOTAL_CARGO_VOLUME = sum(item[M3] for item in data)
	return data

def kg_left(s):
	return s[5] - sum(item[KG] for item in s[CARGO])

def m3_left(s):
	return s[6] - sum(item[M3] for item in s[CARGO])

# update weight and volume left in ship
def update_ship(s):
	s[KG] = kg_left(s)
	s[M3] = m3_left(s)

# Takes  a ship & item as aguments. Returns True if item fits, else False
def fits(ship, item):
	return (ship[KG] - item[KG] >= 0 and ship[M3] - item[M3] >= 0)
	
# putting the packages into the spacecrafts with the most free space
def fill_cargo(ships, cargolist):
	# sort cargolist 
	cargolist.sort(key=itemgetter(M3), reverse=True)
	# if package fits in ship, pack it
	for item in cargolist:
		# ship iterator
		i = 0
		# sort ships with most m3 left on top
		ships.sort(key=itemgetter(M3), reverse=True)
		while i < (len(ships)):
			if fits(ships[i], item):
				print "packing ", item[NAME], " in ship ",  ships[i][NAME]				
				ships[i][CARGO].append(item)
				update_ship(ships[i])
				break
			else:
				i += 1
			
# print information per ship
def print_ships(ships, cargo=False, errorcheck=False):
	svalue = 0
	total_packages = 0
	for s in ships:
		total_packages += len(s[CARGO])
		print s[NAME],"items: ", len(s[CARGO]), "\t kg: ", kg_left(s), "\t m3: ", m3_left(s)
	print "Total packages packed: " + str(total_packages)
			
def init_ships():
	global TOTAL_SHIPS_WEIGTH, TOTAL_SHIPS_VOLUME
	ships = []
	Verne_ATV = ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1]
	Progress = ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6]
	for i in range(number_of_vernes):
		ships.append(copy.deepcopy(Verne_ATV))
		ships[i][0] = "Verne_ATV_" + str(i)
	for i in range(number_of_progress):
		ships.append(copy.deepcopy(Progress))
		ships[number_of_vernes+i][0] = "Progress_" + str(i)
	for i in range(len(ships)):
		ships[i].append(i)
	TOTAL_SHIPS_WEIGTH = sum(s[KG] for s in ships[0:-1])
	TOTAL_SHIPS_VOLUME = sum(s[M3] for s in ships[0:-1])
	return ships

	#						   _____MAIN_____
def main():
	# read data
	cargolist = read_data("CargoList3.txt")
	# initiale ships
	ships =  init_ships()
	fill_cargo(ships, cargolist)
	
	# sort ships on their index number
	ships.sort(key=itemgetter(7))
	# print result
	print_ships(ships)
	
	total_kg_free = 0
	for ship in ships:
		total_kg_free += kg_left(ship)
	print(str(total_kg_free) + " kg left")
	
	total_m3_free = 0
	for ship in ships:
		total_m3_free += m3_left(ship)
	print(str(total_m3_free) + " m3 left")
	
	score = ((total_kg_free/(number_of_vernes*2300 + number_of_progress * 2400)) + 
			(total_m3_free/ (number_of_vernes *13.1 + number_of_progress * 7.6)))  / 2

	print("score: "  + str(1 - score))

if __name__ == "__main__":
	main()
