import math
import matplotlib
import sys
from operator import itemgetter

data = []

with open("CargoList1.txt", 'r') as f:
    for line in f:
        elements = line.split()
        for l in range(len(elements)):
            if l%3==0:
                t = (int(elements[l]),int(elements[l+1]),float(elements[l+2]))
                data.append(t)

# initiale ships
ships = [["Cygnus   ", 2000, 18.9,[]], ["Verne_ATV", 2300, 13.1,[]], ["Progress ", 2400, 7.6,[]], ["Kounotori",5200,14,[]]]

# sort packages: most kg on top
data.sort(key=itemgetter(1), reverse=True)

# sort ships: most left kgs on top
ships.sort(key=itemgetter(1), reverse=True)

# Put package with most kg in ship with most kgs left
for i in data:
    ships[0][1] -= i[1]
    ships[0][2] -= i[2]
    print "packing " , i[1] , " in ship " ,  ships[0][0]
    ships[0][3].append(i)
    ships.sort(key=itemgetter(1), reverse=True)


# Print
for i in ships:
    print i[0], "\t kg: ", i[1], "\t m3: ", i[2] , "\n" , i[3], "\n"
