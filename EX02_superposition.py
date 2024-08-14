import qiskit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import RealAmplitudes
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler, QiskitRuntimeService
from qiskit.visualization import plot_histogram, plot_state_city
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
 
service = QiskitRuntimeService()
 
# Bell Circuit
qc = QuantumCircuit(1, 1)
# Hadamard gate to the qubit to create a superposition
qc.h(0)

# qc.cx(0, 1)
# qc.measure_all()

qc.measure(0, 0)



# qc.draw("mpl")
# Run the sampler job locally using AerSimulator.
# Session syntax is supported but ignored because local mode doesn't support sessions.
# Construct an ideal simulator
aer_sim = AerSimulator()
pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
isa_qc = pm.run(qc)
with Session(backend=aer_sim) as session:
    sampler = Sampler()
    result = sampler.run([isa_qc], shots=500).result()._pub_results
print(" - - - - - - - - - - - > myresutlst:")

# print(result[0].data.c.array )
# print(dir(result[0].data.c) )
real_resurts = result[0].data.c.array 
# Flatten the 2D array to a 1D array
flat_results = real_resurts.flatten()

# Count the occurrences of each result
counts = Counter(flat_results)

# Calculate the total number of measurements
total_shots = len(flat_results)

# Calculate probabilities for each outcome
probabilities = {outcome: count / total_shots for outcome, count in counts.items()}

# Plotting the histogram
plt.bar(probabilities.keys(), probabilities.values(), color=['blue', 'orange'])
plt.xlabel('Measurement Outcomes')
plt.ylabel('Probability')
plt.title('Measurement Outcome Probabilities')
plt.xticks([0, 1], ['0', '1'])
plt.ylim(0, 1)

# Adding text on top of each bar
for outcome, probability in probabilities.items():
    plt.text(outcome, probability, f'{probability:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.show()



# print(dir(result))

# print(dir(result))
# print(result._pub_results)
# Extracting data
# sampler_pub_result = result.data
# print(sampler_pub_result)
# bit_array = sampler_pub_result.data.c

# print(bit_array)

# counts = result.quasi_dists[0].binary_probabilities()

# # Convert bitstrings to integers if necessary
# counts_dict = {int(key, 2): value for key, value in counts.items()}

# # Plotting histogram
# plot_histogram(real_resurts)
# plt.show()
# counts = result.get_counts(qc)
# plot_histogram(counts, title='Bell-State counts')
# Perform an ideal simulation
# result_ideal = qiskit.execute(qc, aer_sim).result()
# counts_ideal = result_ideal.get_counts(0)
# print('Counts(ideal):', counts_ideal)
# Counts(ideal): {'000': 493, '111': 531}


# # Step 3: Generate a preset pass manager for transpiling the circuit
# pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)

# # Step 4: Transpile the circuit using the pass manager
# isa_qc = pm.run(qc)

# # Step 5: Execute the transpiled circuit using the AerSimulator
# job = execute(isa_qc, backend=aer_sim, shots=500)
# result = job.result()

# # Step 6: Get the counts (measurement results)
# counts = result.get_counts(isa_qc)
# print("Measurement Results:")
# print(counts)

# # Step 7: Plot a histogram of the results
# plot_histogram(counts)