#Name: Ally Kimble
#Class: 6th Hour
#Assignment: SC3

#You have been transferred to a new team working on a mobile game that allows you to dress up a
#model and rate other models in a "Project Runway" style competition.

#They want to start prototyping the rating system and are asking you to make it.
#This prototype needs to allow the user to input the number of players, let each player rate
#a single model from 1 to 5, and then give the average score of all of the ratings.

total = 0

players = int(input("Enter Number of Players:"))


for i in range(1, players+1):
    rate = int(input("Rate this model! {i} (1-5)"))

    while rate < 0 or rate > 5:
        print("Rating is invalid, please enter a number between 1 and 5")
        rate = int(input("Rate this model! {i} (1-5)"))
    else:
        total += rate

average = total / players

print("The average score is:", average)