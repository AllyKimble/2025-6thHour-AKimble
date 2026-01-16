#Name:
#Class: 6th Hour
#Assignment: Semester Project 1

import random
import time

#Due to weird time travelling circumstances beyond explanation, you find yourself in 2018 or so
#working for Larian Studios. Currently, they are working on the early prototypes of the hype
#upcoming game "Baldur's Gate 3". BG3 is a game that uses the Dungeons & Dragons 5th edition rules
#as its framework for gameplay. You have been given a basic dictionary of some of the main hero
#characters and some of the enemies they may face, and are tasked with making an early prototype
#of one of the party members fighting against an enemy until one of them hits zero HP (dies).

partyDict = {
    "LaeZel" : {
        "HO" : 48,
        "Init" : 1,
        "AC" : 17,
        "AtkMod": 6,
        "Damage" : random.randint(1,6) + random.randint(1,6) + 3
    },
    "Shadowheart" : {
        "HP" : 40,
        "Init" : 1,
        "AC" : 18,
        "AtkMod": 4,
        "Damage" : random.randint(1,6) + 3,
    },
    "Gale" : {
        "HP" : 32,
        "Init" : 1,
        "AC" : 14,
        "AtkMod": 6,
        "Damage" : random.randint(1,10) + random.randint(1,10),
    },
    "Astarion" : {
        "HP" : 40,
        "Init" : 3,
        "AC" : 14,
        "AtkMod": 5,
        "Damage" : random.randint(1,8) + random.randint(1,6) + 4,
    }
}

enemyDict = {
    "Goblin" : {
        "HP" : 7,
        "Init" : 0,
        "AC" : 12,
        "AtkMod": 4,
        "Damage" : random.randint(1,6) + 2
    },
    "Orc": {
        "HP" : 15,
        "Init": 1,
        "AC" : 13,
        "AtkMod": 5,
        "Damage" : random.randint(1,12) + 3
    },
    "Troll": {
        "HP" : 84,
        "Init": 1,
        "AC" : 15,
        "AtkMod": 7,
        "Damage" : random.randint(1,6) + random.randint(1,6) + 4
    },
    "Mindflayer": {
        "HP" : 71,
        "Init": 1,
        "AC" : 15,
        "AtkMod": 7,
        "Damage" : random.randint(1,10) + random.randint(1,10) + 4
    },
    "Dragon": {
        "HP" : 127,
        "Init": 2,
        "AC" : 18,
        "AtkMod": 7,
        "Damage" : random.randint(1,10) + random.randint(1,10) + random.randint(1,8) + 4
    },
}

#Combat consists of these steps:

#1. Rolling for 'initiative' to see who goes first. This is determined by rolling a
#20-sided die (d20) and adding their initiative modifier (If the roll is the same,
#assume the hero goes first).

#2. Rolling to attack. This is determined by rolling a 20-sided die (d20) and adding their
#attack modifier. The attack hits if it matches or is higher than the target's Armor Class (AC).
#If the d20 rolled to attack is an unmodified ("natural") 20, the attack automatically hits and
#the character deals double damage. If the d20 rolled to attack is an unmodified ("natural") 1,
#the attack automatically misses

#3. If the attack hits, roll damage and subtract it from the target's hit points.

#4. The second in initiative rolls to attack (and rolls damage) afterwards.

#5. Repeat steps 2-5 until one of the characters is dead.


player = partyDict["Astarion"]
enemy = enemyDict["Mindflayer"]

#Initiative rollllllls Wheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

player_init = random.randint(1,20) + player["Init"]
enemy_init = random.randint(1,20) + enemy["Init"]

print("Astarions Initiative Roll:" , player_init)
time.sleep(1)
print("Mindflayer Initiative Roll:" , enemy_init)
time.sleep(1)

if player_init >= enemy_init:
    print("Astarion goes first!")
    attacker = player
else:
    print("Mindflayer goes first!")
    attacker = enemy

time.sleep(1)
print("--- Combat Begins ---")
time.sleep(1)

#Combat loop. Needs to keep going until one is dead.

while player["HP"] > 0 and enemy["HP"] > 0:

    if attacker == player:
        roll = random.randint(1,20)
        print("Astarion rolls:" , roll)

        if roll == 1:
            print("Nat 1! Automatic Miss!")
            attacker = enemy
        else:
            hit_value = roll + player["AtkMod"]

            if roll == 20:
                print("Nat 20! Automatic hit and double damage!")
                dmg = player["Damage"] * 2
                enemy["HP"] -= dmg
                print("Astarion deals" , dmg , "damage!")
                attacker = enemy
            elif hit_value >= enemy["AC"]:
                dmg = player["Damage"]
                enemy["HP"] -= dmg
                print("Astarion hits! They deal" , dmg , "damage!")
                attacker = enemy
            else:
                print("Astarion misses!")
                attacker = enemy

    if attacker == enemy:
        roll = random.randint(1, 20)
        print("Mindflayer rolls:", roll)

        if roll == 1:
            print("Nat 1! Automatic Miss!")
            attacker = player
        else:
            hit_value = roll + enemy["AtkMod"]

            if roll == 20:
                print("Nat 20! Automatic hit and double damage!")
                dmg = enemy["Damage"] * 2
                player["HP"] -= dmg
                print("Mindflayer deals", dmg, "damage!")
                attacker = player
            elif hit_value >= player["AC"]:
                dmg = enemy["Damage"]
                player["HP"] -= dmg
                print("Mindflayer hits! They deal", dmg, "damage!")
                attacker = player
            else:
                print("Mindflayer misses!")
                attacker = player

print("Astarion HP:" , player["HP"])
print("Mindflayer HP:" , enemy["HP"])
time.sleep(1)

print("--- Combat Over ---")
if player["HP"] < 0:
    print("Astarion has died. Mindflayer wins!")
elif enemy["HP"] < 0:
    print("Mindfllayer has been defeated! Astarion wins!")