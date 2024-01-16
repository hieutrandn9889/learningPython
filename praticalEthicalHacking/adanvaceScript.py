#!/bin/python3
import sys  # system func and parameters
from datetime import datetime as dt
print(dt.now())

myName = "Heath"
print(myName[0])  # H
print(myName[-1])  # h

# split the name
sentence = "This is a sentence"
print(sentence[:4])  # this
print(sentence.split())  # ['This', 'is', 'a', 'sentence']

# join the name
sentence_split = sentence.split()
sentence_join = ' '.join(sentence_split)
print(sentence_join)  # This is a sentence

# symbol \\
quote = "He said, \"Give me money\""
print(quote)  # He said, "Give me money" # This is a quote

# cut space
too_much_space = "        Hello     "
print(too_much_space.strip())

# compare
letter = "A"
word = "Apple"
print(letter.lower() in word.lower())  # true

# join string
movie = " Hello"
print("That is a {} .".format(movie))  # That is a  Hello .

drinks = {"drinks1": 1, "drinks2": 2, "drinks3": 3}
print(drinks)

employees = {"employees1": ["Hihi", "HEHE",
                            "HUHU"], "employees2": ["HAHA", "KEKE"]}
print(employees)

employees['employees3'] = ['Mr.Hieu']
# {'employees1': ['Hihi', 'HEHE', 'HUHU'], 'employees2': ['HAHA', 'KEKE'], 'employees3': ['Mr.Hieu']}
print(employees)


# get value
drinks['drinks4'] = 9
print(drinks)  # {'drinks1': 1, 'drinks2': 2, 'drinks3': 3, 'drinks4': 9}
print(drinks.get('drinks4'))  # 9
