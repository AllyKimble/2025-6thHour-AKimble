#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW14
from unittest import skipIf, SkipTest

#1. Create a for loop with variable i that counts down from 5 to 1 and then prints "Hello World!"
#at the end.
x = 5

for i in range(1, 6):
    print(x)
    x -=1
print("Hello World!")


#2. Create a for loop that counts up and prints only even numbers between 1 and 30.
for i in range(1, 31):
    if i % 2 == 0:
        print(i)
        i +=1

#3. Create a for loop that prints from 1 to 30 and continues (skips the number) if the number is
#divisible by 3.
for i in range(1, 31):
    if i % 3 != 0:
        print(i)


#4. Create a for loop that prints 5 different animals from a list.
AnimalList = ["Raphael", "Michelangelo", "Turtle", "Donatello", "Leonardo"]
for animal in AnimalList:
    print(animal)


#5. Create a for loop that spells out a word you input backwards.
#(HINT: Google "How to reverse a string in Python")
for d in input("Give me a word: ")[::-1]:
    print(d)

#6. Create a list containing 10 integers of your choice and print the list.
NumList = [564, 4351, 45, 5, 786, 5247, 4, 86, 7, 67]
print(NumList)

#7. Create two empty variables named evenNumbers and oddNumbers.
evenNumbers = 0

oddNumbers = 0

#8. Make a loop that counts the number of even and odd numbers in the list, and prints the
#result after the loop.
for item in NumList:
    if item % 2 == 0:
        evenNumbers += 1
    else:
        oddNumbers += 1

print(evenNumbers)
print(oddNumbers)


#9. Create a variable that asks the user for an integer and an empty integer variable.
num = 1
x = int(input("Enter Number Here:"))

#10. Create a loop with a range from 1 to the number the user input. Use the loop to find the
#factorial of that number and print the result. A factorial of a number is that number multiplied
#by every number before it until you reach 1. (For example: 5! is 5 x 4 x 3 x 2 x 1 = 120)
for i in range(1, x+1):
    num *= i

print(num)