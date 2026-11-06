"""Loops"""

"""While loop"""

# A while-loop is a control flow statement for specifying iteration, which allows code to be executed repeatedly.

# TODO: Write a while loop that prints break_condition and increments it, until it reaches 5

break_condition = 0

while break_condition < 10:   
    break_condition += 1
    print(break_condition)
else:
    print("Loop finished")

print("out of while loop")

# ----------------------------------------------

"""For loop"""

# For-loop is a control flow statement for specifying iteration, which allows code to be executed repeatedly.

# TODO: Iterate over pets, printing each one

pets = ["dog", "cat", "horse", "rabbit", "snake"]

for pet in pets:
    print(pet)

my_list = [30,70]

for i in my_list:
    print(i-20)

for i in range(5):
    print(i)