#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW_R8


#1. Import all of HW_R7 into this assignment using the from/import function.

from R7 import *

#2. Create an object of three students in the classroom. Ask for their name, grade, and favorite color as need be.

Greg = Student("Greg" , 12, "Purple")
Alaya = Student("Alaya", 9, "Purple")
Devon = Student("Devon", 12, "Indigo")

#3. Print the name of the first student.

print(Greg.name)

#4. Use the def function from HW_R7 to bump the grade level of the second student up by 1. Print the new grade.

Alaya.addone()
print(Alaya.grade)

#5. Use the def function from HW_R7 to ask the third student to change their favorite color to something else.
#Print the new color.

Devon.colorchg()
print(Devon.color)