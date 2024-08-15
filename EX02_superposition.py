from qiskit_aer import AerSimulator
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler, QiskitRuntimeService
import matplotlib.pyplot as plt
from collections import Counter


service = QiskitRuntimeService()
 
# Bell Circuit 1 qubit and 1 classic bit for messurements
qc = QuantumCircuit(1, 1)
# Hadamard gate to the qubit to create a superposition
qc.h(0)
qc.measure(0, 0)
qc.draw("mpl")
plt.show()

aer_sim = AerSimulator()
pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
isa_qc = pm.run(qc)
with Session(backend=aer_sim) as session:
    sampler = Sampler()
    result = sampler.run([isa_qc], shots=500).result()._pub_results

print(" - - - - - - - - - - - > myresutlst:")
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
