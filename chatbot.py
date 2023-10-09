import random
import string
import time

import pyautogui as py

characters = string.ascii_letters
numbers = string.digits
length = input("Length of char or nums: ")
number = input("No of messages: ")
choice = input("Characters or numbers: ")

if choice == "c":
    py.typewrite("This is bot message characters:")
    for i in range(int(number)):
        output = "".join(random.sample(characters, int(length)))
        py.typewrite(output)
        py.press('Enter')
        time.sleep(2)

elif choice == "n":
    py.typewrite("This is bot message numbers:")
    for i in range(int(number)):
        output = "".join(random.sample(numbers, int(length)))
        py.typewrite(output)
        py.press('Enter')
        time.sleep(2)
else:
    print("Pls make a choice from characters or numbers")
