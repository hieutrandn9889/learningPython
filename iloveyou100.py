import pyautogui as py
import time

message = "I love you"
count = 1
time.sleep(2)

for i in range(2):
    py.typewrite(message + " " + str(count))
    py.press('Enter')
    time.sleep(2)
    count = count + 1

py.typewrite("I love you 100")
py.press('Enter')