#Name: Ally Kimble
#Class: 6th Hour
#Assignment: Scenario 1

#Scenario 1:
#You are a programmer for a fledgling game developer. Your team lead has asked you
#to create a nested dictionary containing five enemy creatures (and their properties)
#for combat testing. Additionally, the testers are asking for a way to input changes
#to the enemy's damage values for balancing, as well as having it print those changes
#to confirm they went through.

#It is up to you to decide what properties are important and the theme of the game.



enemies_from_book = {
    "Zarem": {
        "health": 80,
        "damage": 20,
        "speed": 25,
        "behavior": "Hostile"
    },
    "Vuahid": {
        "health": 40,
        "damage": 9,
        "speed": 15,
        "behavior": "Neutral"
    },
    "Ozk": {
        "health": 60,
        "damage": 4,
        "speed": 3,
        "behavior": "Neutral"
    },
    "Marpe": {
        "health": 20,
        "damage": 7,
        "speed": 10,
        "behavior": "Passive"
    },
    "Shiv": {
        "health": 90,
        "damage": 30,
        "speed": 30,
        "behavior": "Neutral"
    }
}

print(enemies_from_book["Zarem"])
print(enemies_from_book["Vuahid"])
print(enemies_from_book["Ozk"])
print(enemies_from_book["Marpe"])
print(enemies_from_book["Shiv"])


enemies_from_book["Zarem"]["damage"] = int(input("New Damage for Zarem:"))
print(enemies_from_book["Zarem"])

enemies_from_book["Vuahid"]["damage"] = int(input("New Damage for Vuahid:"))
print(enemies_from_book["Vuahid"])

enemies_from_book["Ozk"]["damage"] = int(input("New Damage for Ozk:"))
print(enemies_from_book["Ozk"])

enemies_from_book["Marpe"]["damage"] = int(input("New Damage for Marpe:"))
print(enemies_from_book["Marpe"])

enemies_from_book["Shiv"]["damage"] = int(input("New Damage for Shiv:"))
print(enemies_from_book["Shiv"])
