
import math
import matplotlib
import sys
from operator import itemgetter
import random
import copy
import time

TOTAL_CARGO_WEIGTH = 0 # total cargo weight
TOTAL_CARGO_VOLUME = 0 # total cargo volume
TOTAL_SHIPS_WEIGTH = 0 # total ships weight
TOTAL_SHIPS_VOLUME = 0 # total ships volume

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
                    index = int(i[l])
                    kg = float(i[l+1])
                    m3 = float(i[l+2])
                    ratio = kg/m3
                    data.append((index, kg, m3, ratio))
    TOTAL_CARGO_WEIGTH = sum(item[KG] for item in data)
    TOTAL_CARGO_VOLUME = sum(item[M3] for item in data)
    return data


def kg_left(s):
    return s[5] - sum(item[KG] for item in s[CARGO])


def m3_left(s):
    return s[6] - sum(item[M3] for item in s[CARGO])


# Takes sigle ship and updates the kg's and m3's that are left
def update_ship(s):
    s[KG] = kg_left(s)
    s[M3] = m3_left(s)


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


# returns average ship part that is empty as a number between 0 and 1
def cost(ships):
    kgs_taken = sum(ship[KG] for ship in ships[0:-1])
    m3s_taken = sum(ship[M3] for ship in ships[0:-1])
    percentage_kg_filled = kgs_taken / TOTAL_SHIPS_WEIGTH
    percentage_m3_filled = m3s_taken / TOTAL_SHIPS_VOLUME
    profit = (percentage_kg_filled + percentage_m3_filled) / 2
    cost = 1 - profit
    return cost

# update weight and volume taken by ships that are listed in swaps
# IMPORTANT: if swap is rejected, reverse with "direction = -1"
def update_swap(ships, swap, direction = 1):
    A, B, item = swap# item from ship A to B
    print A, B, item
    ships[A][KG] -= direction * item[KG]
    ships[A][M3] -= direction * item[M3]
    ships[B][KG] += direction * item[KG]
    ships[B][M3] += direction * item[M3]

def reverse_swaps(ships, swaps):
    for swap in swaps:
        update_swap(ships, swap, direction = -1)


# update cargolists if swap is accepted
def keep_swaps(ships, swaps):
    for A, B, (item) in swaps: # item from ship A to B
        ships[A][CARGO].remove(item)
        ships[B][CARGO].append(item)

def random_swap(ships):

    # keeps track of swaps for efficiency (preventing any deepcopy)
    # this function will make things look more messy and errorprone, but will
    # boost the efficiency from O(..) to O(..). This efficiency implementation
    # comes together with update_swap() and swap_cost().
    swap = () # (from ship A, to ship B, item)
    swap_list = [] # list of swaps

    # move items from ship A to cargo
    s1 = random.randint(0,len(ships)-2)
    l = len(ships[s1][CARGO]) - 1
    weight = 0 #
    used_items = []
    while weight < .02 and l - len(used_items) > 1:
        # find item that's not swapped
        item = random.randint(0,l)
        while item in used_items:
            item = random.randint(0,l)
        used_items.append(item)
        # update weight
        kg_weight = ships[s1][CARGO][item][KG] / TOTAL_SHIPS_WEIGTH
        m3_weight = ships[s1][CARGO][item][M3] / TOTAL_SHIPS_VOLUME
        weight += (kg_weight + m3_weight) / 2
        # swap
        swap = (s1, -1, ships[s1][CARGO][item])
        swap_list.append(swap)
        update_swap(ships, swap)


    # move items from ship B to ship A
    s2 = random.randint(0,len(ships)-2)
    used_items = []
    while s2 == s1:
        s2 = random.randint(0,len(ships)-2)
    counter = 0
    l = len(ships[s2][CARGO]) - 1
    while counter < 5 and l - len(used_items) > 1:
        # find item that's not swapped
        item = random.randint(0,l)
        while item in used_items:
            item = random.randint(0,l)
        used_items.append(item)
        # move if possible
        if fits(ships[s1], ships[s2][CARGO][item]):
            swap = (s2, s1, ships[s2][CARGO][item])
            swap_list.append(swap)
            update_swap(ships, swap)
        else:
            counter += 1

    # move items from cargo to ship B
    counter = 0
    l = len(ships[-1][CARGO]) - 1
    used_items = []
    while counter < 5 and l -len(used_items) > 1:
        # find item that's not swapped
        item = random.randint(0,l)
        while item in used_items:
            item = random.randint(0,l)
        used_items.append(item)
        # move if possible
        if fits(ships[s2], ships[-1][CARGO][item]):
            swap = (-1, s2, ships[-1][CARGO][item])
            swap_list.append(swap)
            update_swap(ships, swap)
        else:
            counter += 1

    return swap_list


# acceptance probability
def acceptance_probability(old_cost, new_cost, T):
    return math.exp((old_cost - new_cost)/T)

# simulated annealing
def simulated_annealing(solution):
    # initialize variables for annealing
    T = 1.0
    T_min = 0.00001
    alpha = 0.9
    old_cost = cost(solution) # init old_cost
    best_solution = copy.deepcopy(solution) # keep track of best solution

    while T > T_min:
        i = 1
        while i <= 1000:
            print "1",cost(solution), old_cost
            swap_list = random_swap(solution)
            new_cost = cost(solution)
            print "2",new_cost, old_cost
            # ap = acceptance_probability(old_cost, new_cost, T)
            # if ap > round(random.uniform(0.1, 1.0), 10):
            if new_cost < old_cost:
                old_cost = new_cost
                keep_swaps(solution, swap_list)
            else:
                reverse_swaps(solution, swap_list)
            i += 1
        T = T * alpha

        print ("Temperature: %.5f" % T)
        print "Overall lowest cost: ", cost(best_solution)
        print "Current cost: ", old_cost ,"\n"
        # check if this solution should be saved as the overall best solution
        if old_cost < cost(best_solution):
            print("Updated best solution \n")
            best_solution = copy.deepcopy(solution)
            keep_swaps(best_solution, swap_list)

    solution = best_solution
    return solution


def print_ships(ships):
    svalue = 0
    for s in ships:
        print s[NAME],"item: ", len(s[CARGO]), "\t kg: ", kg_left(s), "\t m3: ", m3_left(s)



def print_cargoleft(ships, cargolist):
    item_left = len(cargolist) - sum(len(ships[i][CARGO]) for i in range(len(ships)))
    print "Number of items left: ", item_left


def mothership():
    ships = [["Mothership", TOTAL_SHIPS_WEIGTH, TOTAL_SHIPS_VOLUME, 0.0, [], TOTAL_SHIPS_WEIGTH, TOTAL_SHIPS_VOLUME],
            ["5th ship ", 1.e5  , 1.e4, 0.0, [],   1.e5, 1.e4]]
    update_ship(ships[0])
    return ships


def init_ships():
    global TOTAL_SHIPS_WEIGTH, TOTAL_SHIPS_VOLUME
    ships = []
    Cygnus = ["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9]
    Verne_ATV = ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1]
    Progress = ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6]
    Kounotori = ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]
    ThianZhou = ["ThianZhou", 6500.0, 15.0, 0.0, [], 6500.0, 15.0]
    Dragon = ["Dragon   ", 3400.0, 42.0, 0.0, [], 3400.0, 42.0]
    Cargo = ["5th_ship ", 1.e5  , 1.e4, 0.0, [],   1.e5, 1.e4]
    for i in range(10):
        ships.append(copy.deepcopy(Cygnus))
        ships.append(copy.deepcopy(Verne_ATV))
        ships.append(copy.deepcopy(Progress))
        ships.append(copy.deepcopy(Kounotori))
        ships.append(copy.deepcopy(ThianZhou))
        ships.append(copy.deepcopy(Dragon))
    ships.append(Cargo)
    for s in ships:
        update_ship(s)
    TOTAL_SHIPS_WEIGTH = sum(s[KG] for s in ships[0:-1])
    TOTAL_SHIPS_VOLUME = sum(s[M3] for s in ships[0:-1])
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
    simulated_annealing(ships)
    #print_cargoleft(ships, cargolist)
    #update_ship(ships[0])
    print_ships(ships)
    print "cargo in 5th ship: weight =", sum(s[1] for s in ships[-1][4]), ",\tvolume = ",sum(s[2] for s in ships[-1][4])
    print TOTAL_CARGO_WEIGTH, TOTAL_CARGO_VOLUME, TOTAL_SHIPS_WEIGTH, TOTAL_SHIPS_VOLUME
    print 1 - cost(ships)
    print "Runtime ", time.clock() - start_time, "seconds"

if __name__ == "__main__":
    start_time = time.clock()
    main()
