from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram, plot_distribution
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import matplotlib.pyplot as plt
from qiskit_aer.noise import NoiseModel


# Define the secret string (must be a binary string of length n)
secret_string = "1110"  # Change this to your secret string

# Convert the secret string to a list of integers for the oracle
def secret_to_list(secret_string):
    return [int(bit) for bit in secret_string]

# Define the function to create the Simon's oracle
def create_simon_oracle(secret_string):
    secret_list = secret_to_list(secret_string)
    n = len(secret_list)
    oracle = QuantumCircuit(2 * n)
    # Apply X gates to the ancilla qubits to prepare them in |1> state
    oracle.x(range(n))
    # Apply CNOT gates based on the secret string
    for i in range(n):
        if secret_list[i] == 1:
            oracle.cx(i, n + i)
    return oracle.to_gate()

# Number of qubits
n = len(secret_string)

# Create the Simon's oracle
oracle = create_simon_oracle(secret_string)

# Set up the quantum circuit
qc = QuantumCircuit(2 * n, n)

# Initialize the ancilla qubits
qc.h(range(n))
qc.x(range(n, 2 * n))
qc.h(range(n, 2 * n))

# Apply the Simon's oracle
qc.append(oracle, range(2 * n))

# Apply Hadamard gates again to the first n qubits
qc.h(range(n))

# Measure the first n qubits
qc.measure(range(n), range(n))

# Execute the circuit on a simulato
# apply noise simpulation
# noise_model = NoiseModel()
service = QiskitRuntimeService()
backendreal = service.backend("ibm_brisbane")
noise_model = NoiseModel.from_backend(backendreal)

backend = AerSimulator(noise_model=noise_model)

# # -------------- Quantum computer --------------
# backend = service.least_busy(operational=True, simulator=False)

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
circuit_isa = pm.run(qc)

sampler = Sampler(backend)

job = sampler.run([circuit_isa], shots=1000)
result = job.result()
print("Job id: ", job.job_id())

counts = result[0].data.c.get_counts()
print("Counts: ", counts)

plot_histogram(counts)
plt.show() 

# Analyze results to find the secret string
from collections import Counter

def find_secret_string(counts):
    max_count = max(counts.values())
    candidates = [k for k, v in counts.items() if v == max_count]
    return candidates[0]  # Return the most frequent result

# Find and print the most frequent result
discovered_secret = find_secret_string(counts)
print("Most frecvent reuslt (binary):", discovered_secret)

rev_target = discovered_secret[::-1]
print("The Secret string: ", rev_target)
