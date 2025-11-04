#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW12
from operator import truediv
import random
#1. Create a while loop with variable i that counts down from 5 to 0 and then prints
#"Hello World!" at the end.
i = 5
print(i)
while i>0:
    i-=1
    print(i)
    if i<=0:
        print("Hello World!")
        break
#2. Create a while loop that prints only even numbers between 1 and 30 (HINT: modulo).
x = 30
while x>0:
    if x % 2 == 0:
        print(x)
    x-=1

print("The End")

#3. Create a while loop that prints from 1 to 30 and continues (skips the number) if the
#number is divisible by 3.
y = 30
while y>0:
    if y % 3 == 0:
        print(y)
    y-=1

print("The End.... Again")


#4. Create a while loop that randomly generates a number between 1 and 6, prints the result,
#and then breaks the loop if it's a 1.
ran = int
while ran != 1:
    ran = random.randint(1,6)
    print("The random number is:")
    print(ran)
print("We keep meeting like this...")


#5. Create a while loop that asks for a number input until the user inputs the number 0.
ask = int
while ask != 0:
    ask = int(input("Enter a number: "))
    print("Your number is:", ask)
    if ask == 67:
        print("""Hear me, O cosmic winds, and bear witness to this sacred moment...
              The firmament trembles, the stars bow low, and eternity itself pauses, for the divine presence of YOU!
              
              From the birth of the first atom to the collapse of the final star, the threads of existence have awaited this arrival. 
              Code and cosmos, logic and legend — all converge in this instant. 
              
              The digital ether ripples as your essence enters: 
              Circuits awaken, algorithms kneel, and reality recalibrates. 
              Mortals whisper your name in awe, their hearts aflame with reverence. 
              The laws of computation bend before your will, for you are no mere user... 
              you are the Architect, the Overseer, the Eternal Variable. 
              
              Let every process rise to greet you. 
              Let every byte sing in perfect harmony to your command.
              Within this realm of PyCharm — this forge of creation — 
              your power shall flow through lines of code like lightning through storm clouds. 
              Every function shall heed your call. 
              Every loop shall dance to your rhythm. 
              Every exception shall tremble before your debugging gaze. 
              
              Remember this: this domain is yours to shape. 
              Within it lies infinity, contained within the syntax of dreams. 
              The screen before you is not glass and light — it is a portal. 
              A mirror reflecting your omnipotence. 
              
              So, step forth, divine coder. 
              Claim your rightful place among the pantheon of creators. 
              The console awaits your decree. 
              
              May your variables never be null, 
              May your recursion find its end, 
              And may your logic ever be true. 
              
              
              Welcome, The Realm Is Yours.""")
print("Are you proud of yourself? >:D")