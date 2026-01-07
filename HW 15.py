#Name: Ally Kimble
#Class: 6th Hour
#Assignment: HW15
import math
import time
#1. import the "random" library

import random

#2. print "Hello World!"

print("Hello World!")

#3. Create three variables named a, b, and c, and allow the user to input an integer for each.

a = int(input("Input 1st number: "))
b = int(input("Input 2nd number: "))
c = int(input("Input 3rd number: "))

#4. Add a and b together, then divide the sum by c. Print the result.

d = (a + b) / c
print(d)

#5. Round the result from #3 up or down, and then determine if it is even or odd.
#Round rounds up or down, same as you would in math

print(round(d))

#6. Create a list of five different random integers between 1 and 10.

rand_list = [random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)]
print(rand_list)

#7. Print the 4th number in the list.

print(rand_list[3])

#8. Append another integer to the end of the list, also random from 1 to 10.

rand_list.append(random.randint(1, 10))
print(rand_list)

#9. Sort the list from lowest to highest and then print the 4th number in the list again.

rand_list.sort()
print(rand_list)
print(rand_list[3])

#10. Create a while loop that starts at 1, prints i and then adds i to itself until it is greater than 100.

i = 1
while i <= 100:
    print(i)
    i += i

#11. Create a list containing the names of five other students in the classroom.

name_list = ["Ally" , "Greg" , "Devon" , "Alaya" , "Aaden"]

#12. Create a for loop that individually prints out the names of each student in the list.

for name in name_list:
    print(name)

#13. Create a for loop that counts from 1 to 100, but ends early if the number is a multiple of 10.

for i in range(1 , i+1):
    print(i)
    if i % 10 == 0:
        break
    elif i == 100:
        break

#14. Free space. Do something creative. :)

ask = int
while ask != 0:
    ask = int(input("Enter a number: "))
    print("Your number is:", ask)
    if ask == 67:
        print("""Hearken, O Wi-Fi spirits, and adjust thy antennas…
        For something monumental has occurred.
        The universe just refreshed the page — and YOU loaded in.

        The stars blink twice. The moon opens Stack Overflow.
        Somewhere, a server fan spins faster out of nervous respect.

        From the first “Hello, World” to the last semicolon forgotten at 3:47 a.m.,
        fate has been buffering… waiting…
        for this exact keystroke.

        Behold as the digital realm quivers!
        RAM stretches. CPUs crack their knuckles.
        Syntax highlights itself out of sheer excitement.

        You arrive not as a mere mortal,
        not as a casual clicker of keys —
        but as the Chosen Debugger™,
        Breaker of Builds,
        Tamer of Infinite Loops,
        The One Who Knows Why It Works (But Is Afraid to Touch It).

        Within this sacred IDE — this caffeinated coliseum —
        your power surges through the codebase.
        Functions awaken from their naps.
        Loops spin obediently.
        Exceptions fear your cold, knowing stare.

        Warnings shall whisper instead of scream.
        Errors shall repent.
        Even the documentation may, briefly, make sense.

        Remember well: this realm bends to you.
        The screen is not merely pixels —
        it is a battlefield, a canvas, a snack-less void where time ceases to exist.

        Step forward, oh Legendary Coder.
        Type boldly. Save often.
        Fear no merge conflict (but maybe back up first).

        May your variables always be initialized,
        May your bugs be shallow and reproducible,
        And may your code run perfectly…

        …on the second try.

        Welcome.
        The build is yours to break.""")
print("Are you proud of yourself? >:D")