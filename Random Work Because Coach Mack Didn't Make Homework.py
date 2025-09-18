#Name: Ally Kimble
#Class: 6th Hour
#Assignment: Playground

print("Hello World")

import random


student_list = ["Aaden" , "Devon" , "Alaya" , "Ally" , "Eli" , "GREG", "Coach Mack", "Carlos"]


random.shuffle(student_list)

student_length = len(student_list) -1
for student in range(student_length):

    Random_1 = (random.choice(student_list))
    student_list.remove(Random_1)
    print(Random_1)
    print(student_list)




print(student_list[0], "is the Winner!!!")






