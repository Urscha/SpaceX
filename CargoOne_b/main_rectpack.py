import math
import matplotlib
import sys
from operator import itemgetter
import random
import copy
from rectpack import *

# read data with additional values made in excell (ratio )
def read_data(input_file):
	data = []
	with open(input_file, 'r') as f:
		for line in f:
			i = line.split()
			for l in range(len(i)):
				if l%5==0:
					t = (int(i[l]), float(i[l+1]), float(i[l+2]), float(i[l+2])**4/float(i[l+1]), float(i[l+4]))
					data.append(t)
	return data

def kg_left(s):
	return s[5] - sum(item[1] for item in s[4])

def m3_left(s):
	return s[6] - sum(item[2] for item in s[4])

def update_ship(s):
	s[1] = kg_left(s)
	s[2] = m3_left(s)
	s[3] = float(s[1]) / float(s[2])

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

def init_ships():
	ships = [["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9],
			 ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1],
			 ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6],
			 ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]]

	for s in ships:
		update_ship(s)
	return ships

def packer_init(cargolist, ships):
	
	packer = newPacker(mode=PackingMode.Offline,
						bin_algo=PackingBin.BBF,
						rotation=False,
						sort_algo=SORT_RATIO)

	# add packages to the packing queue
	for r in cargolist:
		weight = float2dec(r[1], 0)
		volume = float2dec(r[2], 2)
		packer.add_rect(weight, volume, r[0])
	
	# add spacecrafts as bins
	for s in ships:
		payload_kg = float2dec(r[1], 0)
		payload_m3 = float2dec(r[2], 1)
		packer.add_bin(payload_kg, payload_m3)
	
	# start packing
	packer.pack()
	
	# Full rectangle list
	all_rects = packer.rect_list()
	for rect in all_rects:
		b, x, y, w, h, rid = rect
		print(rect)
	
	for i in range(len(packer)):
		n_packages = len(packer[i])
		print("there are", n_packages, "packages in ship", i)
		ship = packer[i]
		
#						   _____MAIN_____
def main():
	# initiale ships
	ships = init_ships()
	cargolist = read_data("CargoList1_b.txt")
	print_ships(ships)
	packer_init(cargolist, ships)
	
if __name__ == "__main__":
	main()
