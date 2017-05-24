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


# update weight and volume left in ship
def update_ship(s):
    s[KG] = s[5] - sum(item[KG] for item in s[CARGO])
    s[M3] = s[6] - sum(item[M3] for item in s[CARGO])


# returns true if item fits in ship
def fits(ship, item):
    return (ship[KG] - item[KG] >= 0 and ship[M3] - item[M3] >= 0)


# fills ships on ratio
def fill_ships_with_extreme_ratio(ships, data):
    data.sort(key=itemgetter(3), reverse=True) # most ratio on top
    ships[0:-1].sort(key=itemgetter(3), reverse=True)
    temp = copy.deepcopy(data)
    boolian = 0
    for item in temp:
        for ship in ships:
            if fits(ship, item):
                ship[CARGO].append(item)
                data.remove(item)
                update_ship(ship)
                break
        data.sort(key=itemgetter(3), reverse=(boolian%2))
        ships[0:-1].sort(key=itemgetter(3), reverse=(boolian%2))
        boolian += 1


# Fills ships randomly
def fill_cargo_random(ships, data):
    random.shuffle(data)
    for item in data:
        random.shuffle(ships[0:-1])
        for ship in ships:
            if fits(ship, item):
                ship[CARGO].append(item)
                update_ship(ship)


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
    random.shuffle(ships[A][CARGO])
    for item in ships[A][CARGO]:
        if fits(ships[B], item):
            swap = (A, B, item)
            swap_list.append(swap)
            update_swap(ships, swap)


def random_swap(ships):
    # Keeps track of swaps/moves with update_swap() and swap_cost().
    swap_list = [] # swap elements are tuple(from ship, to ship, item)
    A, B = random.sample(range(len(ships) - 1), 2) # select 2 random ships

    # move items from ship A to cargo
    amount = 0
    random.shuffle(ships[A][CARGO])
    for item in ships[A][CARGO]:
        if amount > 2e-2:
            break
        amount += item[KG]/SHIPS_KG + item[M3]/SHIPS_M3
        swap = (A, -1, item)
        swap_list.append(swap)
        update_swap(ships, swap)

    move_random_items(B, A, ships, swap_list)
    move_random_items(-1, B, ships, swap_list)

    return swap_list

# simulated annealing
def simulated_annealing(solution, runs = 1e2):
    T, T_min, alpha = 1.0, 1e-4, .9 # SA variables

    old_cost = cost(solution)
    best_cost = old_cost
    best_solution = copy.deepcopy(solution)

    while T > T_min: # SA
        for i in range(int(runs)):
            swap_list = random_swap(solution)
            new_cost = cost(solution)
            ap = math.exp((old_cost - new_cost)/T) # acceptance probability
            if ap > round(random.uniform(0.1, 1.0), 10):
                old_cost = new_cost
                keep_swaps(solution, swap_list)
            else:
                reverse_swaps(solution, swap_list)
        T = T * alpha

        if old_cost < best_cost:  # find best solution
            best_solution = copy.deepcopy(solution)
            best_cost = old_cost

        print "Best cost:", best_cost, "\nCurrent cost:", old_cost

    solution = best_solution
    return solution

# hillclimber
def hillclimber(solution, runs = 1e4):
    old_cost = cost(solution) # current cost
    for i in range(int(runs)):
            swap_list = random_swap(solution)
            new_cost = cost(solution)
            if new_cost < old_cost:
                old_cost = new_cost
                keep_swaps(solution, swap_list)
            else:
                reverse_swaps(solution, swap_list)
            print "Cost:", old_cost
    return solution

def print_ships(ships):
    for s in ships:
        print s[NAME],"item: ", len(s[CARGO]), "\tkg: ", s[KG], "\tm3: ", s[M3]


def print_cargoleft(ships, cargolist):
    item_left = len(cargolist) - sum(len(ships[i][CARGO]) for i in range(len(ships)))
    print "Number of items left: ", item_left


# make of initialized ships one big ship
def mothership(ships):
    ships = [["Mothership", SHIPS_KG, SHIPS_M3, 0.0, [], SHIPS_KG, SHIPS_M3],
             ["cargo     ", CARGO_KG, CARGO_M3, 0.0, [], CARGO_KG, CARGO_M3]]
    for ship in ships:
        update_ship(ship)
    return ships


def init_ships(ships):
    global SHIPS_KG, SHIPS_M3

    for i in range(10):
        ships.append(copy.deepcopy(Cygnus))
        ships.append(copy.deepcopy(Verne_ATV))
        ships.append(copy.deepcopy(Progress))
        ships.append(copy.deepcopy(Kounotori))
        ships.append(copy.deepcopy(ThianZhou))
        ships.append(copy.deepcopy(Dragon))
    ships.append(["cargo", CARGO_KG, CARGO_M3, 0.0, [], CARGO_KG, CARGO_M3])

    SHIPS_KG = sum(s[KG] for s in ships[0:-1])
    SHIPS_M3 = sum(s[M3] for s in ships[0:-1])
    for s in ships:
        update_ship(s)
    return ships



def fill_again(ships):
    cargo = copy.deepcopy(ships[-1][CARGO])
    for item in cargo:
        for ship in ships[0:-1]:
            if fits(ship, item):
                ship[CARGO].append(item)
                update_ship(ship)
                ships[-1][CARGO].remove(item)
                break
    return ships


#                           _____MAIN_____
def main():
    ships, cargolist = [], []
    read_data("CargoList3.txt", cargolist)
    init_ships(ships)

    fill_ships_with_extreme_ratio(ships, cargolist)
    fill_cargo_random(ships, cargolist)
    simulated_annealing(ships)

    for i in range(3):
        hillclimber(ships)
        fill_again(ships)


    print_ships(ships)
    print sum(len(ship[CARGO]) for ship in ships )
    print "cargo in 5th ship: weight =", sum(item[KG] for item in ships[-1][CARGO]), ",\tvolume = ",sum(item[M3] for item in ships[-1][CARGO])
    print CARGO_KG, CARGO_M3, SHIPS_KG, SHIPS_M3
    print 1 - cost(ships)
    print "Runtime ", time.clock() - start_time, "seconds"

if __name__ == "__main__":
    start_time = time.clock()
    main()
