#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW4


#1. Print Hello World!
print("Hello World")

#1. Create a list with 5 strings containing 5 different names in it.
stray_kids_list = ["Felix" , "Hyunjin" , "BangChan" , "Han" , "Seungmin"]

print(stray_kids_list)

#2. Append a new name onto the Name List.
stray_kids_list.append("Changbin")

print(stray_kids_list)

#3. Print out the 4th name on the list.
print(stray_kids_list[3])

#4. Create a list with 4 different integers in it.
num_list = [1,2,3,4]

print(num_list)

#5. Insert a new integer into the 2nd spot and print the new list.
num_list.insert(1, 0)

print(num_list)

#6. Sort the list from lowest to highest and print the sorted list.
num_list.sort()

print(num_list)

#7. Add the 1st three numbers on the sorted list together and print the sum.
print(num_list[0] + num_list[1] + num_list[2])

#8. Create a list with two strings, two variables, and too boolean values.
var1 = "Camel"
var2 = "Snail"
hermit_list = ["Grian" , "Mumbo" , True , False, var1, var2]

print(hermit_list)

#9. Create a print statement that asks the user to input their own index value for the list on #8.

print(hermit_list[int(input())])