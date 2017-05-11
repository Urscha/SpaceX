
import math
import matplotlib
import sys
from operator import itemgetter
import random
import copy
import time

_cWEIGTH = 0 # total cargo weigth
_cVOLUME = 0 # total cargo volume
_sWEIGTH = 0 # total ships weight
_sVOLUME = 0 # total ships volume

# read data with additional values made in excell (ratio )
def read_data(input_file):
    global _cWEIGTH, _cVOLUME
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            i = line.split()
            for l in range(len(i)):
                if l%3==0:
                    t = (int(i[l]), float(i[l+1]), float(i[l+2]))
                    data.append(t)
    _cWEIGTH = sum(item[1] for item in data)
    _cVOLUME = sum(item[2] for item in data)
    return data


def kg_left(s):
    return s[5] - sum(item[1] for item in s[4])


def m3_left(s):
    return s[6] - sum(item[2] for item in s[4])


# Takes sigle ship and updates the kg's and m3's that are left
def update_ship(s):
    s[1] = kg_left(s)
    s[2] = m3_left(s)


# Takes  a ship & item as aguments. Returns True if item fits, else False
def fits(ship, item):
    return (ship[1] - item[1] >= 0 and ship[2] - item[2] >= 0)


# Fills ships with random cargo untill they are full
def fill_cargo_random(ships, data):
    random.shuffle(data)
    for i in data:
        s = random.randint(0,len(ships) - 2)
        if fits(ships[s], i):
            ships[s][4].append(i)
            update_ship(ships[s])
        else:
            ships[-1][4].append(i)


# Takes all ships and returns average percentage that is not taken
def cost(ships):
    kgs = sum(item[1] for item in ships[-1][4])
    m3s = sum(item[2] for item in ships[-1][4])
    cost = ((_cWEIGTH - kgs)/_sWEIGTH + (_cVOLUME - m3s)/_sVOLUME)/2
    return 1 - cost

def random_swap2(ships):
    s = random.randint(0,len(ships)-2)
    l = len(ships[s][4]) - 1
    weigth = 0
    while weigth < 0.02:
        item = random.randint(0,l)
        ships[-1][4].append(ships[s][4][item])
        l -= 1
        weigth += (ships[s][4][item][1]/11895 + ships[s][4][item][2]/53.6)/2
        del ships[s][4][item]

    update_ship(ships[s])
    counter = 0
    l = len(ships[-1][4]) - 1
    while counter < 5:
        item = random.randint(0,l)
        if fits(ships[s], ships[-1][4][item]):
            ships[s][4].append(ships[-1][4][item])
            del ships[-1][4][item]
            l -= 1
            update_ship(ships[s])
        else:
            counter += 1

    update_ship(ships[-1])
    return ships



# Takes all ships and randomly swaps and moves a package
def random_swap(ships):

    # Random swaps
    swapcount = random.randint(0,2)
    for i in range(swapcount):
        s1 = random.randint(0,4)
        s2 = random.randint(0,4)
        len1 = len(ships[s1][4]) - 1
        len2 = len(ships[s2][4]) - 1
        if len1 >= 0 and len2 >= 0:
            p1 = random.randint(0, len1)
            p2 = random.randint(0, len2)
            if fits(ships[s2], ships[s1][4][p1]) and fits(ships[s1], ships[s2][4][p2]):
                ships[s1][4][p1],ships[s2][4][p2] = ships[s2][4][p2], ships[s1][4][p1]
                update_ship(ships[s1])
                update_ship(ships[s2])
    # Random moves
    movecount = random.randint(0,1)
    for i in range(movecount):
        s1 = random.randint(0,4)
        s2 = random.randint(0,4)
        len1 = len(ships[s1][4]) - 1
        if len1 >= 0:
            p1 = random.randint(0, len1)
            if fits(ships[s2], ships[s1][4][p1]):
                ships[s2][4].append(ships[s1][4][p1])
                del ships[s1][4][p1]
                update_ship(ships[s1])
                update_ship(ships[s2])
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
            new_solution = random_swap2(temp)
            new_cost = cost(new_solution)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > round(random.uniform(0.1, 1.0), 10):
            #if new_cost < old_cost:
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


def print_ships(ships, score=False, cargo=False, errorcheck=False):
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


def print_cargoleft(ships, cargolist):
    item_left = len(cargolist) - sum(len(ships[i][4]) for i in range(len(ships)))
    print "Number of items left: ", item_left


def mothership():
    ships = [["Mothership", _sWEIGTH, _sVOLUME, 0.0, [], _sWEIGTH, _sVOLUME],
            ["5th ship ", 1.e5  , 1.e4, 0.0, [],   1.e5, 1.e4]]
    update_ship(ships[0])
    return ships


def init_ships():
    global _sWEIGTH, _sVOLUME
    ships = []
    Cygnus = ["Cygnus   ", 2000.0, 18.9, 0.0, [], 2000.0, 18.9]
    Verne_ATV = ["Verne_ATV", 2300.0, 13.1, 0.0, [], 2300.0, 13.1]
    Progress = ["Progress ", 2400.0,  7.6, 0.0, [], 2400.0,  7.6]
    Kounotori = ["Kounotori", 5200.0, 14.0, 0.0, [], 5200.0, 14.0]
    ThianZhou = ["ThianZhou", 6500.0, 15.0, 0.0, [], 6500.0, 15.0]
    Dragon = ["Dragon   ", 3400.0, 42.0, 0.0, [], 3400.0, 42.0]
    Cargo = ["5th_ship ", 1.e5  , 1.e4, 0.0, [],   1.e5, 1.e4]
    for i in range(11):
        ships.append(copy.deepcopy(Cygnus))
        ships.append(copy.deepcopy(Verne_ATV))
        ships.append(copy.deepcopy(Progress))
        ships.append(copy.deepcopy(Kounotori))
        ships.append(copy.deepcopy(ThianZhou))
        ships.append(copy.deepcopy(Dragon))
    ships.append(Cargo)
    for s in ships:
        update_ship(s)
    _sWEIGTH = sum(s[1] for s in ships[0:-1])
    _sVOLUME = sum(s[2] for s in ships[0:-1])
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
    print _cWEIGTH, _cVOLUME, _sWEIGTH, _sVOLUME
    print 1 - cost(ships)
    print "Runtime ", time.clock() - start_time, "seconds"

if __name__ == "__main__":
    start_time = time.clock()
    main()
