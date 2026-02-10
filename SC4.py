#Name: Ally Kimble
#Class: 6th Hour
#Assigment: SC4

import random

#After an extended leave, the team lead for the RPG developer is back, and he wants to continue the project.
#He wants to prototype the character creation model but first needs something that rolls stats for the characters.
#He wants you to make a function that rolls 4 six-sided dice (d6), sorts them from highest to lowest, and then adds the
#highest 3 together. He then wants you to add that result to a list outside the function. He wants you to run that function
#5 more times (six times total) and print all six stats.
stats = []

def roll_stat():
    rolls = []

    for i in range(4):
        rolls.append(random.randint(1, 6))

    rolls.sort(reverse=True)
    stat_total = rolls[0] + rolls[1] + rolls[2]

    stats.append(stat_total)

for i in range(6):
    roll_stat()

print("Character Stats:")
print(stats)

#Once that is done, to ensure that the average of the statblock is fair (somewhere roughly between 12-13), he wants you
#to plug it into a calculator (SC5) and print the average.

average = sum(stats) / 6
print("Average Stat:", average)