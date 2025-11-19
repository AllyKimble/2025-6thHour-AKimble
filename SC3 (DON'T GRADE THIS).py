#Name: Ally Kimble
#Class: 6th Hour
#Assignment: SC3
from ursina.prefabs.primitives import modelname

#You have been transferred to a new team working on a mobile game that allows you to dress up a
#model and rate other models in a "Project Runway" style competition.

#They want to start prototyping the rating system and are asking you to make it.
#This prototype needs to allow the user to input the number of players, let each player rate
#a single model from 1 to 5, and then give the average score of all of the ratings.

players = int(input("How many players?:"))

if players < 3:
    print("Not enough players")
elif players == 3:
    a = int(input("Player 1, Rate This Model 1-5!:"))
    if a > 5:
        print("Too high of score, will not be added.")
    elif a < 1:
        print("Too low of score, will not be added.")
    b = int(input("Player 2, Rate This Model 1-5!:"))
    if b > 5:
        elif b < 1:(
            print("Too low of score, will not be added."))
        print("Too high of score, will not be added.")
    c = int(input("Player 3, Rate This Model 1-5!:"))
    if c > 5:
        print("Too high of score, will not be added.")
    print((a+b+c)%3)
elif players == 4:
    d = int(input("Player 1, Rate This Model 1-5!:"))
    if d > 5:
        print("Too high of score, will not be added.")
    e = int(input("Player 2, Rate This Model 1-5!:"))
    if e > 5:
        print("Too high of score, will not be added.")
    f = int(input("Player 3, Rate This Model 1-5!:"))
    if f > 5:
        print("Too high of score, will not be added.")
    g = int(input("Player 4, Rate This Model 1-5!:"))
    if g > 5:
        print("Too high of score, will not be added.")
    print((d+e+f+g)%3)
elif players == 5:
    h = int(input("Player 1, Rate This Model 1-5!:"))
    if h > 5:
        print("Too high of score, will not be added.")
    i = int(input("Player 2, Rate This Model 1-5!:"))
    if i > 5:
        print("Too high of score, will not be added.")
    j = int(input("Player 3, Rate This Model 1-5!:"))
    if j > 5:
        print("Too high of score, will not be added.")
    k = int(input("Player 4, Rate This Model 1-5!:"))
    if k > 5:
        print("Too high of score, will not be added.")
    l = int(input("Player 5, Rate This Model 1-5!:"))
    if l > 5:
        print("Too high of score, will not be added.")
    print((h+i+j+k+l)%3)
elif players > 5:
    print("Too many players5")

