import math
import matplotlib
import sys
from operator import itemgetter
import random
import copy
import time
import numpy as np

# ships indices
NAME, KG, M3, RATIO, CARGO, SIZE_KG, SIZE_M3 = 0, 1, 2, 3, 4, 5, 6


# available ships
available_ships =  [["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9, 0],
                    ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1, 0],
                    ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6, 0],
                    ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0, 0],
                    ["ThianZhou", 6500.0, 15.0, 0.0, [], 6500.0, 15.0, 0],
                    ["Dragon   ", 3400.0, 42.0, 0.0, [], 3400.0, 42.0, 0]]


# available ships
Cygnus    = ["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9]
Verne_ATV = ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1]
Progress  = ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6]
Kounotori = ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]
ThianZhou = ["ThianZhou", 6500.0, 15.0, 0.0, [], 6500.0, 15.0]
Dragon    = ["Dragon   ", 3400.0, 42.0, 0.0, [], 3400.0, 42.0]

# total values
CARGO_KG = 0
CARGO_M3 = 0
SHIPS_KG = 0
SHIPS_M3 = 0



# read data
def read_data(input_file, data):
    global CARGO_KG, CARGO_M3
    with open(input_file, 'r') as f:
        for line in f:
            i = line.split()
            for l in range(len(i)):
                if l%3==0:
                    index, kg, m3 = int(i[l]), float(i[l+1]), float(i[l+2])
                    ratio = int(kg/m3)
                    data.append((index, kg, m3, ratio))
    CARGO_KG = sum(item[KG] for item in data)
    CARGO_M3 = sum(item[M3] for item in data)


def write_packing_list(ships):
    # extraships = []
    # for ship in available_ships:
    #     if ship[-1] == 1:
    #         extraships.append(ship[NAME])
    ships[0:-1].sort(key=itemgetter(NAME))
    with open("packinglist.txt", "w") as f:
        for ship in ships[0:-1]:
            f.write("\nName:\t" + ship[NAME] + "\tITEMS:\t")
            for item in ship[CARGO]:
                f.write(str(item[NAME]) + "\t")


# update weight and volume left in ship
def update_ship(s):
    s[KG] = s[SIZE_KG] - sum(item[KG] for item in s[CARGO])
    s[M3] = s[SIZE_M3] - sum(item[M3] for item in s[CARGO])
    if s[M3] != 0:
        s[RATIO] = int(s[KG]/s[M3])


# returns true if item fits in ship
def fits(ship, item):
    return (ship[KG] - item[KG] >= 0 and ship[M3] - item[M3] >= 0)


# fills ships on ratio
def fill_ships_with_extreme_ratio(ships, data):
    data.sort(key=itemgetter(RATIO), reverse=True) # most ratio on top
    ships[0:-1].sort(key=itemgetter(RATIO), reverse=True)
    temp = copy.deepcopy(data)
    boolian = 0
    for item in temp:
        for ship in ships:
            if fits(ship, item):
                ship[CARGO].append(item)
                data.remove(item)
                update_ship(ship)
                break
        data.sort(key=itemgetter(RATIO), reverse=(boolian%2))
        ships[0:-1].sort(key=itemgetter(RATIO), reverse=(boolian%2))
        boolian += 1


# returns average ship part that is empty as a number between 0 and 1
def cost(ships):
    kgs_taken = sum(ship[KG] for ship in ships[0:-1])
    m3s_taken = sum(ship[M3] for ship in ships[0:-1])
    percentage_kg_filled = kgs_taken / SHIPS_KG
    percentage_m3_filled = m3s_taken / SHIPS_M3
    return (percentage_kg_filled + percentage_m3_filled) / 2

# update KG and M3 change by swap
def update_swap(ships, swap, direction = 1):
    A, B, item = swap # item from ship A to B
    ships[A][KG] += direction * item[KG]
    ships[A][M3] += direction * item[M3]
    ships[B][KG] -= direction * item[KG]
    ships[B][M3] -= direction * item[M3]


# reverse swaps if rejected in annealing / hillclimber
def reverse_swaps(ships, swaps):
    for swap in swaps:
        update_swap(ships, swap, direction = -1)


# update CARGO if swap is accepted in annealing / hillclimber
def keep_swaps(ships, swaps):
    for A, B, item in swaps: # item from ship A to B
        ships[A][CARGO].remove(item)
        ships[B][CARGO].append(item)


def move_random_items(A, B, ships, swap_list):
    ships[A][CARGO].sort(key=itemgetter(RATIO), reverse=bool(random.getrandbits(1))) # most ratio on top
    for item in ships[A][CARGO]:
        if random.uniform(0,1) < 0.2:
            break
        if fits(ships[B], item):
            swap = (A, B, item)
            swap_list.append(swap)
            update_swap(ships, swap)


def random_swap(ships):
    # Keeps track of swaps/moves with update_swap() and swap_cost().
    swap_list = [] # swap elements are tuple(from ship, to ship, item)
    A, B = random.sample(range(len(ships) - 1), 2) # select 2 random ships

    # move items from ship A to cargo
    payload = 0
    ships[A][CARGO].sort(key=itemgetter(RATIO), reverse=bool(random.getrandbits(1))) # most ratio on top
    for item in ships[A][CARGO]:
        if random.uniform(0,1) < 0.1:
            continue
        if payload > 1e-2:
            break
        payload += item[KG]/SHIPS_KG + item[M3]/SHIPS_M3
        swap = (A, -1, item)
        swap_list.append(swap)
        update_swap(ships, swap)
        break
    move_random_items(B, A, ships, swap_list)
    move_random_items(-1, B, ships, swap_list)

    return swap_list


# add ship to ships
def add_ship(solution):
    global SHIPS_KG, SHIPS_M3
    weight_left = sum(item[KG] for item in solution[-1][CARGO])
    volume_left = sum(item[M3] for item in solution[-1][CARGO])
    ratio_left = weight_left / volume_left
    print(ratio_left)
    for ship in available_ships:
        if weight_left <= ship[KG] and volume_left <= ship[M3]:
            temp = copy.deepcopy(ship)
            for item in solution[-1][CARGO]:
                temp[CARGO].append(item)
            SHIPS_KG += temp[KG]
            SHIPS_M3 += temp[M3]
            update_ship(temp)
            solution.insert(0,temp)
            solution[-1][CARGO] = []
            return solution

    best, temp = 1e4, []
    for ship in available_ships:
        update_ship(ship)
        diff = abs(ship[RATIO]-ratio_left)
        if diff < best:
            best = diff
            temp = ship
    SHIPS_KG += temp[KG]
    SHIPS_M3 += temp[M3]
    solution.insert(0, copy.deepcopy(temp[0:-1]))
    return solution

# simulated annealing
def simulated_annealing(solution, runs = 1e2, addshipthreshold = 1e3):
    # add ship if first run
    while len(solution) < 3:
        add_ship(solution)

    T, T_min, alpha = 1.0, 1e-5, .9 # SA variables

    old_cost = cost(solution)
    best_cost = old_cost
    best_solution = copy.deepcopy(solution)
    counter = 0
    while solution[-1][CARGO]: # SA
        for i in range(int(runs)):
            swap_list = random_swap(solution)
            new_cost = cost(solution)
            ap = math.exp((old_cost - new_cost)/T) # acceptance probability
            if ap > round(random.uniform(0.1, 1.0), 10):
                old_cost = new_cost
                keep_swaps(solution, swap_list)
                counter = 0
            else:
                reverse_swaps(solution, swap_list)
                counter += 1
            if len(solution[-1][CARGO]) < 100:
                addshipthreshold = 1e4
            if len(solution[-1][CARGO]) < 30:
                addshipthreshold = 1e5
            if counter > addshipthreshold:
                solution = add_ship(solution)
                counter = 0
                simulated_annealing(solution)
                old_cost = cost(solution)
                break
        if T > T_min:
            T = T * alpha

        if old_cost < best_cost:  # find best solution
            best_solution = copy.deepcopy(solution)
            best_cost = old_cost

        print "ships:", len(solution)-1, "filled:","%0.2f" % ((1 - old_cost)*100), "%", "items left: ", len(solution[-1][CARGO])

    solution = best_solution
    return solution

def print_ships(ships):
    for s in ships:
        print s[NAME],"item: ", len(s[CARGO]), "\tkg: ", s[KG], "\tm3: ", s[M3]


def init_ships(ships, cargo):
    global SHIPS_KG, SHIPS_M3
    ships.append(["cargo", CARGO_KG, CARGO_M3, 0.0, [], CARGO_KG, CARGO_M3])
    ships[0][4] = cargo
    weight_left = sum(item[KG] for item in ships[-1][CARGO])
    volume_left = sum(item[M3] for item in ships[-1][CARGO])
    ratio_left = weight_left / volume_left
    ships[0][3] = ratio_left
    SHIPS_KG = sum(s[KG] for s in ships[0:-1])
    SHIPS_M3 = sum(s[M3] for s in ships[0:-1])
    if len(ships) > 1:
        for s in ships:
            update_ship(s)
    return ships

#                           _____MAIN_____
def main():
    ships, cargolist = [], []
    read_data("CargoList3.txt", cargolist)
    init_ships(ships, cargolist)
    fill_ships_with_extreme_ratio(ships, cargolist)
    simulated_annealing(ships)

    print "ships:", len(ships)-1, "filled:","%0.2f" % ((1 - cost(ships))*100), "%", "items left: ", len(ships[-1][CARGO])
    print "Runtime ", time.clock() - start_time, "seconds"
    print "solution saved as 'packinglist.txt'"
    write_packing_list(ships)


if __name__ == "__main__":
    start_time = time.clock()
    main()
