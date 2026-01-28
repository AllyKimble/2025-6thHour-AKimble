#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW18

import random

#1. Import the "random" library and create a def function that prints "Hello World!"

def hello():
    print("Hello World")

#2. Create two empty integer variables named "heads" and "tails"

heads = 0
tails = 0

#3. Create a def function that flips a coin one hundred times and increments the result in the above variables.

def flip():
    global heads, tails
    count = 0
    while count != 100:
        flip = random.randint(1, 2)
        if flip == 1:
            heads += 1
        else:
            tails += 1
        count = count + 1
#4. Call the "Hello world" and "Coin Flip" functions here

hello()
flip()
print("The amount of heads is:", heads)
print("The amount of tails is:", tails)

#5. Print the final result of heads and tails here

#6. Create a list called beanBag and add at least 5 different colored beans to the list as strings.

Beanbag = ["Red" , "Blue" , "Yellow" , "Pink", "White"]

#7. Create a def function that pulls a random bean out of the beanBag list, prints which bean you pulled, and then removes it from the list.

def beans():
    rand_bean = random.choice(Beanbag)
    print(rand_bean)
    Beanbag.remove(rand_bean)
    print(Beanbag)
    recall()
#8. Create a def function that asks if you want to pull another bean out of the bag and, if yes, repeats the #3 def function

def recall():
    choice = (input("Want another bean?????? (y/n):"))
    print(choice)
    if choice == "y":
        beans()
    elif choice == "n":
        print("Fine. Goodbye")
        exit()
    else:
        print("Please try again.")
        recall()

#9. Call the "Bean Pull" function here

beans()