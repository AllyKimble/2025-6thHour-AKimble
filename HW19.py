#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW19

import random

#1. Import the def functions created in problem 1-4 from HW16

from HW16 import hello_world, calc, animal_list, loop

#2. Call the functions here and run HW19

hello_world()
calc(a = random.randint(1, 100), b = random.randint(1, 100), c = random.randint(1, 100))
animal_list("Dog", "Turtle" , "Cat" , "Penguin" , "Panda" )
loop(67)

#3. Delete all calls for problem 5 in HW16 and run HW19 again.

#I DID THAT :)

#4. Create a try catch that tries to print variable x (which has no value), but prints "Hello World!" instead.

try:
    print(x)
except NameError:
    print("Hello World!")

#5. Create a try catch that tries to divide 100 by whatever number the user inputs, but prints an exception for Divide By Zero errors.

try:
    num = int(input("Enter a number: "))
    result = 100 / num
    print(result)
except ZeroDivisionError:
    print("Cannot divide 100 by zero >:(")

#6. Create a variable that asks the user for a number. If the user input is not an integer, prints an exception for Value errors.

try:
    user_num = int(input("Enter a number: "))
    print(f"You entered: {user_num}")
except ValueError:
    print("You did not enter a whole number :(")

#7. Create a while loop that counts down from 5 to 0, but raises an exception when it counts below zero.

cnt = 5

while True:
    if cnt < 0:
        raise Exception("You went below zero!")
    print(cnt)
    cnt -= 1