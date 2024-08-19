from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

 # Number of qubits for the function, plus one ancillary
n = 3 

# Create the quantum circuit
qc = QuantumCircuit(n + 1, n)

# Initialize the ancillary qubit in state |1> and put input qubits in superposition
qc.x(n)
qc.h(range(n + 1))

# Oracle: Example of a constant function oracle
# Uncomment this section for a constant oracle
# def oracle(qc, n):
#     # Apply no operation, function f(x) = 0 or 1 for all x
#     pass

# Oracle: Example of a balanced function oracle
# Uncomment this section for a balanced oracle
def oracle(qc, n):
    for i in range(n):
        qc.cx(i, n)

# Apply the oracle
oracle(qc, n)

# Apply Hadamard gates to input qubits after oracle
qc.h(range(n))

# Measure the input qubits
qc.measure(range(n), range(n))

# Execute the circuit on a simulator
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=simulator, shots=1024).result()
counts = result.get_counts()

# Plot the results
plot_histogram(counts)
plt.show()

# Print the result
print(counts)

# Interpretation of results
if '000' in counts and counts['000'] == 1024:
    print("The oracle is constant.")
else:
    print("The oracle is balanced.")

# https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/quantum-query-algorithms#section-the-deutsch-jozsa-algorithm