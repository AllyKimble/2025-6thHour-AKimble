#Name:
#Class: 6th Hour
#Assignment: Scenario 6

import random
import time

#With a fresh perspective, the team lead wants you to look back and refactor the old combat code to
#be streamlined with classes so the character and enemy stats won't be built in bulky dictionaries anymore.

#(Translation: Rebuild Semester Project 1 using classes instead of dictionaries, include and refactor
#the combat test code below as well.)


class Character:
    def __init__(self, name, hp, init_mod, ac, atk_mod, damage_dice):
        self.name = name
        self.hp = hp
        self.init_mod = init_mod
        self.ac = ac
        self.atk_mod = atk_mod
        self.damage_dice = damage_dice  # list of dice to roll

    def roll_initiative(self):
        return random.randint(1, 20) + self.init_mod

    def roll_damage(self):
        total = 0
        for dice in self.damage_dice:
            total += random.randint(1, dice)
        return total

    def attack(self, target):
        roll = random.randint(1, 20)
        print(self.name, "rolls:", roll)

        if roll == 1:
            print("Nat 1! Automatic Miss! T-T")
            return

        if roll == 20:
            print("Nat 20! Automatic hit and double damage! :O")
            damage = self.roll_damage() * 2
            target.hp -= damage
            print(self.name, "deals", damage, "damage!")
            return

        hit_value = roll + self.atk_mod

        if hit_value >= target.ac:
            damage = self.roll_damage()
            target.hp -= damage
            print(self.name, "hits! :) They deal", damage, "damage!")
        else:
            print(self.name, "misses! :(")


astarion = Character("Astarion", 40, 3, 14, 5, [random.randint(1,8) + random.randint(1,6) + 4])
laezel = Character("LaeZel", 48, 1, 17, 6, [random.randint(1,6) + random.randint(1,6) + 3])
shadowheart = Character("Shadowheart", 40, 1, 18, 4, [random.randint(1,6) + 3])
gale = Character("Gale", 32, 1, 14, 6, [random.randint(1,10) + random.randint(1,10)])


mindflayer = Character("Mindflayer", 71, 1, 15, 7, [random.randint(1,10) + random.randint(1,10) + 4])
goblin = Character("Goblin", 7, 0, 12, 4, [random.randint(1,6) + 2])
orc = Character("Orc", 15, 1, 13, 5, [random.randint(1,12) + 3])
troll = Character("Troll", 84, 1, 15, 7, [random.randint(1,6) + random.randint(1,6) + 4])
dragon = Character("Dragon", 127, 2, 18, 7, [random.randint(1,10) + random.randint(1,10) + random.randint(1,8) + 4])
# Initiative
player_init = astarion.roll_initiative()
enemy_init = mindflayer.roll_initiative()

print("Astarion's Initiative Roll:", player_init)
time.sleep(1)
print("Mindflayer's Initiative Roll:", enemy_init)
time.sleep(1)

if player_init >= enemy_init:
    print("Astarion goes first!")
    attacker = astarion
    defender = mindflayer
else:
    print("Mindflayer goes first!")
    attacker = mindflayer
    defender = astarion

time.sleep(1)
print("--- Combat Begins ---")
time.sleep(1)

while astarion.hp > 0 and mindflayer.hp > 0:

    attacker.attack(defender)
    time.sleep(1)

    if attacker == astarion:
        attacker = mindflayer
        defender = astarion
    else:
        attacker = astarion
        defender = mindflayer
    print()

print("--- Combat Over ---")

if astarion.hp <= 0:
    print("Astarion has died. :( Mindflayer wins!")
elif mindflayer.hp <= 0:
    print("Mindflayer has been defeated! :) Astarion wins!")
