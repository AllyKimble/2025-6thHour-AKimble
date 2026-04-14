#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW_R7


#1. Create a class containing a def function that inits self and the three attributes: name, grade, color.

class Student:
    def __init__(self, name, grade, color):
        self.name = name
        self.grade = grade
        self.color = color

#2. Make a def function within the class that adds 1 to the grade attribute to any object called to it.
#If they are 12th grade, have the code change their grade to "graduated" instead.

    def addone(self):
        if self.grade == 12:
            print("They have graduated!")
        else:
            self.grade +=1

#3. Make a def function within the class that offers the user to input/change their favorite color.

    def colorchg(self):
        self.color = input("What is your favorite color?")
