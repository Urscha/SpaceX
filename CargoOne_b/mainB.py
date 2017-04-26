
import math
import matplotlib
import sys
from operator import itemgetter


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
    return data


def kg_left(s):
    return s[5] - sum(item[1] for item in s[4])


def m3_left(s):
    return s[6] - sum(item[2] for item in s[4])


def update_ship(s):
    s[1] = kg_left(s)
    s[2] = m3_left(s)
    s[3] = float(s[1]) / float(s[2])


def which_ship_ratio(ships, item):
    ratio = item[4]
    s0 = (0, abs(ships[0][3] - ratio))
    s1 = (1, abs(ships[1][3] - ratio))
    s2 = (2, abs(ships[2][3] - ratio))
    s3 = (3, abs(ships[3][3] - ratio))
    sList = [s0, s1, s2, s3]
    sList.sort(key=itemgetter(1))
    for s in sList:
        if ships[s[0]][1]>item[1] and ships[s[0]][2]>item[2]:
            return s[0]

    return -1


# initiale ships, including their mass/volume ratio
def fill_cargo_ratio(ships, data):
    # sort packages: highest score on top
    data.sort(key=itemgetter(3), reverse=True)
    # put package with highest score in ship with closest kg/m3 ratio
    for i in data:
        s = which_ship_ratio(ships, i)
        if s == -1:
            continue
        ships[s][4].append(i)
        update_ship(ships[s])


def print_ships(ships, score=True, cargo=False, errorcheck=False):
    svalue = 0
    for i in ships:
        print i[0], "\t kg: ", kg_left(i), "\t m3: ", m3_left(i)
        if(cargo):
            print "cargo: ", i[3], "\n"
        if(errorcheck):
            print i[1], i[2], "\n"
        if(score):
            svalue += (i[1]/i[5] + i[2]/i[6])*(100/2)
    if(score):
        print "average percentage filled: ",100 - svalue/4.0,"%\n"


def init_ships():
    ships = [["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9],
             ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1],
             ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6],
             ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]]

    for s in ships:
        update_ship(s)
    return ships

#                           _____MAIN_____
def main():
    # initiale ships
    ships = init_ships()
    cargolist = read_data("CargoList1_b.txt")
    fill_cargo_ratio(ships, cargolist)
    print_ships(ships)

    ships2 = init_ships()
    cargolist = read_data("CargoList1_b2.txt")
    fill_cargo_ratio(ships2, cargolist)
    print_ships(ships2)



if __name__ == "__main__":
    main()
