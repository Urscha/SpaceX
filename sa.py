
import math
import matplotlib
import sys
from operator import itemgetter
import random


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


def fill_cargo_random(ships, data):
    for i in data:
        s = random.randint(0,3)
        ships[s][4].append(i)
    for s in ships:
        update_ship(s)


def cost(ships):
    totalkgleft = 0
    totalm3left = 0
    for s in ships:
        s[4].sort(key=itemgetter(4), reverse=True)
        #print s[4][4]
        m3left = s[6]
        kgleft = s[5]
        for item in s[4]:
            if (m3left - item[2]) > 0 and (kgleft - item[1]) > 0:
                m3left -= item[2]
                kgleft -= item[1]
        totalkgleft += kgleft
        totalm3left += m3left
    return (totalkgleft/11895 + totalm3left/53.6)/2


def random_swap(ships):
    swapcount = random.randint(1,3)
    for i in range(swapcount):
        s1 = random.randint(0,3)
        s2 = random.randint(0,3)
        len1 = len(ships[s1][4]) - 1
        len2 = len(ships[s2][4]) - 1
        p1 = random.randint(0, len1)
        p2 = random.randint(0, len2)
        ships[s1][4][p1],ships[s2][4][p2] = ships[s2][4][p2], ships[s1][4][p1]
        update_ship(ships[s1])
        update_ship(ships[s1])
    return ships


def acceptance_probability(old_cost, new_cost, T):
    return math.exp((old_cost - new_cost)/T)#2.71828


def simulated_annealing(solution):

    old_cost = cost(solution)
    T = 1.0
    T_min = 0.00001
    alpha = 0.9
    while T > T_min:
        i = 1
        while i <= 1000:
            new_solution = random_swap(solution)
            new_cost = cost(new_solution)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > round(random.uniform(0.1, 1.0), 10):
                solution = new_solution
                old_cost = new_cost
            i += 1
        T = T * alpha
    return solution, old_cost



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



def print_cargoleft(ships, cargolist):
    item_left = len(cargolist) - sum(len(ships[i][4]) for i in range(len(ships)))
    print "Number of items left: ", item_left


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
    print_ships(ships)
    fill_cargo_random(ships, cargolist)
    ships = simulated_annealing(ships)
    #print_cargoleft(ships, cargolist)
    #update_ship(ships[0])
    print_ships(ships)
    print 1 - cost(ships)


if __name__ == "__main__":
    main()
