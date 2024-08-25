import numpy as np
import random
import itertools

# Define the secret string s
secret_string = "11"  # Example secret string of length 2

# Define the function f(x) with the hidden secret s
def f(x):
    n = len(secret_string)
    x_int = int(x, 2)  # Convert binary string to integer
    s_int = int(secret_string, 2)  # Convert secret string to integer
    output = bin(x_int ^ s_int if random.choice([True, False]) else x_int)[2:].zfill(n)
    return output

test = ["00", "01", "10", "11"]

print("examples:")
print("input x=00 | output: ", f("00"))
print("input x=00 | output: ", f("00"))
print("input x=01 | output: ", f("01"))
print("input x=10 | output: ", f("10"))
print("input x=11 | output: ", f("11"))

iter_test = itertools.cycle(test)

x = "00"
y = ""
first = f("00")
second = 0

for item in iter_test:
    second = f(item)
    if second == first:
        y = item
        break

x_int = int(x, 2)  # Convert binary string to integer
y_int = int(y, 2)
output = bin(x_int ^ y_int )[2:].zfill(2)

print("Secret string: ", output)

