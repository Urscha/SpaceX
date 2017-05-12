
import math
import matplotlib
import sys
from operator import itemgetter
import random
import copy
import time

_TOTAL_CARGO_WEIGTH = 0 # total cargo weigth
_TOTAL_CARGO_VOLUME = 0 # total cargo volume
_TOTAL_SHIPS_WEIGTH = 0 # total ships weight
_TOTAL_SHIPS_VOLUME = 0 # total ships volume

NAME, KG, M3, RATIO, CARGO = 0, 1, 2, 3, 4

# read data with additional values made in excell (ratio )
def read_data(input_file):
    global _TOTAL_CARGO_WEIGTH, _TOTAL_CARGO_VOLUME
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            i = line.split()
            for l in range(len(i)):
                if l%3==0:
                    index = float(i[l])
                    kg = float(i[l+1])
                    m3 = float(i[l+2])
                    ratio = kg/m3
                    data.append((index, kg, m3, ratio))
    _TOTAL_CARGO_WEIGTH = sum(item[KG] for item in data)
    _TOTAL_CARGO_VOLUME = sum(item[M3] for item in data)
    return data


def kg_left(s):
    return s[5] - sum(item[KG] for item in s[CARGO])


def m3_left(s):
    return s[6] - sum(item[M3] for item in s[CARGO])


# Takes sigle ship and updates the kg's and m3's that are left
def update_ship(s):
    s[1] = kg_left(s)
    s[2] = m3_left(s)


# Takes  a ship & item as aguments. Returns True if item fits, else False
def fits(ship, item):
    return (ship[KG] - item[KG] >= 0 and ship[M3] - item[M3] >= 0)


# First only the ships with an extreme ratio of kg/m3
def fill_ships_with_extreme_ratio(ships, data):
    pass


# Fills ships with random cargo untill they are full
def fill_cargo_random(ships, data):
    random.shuffle(data)
    for i in data:
        s = random.randint(0,len(ships) - 2)
        if fits(ships[s], i):
            ships[s][CARGO].append(i)
            update_ship(ships[s])
        else:
            ships[-1][CARGO].append(i)


# Takes all ships and returns average percentage that is not taken
def cost(ships):
    kgs_left = sum(item[KG] for item in ships[-1][CARGO])
    m3s_left = sum(item[M3] for item in ships[-1][CARGO])
    percentage_kg_filled = (_TOTAL_CARGO_WEIGTH - kgs_left)/_TOTAL_SHIPS_WEIGTH
    percentage_m3_filled = (_TOTAL_CARGO_VOLUME - m3s_left)/_TOTAL_SHIPS_VOLUME
    profit = ( percentage_kg_filled + percentage_m3_filled ) / 2
    cost = 1 - profit
    return cost


def random_swap(ships):
    # move items from ship A to cargo
    s1 = random.randint(0,len(ships)-2)
    l = len(ships[s1][CARGO]) - 1
    weigth = 0
    while weigth < 0.02 and l > 1:
        item = random.randint(0,l)
        ships[-1][CARGO].append(ships[s1][CARGO][item])
        weigth += (ships[s1][CARGO][item][KG]/11895 + ships[s1][CARGO][item][M3]/53.6)/2
        del ships[s1][CARGO][item]
        l -= 1

    update_ship(ships[s1])

    # move items from ship B to ship A
    s2 = random.randint(0,len(ships)-2)
    while s2 == s1:
        s2 = random.randint(0,len(ships)-2)
    counter = 0
    l = len(ships[s2][CARGO]) - 1
    while counter < 5 and l > 1:
        item = random.randint(0,l)
        if fits(ships[s1], ships[s2][CARGO][item]):
            ships[s1][CARGO].append(ships[s2][CARGO][item])
            del ships[s2][CARGO][item]
            update_ship(ships[s1])
            l -= 1
        else:
            counter += 1

    # move items from cargo to ship B
    counter = 0
    l = len(ships[-1][CARGO]) - 1
    while counter < 5 and l > 1:
        item = random.randint(0,l)
        if fits(ships[s2], ships[-1][CARGO][item]):
            ships[s2][CARGO].append(ships[-1][CARGO][item])
            del ships[-1][CARGO][item]
            l -= 1
            update_ship(ships[s2])
        else:
            counter += 1

    update_ship(ships[-1])
    return ships


# acceptance probability
def acceptance_probability(old_cost, new_cost, T):
    return math.exp((old_cost - new_cost)/T)

# simulated annealing
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
        while i <= 100:
            temp = copy.deepcopy(old_solution)
            new_solution = random_swap(temp)
            new_cost = cost(new_solution)
            # ap = acceptance_probability(old_cost, new_cost, T)
            # if ap > round(random.uniform(0.1, 1.0), 10):
            if new_cost < old_cost:
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
    svalue = 0
    for s in ships:
        print s[NAME],"item: ", len(s[CARGO]), "\t kg: ", kg_left(s), "\t m3: ", m3_left(s)



def print_cargoleft(ships, cargolist):
    item_left = len(cargolist) - sum(len(ships[i][CARGO]) for i in range(len(ships)))
    print "Number of items left: ", item_left


def mothership():
    ships = [["Mothership", _TOTAL_SHIPS_WEIGTH, _TOTAL_SHIPS_VOLUME, 0.0, [], _TOTAL_SHIPS_WEIGTH, _TOTAL_SHIPS_VOLUME],
            ["5th ship ", 1.e5  , 1.e4, 0.0, [],   1.e5, 1.e4]]
    update_ship(ships[0])
    return ships


def init_ships():
    global _TOTAL_SHIPS_WEIGTH, _TOTAL_SHIPS_VOLUME
    ships = []
    Cygnus = ["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9]
    Verne_ATV = ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1]
    Progress = ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6]
    Kounotori = ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]
    ThianZhou = ["ThianZhou", 6500.0, 15.0, 0.0, [], 6500.0, 15.0]
    Dragon = ["Dragon   ", 3400.0, 42.0, 0.0, [], 3400.0, 42.0]
    Cargo = ["5th_ship ", 1.e5  , 1.e4, 0.0, [],   1.e5, 1.e4]
    for i in range(10):
        ships.append(copy.deepcopy(Cygnus)*10)
        ships.append(copy.deepcopy(Verne_ATV))
        ships.append(copy.deepcopy(Progress))
        ships.append(copy.deepcopy(Kounotori))
        ships.append(copy.deepcopy(ThianZhou))
        ships.append(copy.deepcopy(Dragon))
    ships.append(Cargo)
    for s in ships:
        update_ship(s)
    _TOTAL_SHIPS_WEIGTH = sum(s[KG] for s in ships[0:-1])
    _TOTAL_SHIPS_VOLUME = sum(s[M3] for s in ships[0:-1])
    return ships

#                           _____MAIN_____
def main():
    # initiale ships
    ships = init_ships()
    #ships = mothership()
    cargolist = read_data("CargoList3.txt")
    print_ships(ships)
    fill_cargo_random(ships, cargolist)
    # print ships
    print_ships(ships)
    ships = simulated_annealing(ships)
    #print_cargoleft(ships, cargolist)
    #update_ship(ships[0])
    print_ships(ships)
    print "cargo in 5th ship: weight =", sum(s[1] for s in ships[-1][4]), ",\tvolume = ",sum(s[2] for s in ships[-1][4])
    print _TOTAL_CARGO_WEIGTH, _TOTAL_CARGO_VOLUME, _TOTAL_SHIPS_WEIGTH, _TOTAL_SHIPS_VOLUME
    print 1 - cost(ships)
    print "Runtime ", time.clock() - start_time, "seconds"

if __name__ == "__main__":
    start_time = time.clock()
    main()
