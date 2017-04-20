import math
import sys
from operator import itemgetter

#                       _____FUNCTIONS_____


def read_data(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            value = line.split()
            for l in range(len(value)):
                if l % 3 == 0:
                    t = (int(value[l]), int(value[l+1]), float(value[l+2]))
                    data.append(t)
    return data


def kg_left(s):
    return s[4] - sum(item[1] for item in s[3])


def m3_left(s):
    return s[5] - sum(item[2] for item in s[3])


def update_ship(s):
    s[1] = kg_left(s)
    s[2] = m3_left(s)


def fill_cargo_kg(ships, cargolist):
    # sort cargolist: most kg on top
    cargolist.sort(key=itemgetter(1), reverse=True)
    # sort ships: most left kgs on top
    ships.sort(key=itemgetter(1), reverse=True)
    # Put package with most kg in ships with most kgs left
    for item in cargolist:
        print "packing ", item[0], " in ship ",  ships[0][0]
        ships[0][3].append(item)
        update_ship(ships[0])
        ships.sort(key=itemgetter(1), reverse=True)


def change_cargo(ships):
    # ship iterator
    k = 0
    # check if ships on bottom (with least kg) has negative kg
    while ships[-1][1] < 0 and k < len(ships):
        # sort cargo
        ships[-1][3].sort(key=itemgetter(1))
        ships[0][3].sort(key=itemgetter(1))
        # cargo iterators
        i, j = 0, 0
        while i < len(ships[-1][3]) and j < len(ships[k][3]):
            # difference in kg & m3 for specified cargo
            kg_diff = ships[-1][3][i][1] - ships[k][3][j][1]
            m3_diff = ships[-1][3][i][2] - ships[k][3][j][2]
            if kg_diff > 0 and kg_diff <= ships[k][1]:
                # swap
                ships[-1][3][i], ships[k][3][j] = ships[k][3][j], ships[-1][3][i]
                # update info
                update_ship(ships[-1])
                update_ship(ships[k])
                k = 0
                # print "changed cargo: ", ships[0], "<-> ", temp2[0]
                break
            elif kg_diff < ships[-1][1]:
                i += 1
            else:
                j += 1
        k += 1
        ships.sort(key=itemgetter(1), reverse=True)


def print_ships(ships, cargo=False, errorcheck=False):
    for i in ships:
        print i[0], "\t kg: ", kg_left(i), "\t m3: ", m3_left(i)
        if(cargo):
            print "cargo: ", i[3], "\n"
        if(errorcheck):
            print i[1], i[2], "\n"


#                           _____MAIN_____
def main():
    # initiale ships
    ships = [["Cygnus   ", 2000, 18.9, [], 2000, 18.9],
             ["Verne_ATV", 2300, 13.1, [], 2300, 13.1],
             ["Progress ", 2400,  7.6, [], 2400,  7.6],
             ["Kounotori", 5200, 14.0, [], 5200, 14.0]]

    # read data
    cargolist = read_data("CargoList1.txt")

    # distibute cargo
    fill_cargo_kg(ships, cargolist)
    change_cargo(ships)

    # print result
    print_ships(ships)

if __name__ == "__main__":
    main()
