#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW-R3


#1. import random and print "Hello World!"

import random

print("Hello World!")

#2. Create three variables that each randomly generate an integer between 1 and 10, print each number on the same line.

a = random.randint(1, 10)
b = random.randint(1, 10)
c = random.randint(1, 10)

print(a, b, c)

#3. Create a list containing 5 strings listing 5 colors.

color_list = ["red", "blue", "green", "yellow", "pink"]

#4. Use a function to randomly choose one of the 5 colors from the list and print the result.

print(random.choice(color_list))

#5. Create an if statement that determines which of the three variables from #2 is the lowest.

if a <= b and a <= c:
    print(a, "is the smallest.")
elif b <= a and b <= c:
    print(b, "is the smallest.")
elif c <= a and c <= b:
    print(c, "is the smallest.")
elif a == b == c:
    print("They are all the same number stupid :P")