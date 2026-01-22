#Name: Ally Kimble?
#Class: 6th Hour
#Assignment: HW17

import random

#1. Create a def function that plays a single round of rock, paper, scissors where the user inputs
#1 for rock, 2 for paper, or 3 for scissors and compares it to a random number generated to serve
#as the "opponent's hand".

def play_rps():
    user_choice = int(input("Enter 1 for Rock, 2 for Paper, or 3 for Scissors:"))
    opponent_choice = random.randint(1, 3)

    choices = {1: "Rock", 2: "Paper", 3: "Scissors"}

    print("You played:" + choices[user_choice])
    print("Computer played:" + choices[opponent_choice])

    if user_choice == opponent_choice:
        print("Oh My God! It's a Tie!!!!")
    elif (user_choice == 1 and opponent_choice == 3) or (user_choice == 2 and opponent_choice == 1) or (user_choice == 3 and opponent_choice == 2):
        print("Wow! You win!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        print("You lose! HAHAHAHAHAHAHAHA!")

play_rps()
#2. Create a def function that prompts the user to input if they want to play another round, and
#repeats the RPS def function if they do or exits the code if they don't.

def play_again():
    again = input("Play again? (yes/no): ")
    if again != "yes":
        print("I'll remember that...")
    else:
        play_rps()

play_again()
