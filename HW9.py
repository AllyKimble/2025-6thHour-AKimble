#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW9

import random

#1. Print "Hello World!"

print("Hello World!")


#2. Create a list with three variables that each randomly generate a number between 1 and 100
Random_List = [random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)]


#3. Print the list.

print(Random_List)

#4. Create an if statement that determines which of the three numbers is the highest and prints the result.

if Random_List[0] > Random_List[1] and Random_List[0] > Random_List[2]:
    print(f"{Random_List[0]} is the biggest number")
elif Random_List[1] > Random_List[0] and Random_List[1] > Random_List[2]:
    print(f"{Random_List[1]} is the biggest number")
elif Random_List[2] > Random_List[0] and Random_List[2] > Random_List[1]:
    print(f"{Random_List[2]} is the biggest number")

#5. Tie the result (the largest number) from #4 to a variable called "num".

num = max(Random_List)

#6. Create a nested if statement that prints if num is divisible by 2, divisible by 3, both, or neither.

if num % 2 == 0:
    print(f"{num} is divisible by 2")
elif num % 3 == 0:
    print(f"{num} is divisible by 3")
elif num % 2 == 0 and num % 3 == 0:
    print(f"{num} is divisible by 2 AND 3")
else:
    print(f"{num} is not divisible by 2 or 3")
