#Name: Ally Kimble
#Class: 6th Hour
#Assignment: Playground

print("Hello World")

import random


student_list = ["Aaden" , "Devon" , "Alaya" , "Ally" , "Eli" , "GREG"]


student_list.sort(reverse=True)


random.shuffle(student_list)


Random_1 = (random.choice(student_list))
student_list.remove(Random_1)
print(Random_1)
print(student_list)

Random_2 = (random.choice(student_list))
student_list.remove(Random_2)
print(Random_2)
print(student_list)

Random_3 = (random.choice(student_list))
student_list.remove(Random_3)
print(Random_3)
print(student_list)

Random_4 = (random.choice(student_list))
student_list.remove(Random_4)
print(Random_4)
print(student_list)

Random_5 = (random.choice(student_list))
student_list.remove(Random_5)
print(Random_5)
print(student_list)


print(student_list[0], "is the Winner!!!")






