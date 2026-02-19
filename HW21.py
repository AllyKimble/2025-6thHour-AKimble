#Name: ALLY KIMBLE
#Class: 6th Hour
#Assignment: HW21

#1. Import the random and time libraries

import random
import time

#2. Create a class containing a def function that inits self and the 3 attributes health, damage, and speed.

class Character:
    def __init__(self, health, damage, speed):
        self.health = health
        self.damage = damage
        self.speed = speed

    def take_damage_loop(self):
        for i in range(10):
            damage_taken = random.randint(1,6)
            self.health -= damage_taken
            print("TacoMan eats" , damage_taken , "tacos. Health is now:", self.health)
            time.sleep(1)

    def heal_tacoman(self, tacoman):
        tacoman.health += 30
        if tacoman.health >= 100:
            tacoman.health = 100
        print("TacoMan is healed by the life-giving Salsa!!!!!! Health is now:", tacoman.health)


#3. Make a "warrior" character object with 100 health, 20 damage, and 30 speed. Print the character's initial health below.

tacoman = Character(100, 20, 30)
print("TacoMan health:", tacoman.health)


tacoman.take_damage_loop()

#4. Make a def function within the class that loops 10 times. Within this function,
#make the following loop 10 times: the character takes a random amount of damage from 1 to 6,
#the new health is printed, a time.sleep delay of one second is done. Call the function to the warrior.

#5. Make a "healer" character object with 60 health, 10 damage, and 30 speed.

healer = Character(60, 10, 30)

#6. Make a def function within the class that heals the warrior for 30 health. Create an if statement
#that sets the warrior's health to its max (100) if the healing would bring the warrior's health above that.
#Call the function to the healer.

healer.heal_tacoman(tacoman)

#7. Print the warrior's final health at the very bottom.

print("TacoMan's final health is:", tacoman.health)