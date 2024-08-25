def evaluate_function(func):
    inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    results = [func(x) for x in inputs]

    print(f"Function outputs: {results}")

    if all(result == results[0] for result in results):
        print("The function is constant.")
    elif results.count(0) == len(results) // 2 and results.count(1) == len(results) // 2:
        print("The function is balanced.")
    else:
        print("The function is neither constant nor balanced (this should not happen in our case).")

# Example constant function
def constant_function(x):
    return 0

# he XOR operation is a fundamental logical operation that outputs 1 
# only when the two input bits are different 1,0 -> 1... 1,1 -> 0
# Example balanced function
def balanced_function(x):
    return x[0] ^ x[1]

# Testing the functions
print("Testing constant function:")
evaluate_function(constant_function)

print("\nTesting balanced function:")
evaluate_function(balanced_function)
