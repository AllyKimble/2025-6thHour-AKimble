#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW5


#1. Create a list with 9 different numbers inside.
num_list = [656, 68547, 4, 684, 872, 6, 879, 98745, 876]


#2. Sort the list from highest to lowest.
num_list.sort(reverse=True)
print(num_list)
#3. Create an empty list.
empty_list = []

print(empty_list)

#4. Remove the median number from the first list and add it to the second list.
num_list.remove(872)

empty_list.append(872)

#5. Remove the first number from the first list and add it to the second list.
num_list.remove(98745)

empty_list.append(98745)

#6. Print both lists.
print(num_list)
print(empty_list)

#7. Add the two numbers in the second list together and print the result.
print([empty_list[0] + empty_list[1]])
#8. Move the number back to the first list (like you did in #4 and #5 but reversed).
num_list.append(99617)

#9. Sort the first list from lowest to highest and print it.
num_list.sort()
print(num_list)