from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler


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
def oracle(qc, n):
    # Apply no operation, function f(x) = 0 or 1 for all x
    pass

# Oracle: Example of a balanced function oracle
# Uncomment this section for a balanced oracle
# def oracle(qc, n):
#     for i in range(n):
#         qc.cx(i, n)

# Apply the oracle
oracle(qc, n)

# Apply Hadamard gates to input qubits after oracle
qc.h(range(n))

# Measure the input qubits
qc.measure(range(n), range(n))

# Execute the circuit on a simulator
aer_sim = AerSimulator()
res = aer_sim.run(qc, shots=1, memory=True).result()
measurements = res.get_memory()
if "1" in measurements[0]:
    print("balanced")
else:
    print("constant")

# pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
# transplie_opti = pm.run(qc)

# sampler = Sampler(aer_sim)
# # execute the quantum circuit
# results = sampler.run([transplie_opti], shots=1024).result()
# print("results:", results)
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