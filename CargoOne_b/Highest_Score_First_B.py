'''
This is the constructive algorithm 'Heaviest Score First' to solve problem B of the Space Freight case
By team SpaceX: Rico, Ellen, Urscha
'''

import math
import matplotlib
import sys
from operator import itemgetter

# initialize data and values to calculate maximal score and indices
score, kgpacked, m3packed = 0, 0, 0
total_weight_payload, total_volume_payload = 11850, 53.6
total_weight_cargo, total_volume_cargo  = 11895, 72.05
NAME, KG, M3, CARGO_SCORE, RATIO = 0, 1, 2, 3, 4

#					   _____FUNCTIONS_____

# read data
def read_data(inputfile):
	data = []
	with open(inputfile, 'r') as f:
		for line in f:
			i = line.split()
			for l in range(len(i)):
				if l%3==0:
					index, kg, m3 = int(i[l]), float(i[l+KG]), float(i[l+M3])
					score1 = float((kg/total_weight_cargo + m3/total_volume_cargo) / 2)
					ratio = int(kg/m3)
					data.append((index, kg, m3, score1, ratio))
	return data
	
# put package with highest score in ship with closest kg/m3 ratio
def fill_cargo(data, ships):
	global kgpacked, m3packed, score
	for i in data:
		if i[RATIO] < 140.7 and (ships[0][KG] - i[KG]) >= 0 and (ships [0][M3] - i[M3]) >= 0:
			ships[0][KG] -= i[KG]
			ships[0][M3] -= i[M3]
			kgpacked += i[KG]
			m3packed += i[M3]
			print "packing " , i[NAME] , " in ship " ,  ships[0][NAME]
		elif i[RATIO] < 223.5 and (ships[1][KG] - i[KG]) >= 0 and (ships [1][M3] - i[M3]) >= 0:
			ships[1][KG] -= i[KG]
			ships[1][M3] -= i[M3]
			kgpacked += i[KG]
			m3packed += i[M3]
			print "packing " , i[NAME] , " in ship " ,  ships[1][NAME]
		elif i[RATIO] < 587.22 and (ships[3][KG] - i[KG]) >= 0 and (ships [3][M3] - i[M3]) >= 0:
			ships[3][KG] -= i[KG]
			ships[3][M3] -= i[M3]
			kgpacked += i[KG]
			m3packed += i[M3]
			print "packing " , i[NAME] , " in ship " ,  ships[3][NAME]
		elif (ships[2][KG] - i[KG]) >= 0 and (ships [2][M3] - i[M3]) >= 0:
			ships[2][KG] -= i[KG]
			ships[2][M3] -= i[M3]
			kgpacked += i[KG]
			m3packed += i[M3]
			print "packing " , i[NAME] , " in ship " ,  ships[2][NAME]
		# see if leftover packages fit in ships
		elif (ships[1][KG] - i[KG]) >= 0 and (ships [1][M3] - i[M3]) >= 0:
			ships[1][KG] -= i[KG]
			ships[1][M3] -= i[M3]
			kgpacked += i[KG]
			m3packed += i[M3]
			print "packing " , i[NAME] , " in ship " ,  ships[1][NAME]
		else:
			print(i)
			score -= i[CARGO_SCORE]
			print "could not pack ", i[NAME]

# print leftover space in spaceships and score
def print_ships(ships):
	for i in ships:
		print i[NAME], "\t kg: ", i[KG], "\t m3: ", i[M3] , "\n"
	print(kgpacked)
	print(m3packed)
	score =  ((kgpacked / total_weight_cargo) + (m3packed / total_volume_payload)) / 2
	print "score = ", score * 100, " %\n"

#						   _____MAIN_____
def main():
	# initiate ships
	ships = [["Cygnus   ", 2000, 18.9, [], 2000, 18.9],
			 ["Verne_ATV", 2300, 13.1, [], 2300, 13.1],
			 ["Progress ", 2400,  7.6, [], 2400,  7.6],
			 ["Kounotori", 5200, 14.0, [], 5200, 14.0]]
	
	# read data
	cargolist = read_data('CargoList1.txt')
	
	print(cargolist)
	# sort packages: highest score on top
	cargolist.sort(key=itemgetter(CARGO_SCORE), reverse=True)
	
	#fill cargo
	fill_cargo(cargolist, ships)
	
	#print ships
	print_ships(ships)

if __name__ == "__main__":
	main()

