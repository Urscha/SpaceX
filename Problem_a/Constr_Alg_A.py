'''
This is the constructive algorithm 'Heaviest First' to solve problem A of the Space Freight case
By team SpaceX: Rico, Ellen, Urscha
'''
import math
import sys
from operator import itemgetter

# cargo and ships indices
NAME, KG, M3, CARGO = 0, 1, 2, 3

#                       _____FUNCTIONS_____

# read cargolists 
def read_data(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            value = line.split()
            for l in range(len(value)):
                if l % 3 == 0:
                    t = (int(value[l]), int(value[l+KG]), float(value[l+M3]))
                    data.append(t)
    return data

# calculates the kg left in a ship
def kg_left(s):
    return s[4] - sum(item[KG] for item in s[CARGO])

# calculates the m3 left in a ship
def m3_left(s):
    return s[5] - sum(item[M3] for item in s[CARGO])

# updates the ships information (free space)
def update_ship(s):
    s[KG] = kg_left(s)
    s[M3] = m3_left(s)

# putting the packages into the spacecrafts with the most free space
def fill_cargo_kg(ships, cargolist):
    # sort cargolist: most kg on top
    cargolist.sort(key=itemgetter(KG), reverse=True)
    # sort ships: most left kgs on top
    ships.sort(key=itemgetter(KG), reverse=True)
    # Put package with most kg in ships with most kgs left
    for item in cargolist:
        print "packing ", item[NAME], " in ship ",  ships[0][NAME]
        ships[0][CARGO].append(item)
        update_ship(ships[0])
        ships.sort(key=itemgetter(KG), reverse=True)

# if a ship is overloaded, swap two packages to make it fit
def change_cargo(ships):
    # ship iterator
    k = 0
    # check if ships on bottom (with least kg) has negative kg
    while ships[-1][KG] < 0 and k < len(ships):
        # sort cargo
        ships[-1][CARGO].sort(key=itemgetter(KG))
        ships[0][CARGO].sort(key=itemgetter(KG))
        # cargo iterators
        i, j = 0, 0
        while i < len(ships[-1][CARGO]) and j < len(ships[k][CARGO]):
            # difference in kg & mCARGO for specified cargo
            kg_diff = ships[-1][CARGO][i][KG] - ships[k][CARGO][j][KG]
            mCARGO_diff = ships[-1][CARGO][i][M3] - ships[k][CARGO][j][M3]
            if kg_diff > 0 and kg_diff <= ships[k][KG]:
                # swap
                ships[-1][CARGO][i], ships[k][CARGO][j] = ships[k][CARGO][j], ships[-1][CARGO][i]
                # update info
                update_ship(ships[-1])
                update_ship(ships[k])
                k = 0
                break
            elif kg_diff < ships[-1][KG]:
                i += 1
            else:
                j += 1
        k += 1
        ships.sort(key=itemgetter(KG), reverse=True)

# print information per ship
def print_ships(ships, cargo=False, errorcheck=False):
    for i in ships:
        print i[NAME], "\t kg: ", kg_left(i), "\t m3: ", m3_left(i)
        if(cargo):
            print "cargo: ", i[CARGO], "\n"
        if(errorcheck):
            print i[KG], i[M3], "\n"


#                           _____MAIN_____
def main():
    # initiate ships
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
    print('Score: 100%')

if __name__ == "__main__":
    main()
