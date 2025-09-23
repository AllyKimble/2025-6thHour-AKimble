#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW7

#1. Print Hello World!

print("Hello World!")

#2. Create a dictionary with 3 keys and a value for each key. One of the keys must have a value with a list containing
#three numbers inside.

SkzDict = {
    "Oldest" : "BangChan",
    "Youngest" : "I.N",
    "Songs" : [143, 4419, .0325]
}

#3. Print the keys of the dictionary from #2.

print(SkzDict.keys())

#4. Print the values of the dictionary from #2

print(SkzDict.values())

#5. Print one of the three numbers from the list by itself

print(SkzDict["Songs"][0])

#6. Using the update function, add a fourth key to the dictionary and give it a value.

SkzDict.update({"Best Song" : "Circus"})

#7. Print the entire dictionary from #2 with the updated key and value.

print(SkzDict)

#8. Make a nested dictionary with three entries containing the name of another classmate and two other pieces of information
#within each entry.

class_names = {
    "student_1" : {
        "Name" : "Ally",
        "Hair" : "Medium",
        "Height" : "Short",
    },
    "student_2" : {
        "Name" : "Aaden",
        "Hair" : "Short",
        "Height" : "Tall",
    },
    "student_3" : {
        "Name" : "Alaya",
        "Hair" : "Long",
        "Height" : "Short",
    },
}

#9. Print the names of all three classmates on the same line.

print(class_names["student_1"]["Name"], class_names["student_2"]["Name"], class_names["student_3"]["Name"])

#10. Use the pop function to remove one of the nested dictionaries inside and print the full dictionary from #8.

class_names.pop("student_2")
print(class_names)