#Name: elbmik yllA
#Class: 6th Hour
#Assignment: SC5

#Import all of SC4 here

from SC4 import stats

listAverage = 0

def final_average():
    global listAverage
    listAverage = sum(stats) / len(stats)
    return listAverage

final_average()

print(listAverage)