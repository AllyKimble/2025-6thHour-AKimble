#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW6


#1. Import the "random" library

import random

#2. print "Hello World!"

print("Hello World!")

#3. Create three different variables that each randomly generate an integer between 1 and 10

d10_1 = random.randint(1,10)

d10_2 = random.randint(1,10)

d10_3 = random.randint(1,10)

#4. Print the three variables from #3 on the same line.

print(d10_1, d10_2, d10_3)

#5. Add 2 to the first variable in #3, Subtract 4 from the second variable in #3, and multiply by 1.5 the third variable in #3.

d10_1 += 2

d10_2 -= 4

d10_3 *= 1.5

#6. Print each result from #5 on the same line.

print(d10_1, d10_2, d10_3)

#7. Create a list containing four variables that each randomly generate an integer between 1 and 6

Random_List = [random.randint(1, 6) , random.randint(1, 6) , random.randint(1, 6) , random.randint(1, 6)]

print(Random_List)

#8. Sort the list in #7 and print it.

Random_List.sort()

print(Random_List)

#9. Add together the highest three numbers in the list from #7 and print the result.

Sum = sum(Random_List[-3:])

print(Sum)

#10. Create a list with 5 names of other students in this class and print the list.
Name_List = ["Aaden" , "Eli" , "Ally" , "Alaya" , "GREG"]

print(Name_List)

#11. Shuffle the list in #10 and print the list again.

random.shuffle(Name_List)

print(Name_List)

#12. Print a random choice from the list of names from #10.

print(random.choice(Name_List))
