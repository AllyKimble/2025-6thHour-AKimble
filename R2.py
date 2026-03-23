#Name: Ally Kimble
#Class: 5th Hour
#Assignment: HW-R2 ((R2-D2))


#1. Print "Hello World!"

print("Hello World!")

#2. Create an empty list.

empty_list = []

#3. Create a list that contains the names of everyone in the classroom.

class_list = ["Ally", "GREG", "Shane", "Devon", "Tristan", "Ethan", "Conner", "Alaya"]

#4. Print the list from #3, sort the list, then print the list again.

print(class_list)
class_list.sort()
print(class_list)

#5. Append 5 different integers into the empty list from #2 and print the list.

empty_list.append(67)
empty_list.append(6)
empty_list.append(7)
empty_list.append(21)
empty_list.append(13)
print(empty_list)

#6. Add together the middle three numbers in the list from #2 and print the result.

add_list = empty_list[1] + empty_list[2] + empty_list[3]
print(add_list)

#7. Remove the very first number in the list from #2. Print the new first number.

empty_list.remove(empty_list[0])
print(empty_list[0])

#8. Create a dictionary with three keys with respective values: your name, your grade, and your favorite color.

medict = {
    "Name" : "Ally",
    "Grade" : "Senior",
    "Favorite Color" : 'Purple'}

#9. Using the update function, add a fourth key and value determining your favorite candy.

medict.update({"Favorite Candy" : "Gay Bacon"})

#10. Print ONLY the values of the dictionary from #8.

print(medict.values())