from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

service = QiskitRuntimeService()

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
# def oracle(qc, n):
#     for i in range(n):
#         qc.cx(i, n)

def oracle(qc, n):
    # n is the number of qubits representing the input
    # Add a single qubit for the output
    output_qubit = n
    
    # Apply a series of CNOT gates to implement the parity check function
    for i in range(n):
        qc.cx(i, output_qubit)
    
    # Apply a final X gate to ensure the oracle function outputs 1 when the parity is odd
    qc.x(output_qubit)
    
    # Apply a final multi-controlled Z gate to flip the sign of the |1⟩ state
    qc.h(output_qubit)
    qc.mcx(list(range(n)), output_qubit)
    qc.h(output_qubit)


# Apply the oracle
oracle(qc, n)

# Apply Hadamard gates to input qubits after oracle
qc.h(range(n))

# Measure the input qubits
qc.measure(range(n), range(n))

# Execute the circuit on a simulator ----- SIMU -------
# aer_sim = AerSimulator()
# res = aer_sim.run(qc, shots=1, memory=True).result()
# measurements = res.get_memory()
# if "1" in measurements[0]:
#     print("balanced")
# else:
#     print("constant")
# ----- end SIMU -----

backend = service.least_busy(operational=True, simulator=False)


pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
transplie_opti = pm.run(qc)

sampler = Sampler(backend)
# execute the quantum circuit
job = sampler.run([transplie_opti], shots=500)
print("Job id: ", job.job_id())

results = job.result()


print("results: ", results)

pub_result = results[0]
print("pub results:",  pub_result)
# values = pub_result.data.meas.get_counts()
# print("values:", dir(pub_result.data))
# print("values:", pub_result.data.values())

# values = pub_result.data.meas.get_counts()
values = pub_result.data.c.array 


results = np.array(values)

# Convert the results into bitstrings
bitstrings = ['{:04b}'.format(int(res)) for res in results.flatten()]

# Count the occurrences of each bitstring
counts = Counter(bitstrings)

# Sort the bitstrings to display them in order
sorted_bitstrings = sorted(counts.keys())

# Prepare data for the histogram
x_values = sorted_bitstrings
y_values = [counts[bitstring] for bitstring in sorted_bitstrings]

# Plot the histogram
plt.figure(figsize=(10, 6))
plt.bar(x_values, y_values, color='blue')
plt.xlabel('Bitstring Outcome')
plt.ylabel('Count')
plt.title('Histogram of Quantum Measurement Outcomes')
plt.show()

# pub_result = results[0]
# print("pub results:",  pub_result)
# # values = pub_result.data.meas.get_counts()
# values = pub_result.data.c.array 
# values2 = pub_result.data.evs
# # values = pub_result.data.values()
# print("values:",values2)

# # To verify all entries, convert to a list and check
# all_results = list(values)  # Convert to list if it isn't already

# # Check if all elements are `[7]`
# uniform_result = all(entry == [7] for entry in all_results)

# print("All results are [7]:", uniform_result)

# # # Convert dict_values to a list
# # values_list = list(values)

# # # Now you can access the BitArray object
# # bit_array = values_list[0]

# # # Print or work with the BitArray object
# # print(bit_array)
# # print(counts)
# # Print the result

# # Interpretation of results
# # if '000' in counts and counts['000'] == 1024:
# #     print("The oracle is constant.")
# # else:
# #     print("The oracle is balanced.")

# # Plot the results
# # plot_histogram(counts)
# # plt.show()


# # https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/quantum-query-algorithms#section-the-deutsch-jozsa-algorithm