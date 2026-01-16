#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW16
import random


#1. Create a def function that prints out "Hello World!"

def hello_world():
    print("Hello World!")

#2. Create a def function that calculates the average of three numbers (set the 3 numbers as your arguments).

def calc(a, b, c):
    average = (a+b+c) / 3
    print("The average is: ", average)

#3. Create a def function with the names of 5 animals as arguments, treats it like a list, and
#prints the name of the third animal.

def animal_list(*animal):
    print("The 3rd animal is:", animal[2])



#4. Create a def function that loops from 1 to the number put in the argument.

def loop(number):
    for i in range(1, number+1):
        print(i)

#5. Call all of the functions created in 1 - 4 with relevant arguments.

hello_world()
calc(a = random.randint(1, 100), b = random.randint(1, 100), c = random.randint(1, 100))
animal_list("Dog", "Turtle" , "Cat" , "Penguin" , "Panda" )
loop(67)

#6. Create a variable x that has the value of 2. Print x

x = 2
print(x)

#7. Create a def function that multiplies the value of 2 by a random number between 1 and 5.

def random_x():
    global x
    x = x*(random.randint(1, 5))

#8. Print the new value of x.

random_x()

print(x)