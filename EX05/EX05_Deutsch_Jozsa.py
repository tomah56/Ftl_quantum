from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit_aer.noise import NoiseModel


service = QiskitRuntimeService()

# Number of qubits for the function, plus one ancillary.
# The ancillary qubit's role is to facilitate quantum interference
#  by interacting with the control qubits via the oracle
n = 3 

# Create the quantum circuit
qc = QuantumCircuit(n + 1, n)

# Initialize the ancillary qubit in state |1> and put input qubits in superposition
qc.x(n)
qc.h(range(n + 1))

# Oracle: Example of a constant function oracle
# def oracle(qc, n):
#     # Apply no operation, function f(x) = 0 or 1 for all x
#     pass

# Oracle: Example of a balanced function oracle
# For each control qubit that is ∣1⟩, the ancillary qubit flips its state 
# (from ∣1⟩ to ∣0⟩, or vice versa).
def oracle(qc, n):
    for i in range(n):
        qc.cx(i, n)

# Balanced 2
def oracle_II(qc, n):
     # n is the number of qubits representing the input
    # Add a single qubit for the output
    output_qubit = n
    # Apply the XOR pattern
    for i in range(n):
        qc.cx(i, output_qubit)
    # Apply a Z gate to flip the sign of the |1⟩ state if needed
    qc.z(output_qubit)
    # Apply a final X gate to ensure the output is 1 for the correct cases
    qc.x(output_qubit)

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
# backendreal = service.backend("ibm_brisbane")
# noise_model = NoiseModel.from_backend(backendreal)

# backend = AerSimulator(noise_model=noise_model)

# ----- end SIMU -----

backend = service.least_busy(operational=True, simulator=False)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
transplie_opti = pm.run(qc)

sampler = Sampler(backend)
# execute the quantum circuit
job = sampler.run([transplie_opti], shots=500)
print("Job id: ", job.job_id())

results = job.result()
# print("results: ", results)

pub_result = results[0]
# print("pub results:",  pub_result)

values = pub_result.data.c.get_counts()

print("values:", values)
plot_histogram(values)
plt.show() 


# Hadamard gates are applied again to the control qubits.
# This step effectively "undoes" the superposition if the oracle is constant,
#  collapsing the control qubits back to the ∣000⟩ state.
# If the oracle is balanced, the superposition states interfere destructively for the ∣000⟩ state, 
# causing at least one of the control qubits to be measured as ∣1⟩.
# https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/quantum-query-algorithms#section-the-deutsch-jozsa-algorithm