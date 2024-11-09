# PURPOSE OF THIS CODE
# PROJECT
# DATE
# NAME

import numpy as np

fruits = np.array([["Apple","Banana","Blueberry","Cherry"],
["Coconut","Grapefruit","Kumquat","Mango"],
["Nectarine","Orange","Tangerine","Pomegranate"],
["Lemon","Raspberry","Strawberry","Tomato"]])

print(fruits[-1][-1])
print(fruits[:-1][1:3][:, :-1][:, 1:3])
print(fruits[[0, 2], :])
print(fruits[:-1][1:3][:, :-1][:, 1:3][::-1][:, ::-1])

x = fruits.copy()
x[:, [0,-1]] = x[:, [-1,0]]
print(x)

print([['SLICED!']*len(row) for row in fruits])
#print(fruits[:-1][1:3][:, -1][:, 1:3])