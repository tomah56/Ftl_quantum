import itertools
import random

# Function to generate all binary strings of length n
def generate_binary_strings(n):
    return [bin(i)[2:].zfill(n) for i in range(2**n)]

# Example secret string
secret_string = "1101100010110101110"  # Change the length of the secret string as needed

# Define the function f(x) with the hidden secret s
def f(x):
    n = len(secret_string)
    x_int = int(x, 2)  # Convert binary string to integer
    s_int = int(secret_string, 2)  # Convert secret string to integer
    output = bin(x_int ^ s_int if random.choice([True, False]) else x_int)[2:].zfill(n)
    return output

# Generate the test list based on the length of the secret string
test = generate_binary_strings(len(secret_string))
# print(test)

# Print examples
# print("Examples:")
# for item in test:
#     print(f"input x={item} | output: {f(item)}")

# Iterate through test list to find the pair that produces the same output
iter_test = itertools.cycle(test)

x = test[0]  # Starting point for comparison
y = ""
first = f(x)
second = ""

for item in iter_test:
    second = f(item)
    if item != test[0] and second == first:
        y = item
        break

# Output the result
x_int = int(x, 2)  # Convert binary string to integer
y_int = int(y, 2)
# print("Solution inputs: ", x_int, y_int)
output = bin(x_int ^ y_int)[2:].zfill(len(secret_string))

print("Secret string:", output)


# Secret string: 110110
# python general_classicalproblem_simon.py  0.02s user 0.01s system 91% cpu 0.027 total
# Secret string: 1101110
# python general_classicalproblem_simon.py  0.02s user 0.01s system 91% cpu 0.029 total
# Secret string: 11011110
# python general_classicalproblem_simon.py  0.02s user 0.01s system 91% cpu 0.029 total
# Secret string: 11011001110
# python general_classicalproblem_simon.py  0.02s user 0.01s system 92% cpu 0.031 total
# Secret string: 110110011001110
# python general_classicalproblem_simon.py  0.05s user 0.01s system 95% cpu 0.065 total
# Secret string: 1101100101001110
# python general_classicalproblem_simon.py  0.09s user 0.01s system 97% cpu 0.101 total
# Secret string: 11011001010101110
# python general_classicalproblem_simon.py  0.67s user 0.01s system 99% cpu 0.688 total