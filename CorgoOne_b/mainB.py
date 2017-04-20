
import math
import matplotlib
import sys
from operator import itemgetter

# initialize maximal score
score = 10786.35

# read data with additional values made in excell (ratio )
def read_data(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            elements = line.split()
            for l in range(len(elements)):
                if l%5==0:
                    t = (int(elements[l]), int(elements[l+1]), float(elements[l+2]), float(elements[l+3]), float(elements[l+4]))
                    data.append(t)

# initiale ships, including their mass/volume ratio
def fill_cargo_ratio(ships, data):
    # sort packages: highest score on top
    data.sort(key=itemgetter(3), reverse=True)

    # put package with highest score in ship with closest kg/m3 ratio
    for i in data:
        if i[4] < 140.7 and (ships[0][1] - i[1]) >= 0 and (ships [0][2] - i[2]) >= 0:
            ships[0][1] -= i[1]
            ships[0][2] -= i[2]
            print "packing " , i[0] , " in ship " ,  ships[0][0]
        elif i[4] < 223.5 and (ships[1][1] - i[1]) >= 0 and (ships [1][2] - i[2]) >= 0:
            ships[1][1] -= i[1]
            ships[1][2] -= i[2]
            print "packing " , i[0] , " in ship " ,  ships[1][0]
        elif i[4] < 587.22 and (ships[3][1] - i[1]) >= 0 and (ships [3][2] - i[2]) >= 0:
            ships[3][1] -= i[1]
            ships[3][2] -= i[2]
            print "packing " , i[0] , " in ship " ,  ships[3][0]
        elif (ships[2][1] - i[1]) >= 0 and (ships [2][2] - i[2]) >= 0:
            ships[2][1] -= i[1]
            ships[2][2] -= i[2]
            print "packing " , i[0] , " in ship " ,  ships[2][0]
        # see if leftover packages fit in ships
        elif (ships[1][1] - i[1]) >= 0 and (ships [1][2] - i[2]) >= 0:
            ships[1][1] -= i[1]
            ships[1][2] -= i[2]
            print "packing " , i[0] , " in ship " ,  ships[1][0]
        else:
            score -= i[3]
            print "could not pack ", i[0]


def print_ships(ships, cargo=False, errorcheck=False):
    for i in ships:
        print i[0], "\t kg: ", kg_left(i), "\t m3: ", m3_left(i)
        if(cargo):
            print "cargo: ", i[3], "\n"
        if(errorcheck):
            print i[1], i[2], "\n"

#                           _____MAIN_____
def main():
    ships = [["Cygnus", 2000, 18.9, 105.82,[]], ["Verne_ATV", 2300, 13.1, 175.57,[]], ["Progress", 2400, 7.6, 315.79,[]], ["Kounotori",5200, 14, 271.43,[]]]

    cargolist = read_data("CargoList1_b.txt")
    fill_cargo_ratio(ships, cargolist)
    print_ships(ships)
    print "score = ", score, "\n"


if __name__ == "__main__":
    main()
