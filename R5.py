#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW-R5
from unittest import skipIf

#1. Fix the "class" comment at the top to "6th Hour"

#I did it :)

#2. Create a list of the names of all the students in the classroom.

name_list = ["Connor","Ethan","Shane","GREG","Ally","Devon","Tristan","Alaya"]

#3. Create a for loop that prints the names of every student in the list.

for name in name_list:
    print(name)

print("~~~~~~")

#4. Using the "in" operator (hint: Google), create a for loop that only prints
#the name of a student if the letter "e" is in it.

for name in name_list:
    if "e" in name or "E" in name:
        print(name)