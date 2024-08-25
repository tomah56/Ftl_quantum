from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.circuit.library import GroverOperator
from qiskit.visualization import plot_distribution
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import DensityMatrix, Operator


service = QiskitRuntimeService()

mark_state = Statevector.from_label('1001')
diffuse_operator = 2 * DensityMatrix.from_label('0000') - Operator.from_label('IIII')
print(diffuse_operator)
grover_op = GroverOperator(oracle=mark_state, zero_reflection=diffuse_operator)

qc = QuantumCircuit(grover_op.num_qubits)
# Create even superposition of all basis states
qc.h(range(grover_op.num_qubits))
qc.compose(grover_op, inplace=True)

# Measure all qubits
qc.measure_all()

# #  ------------------- SIMULATIO -------------------
# Execute the circuit on a simulato
backend = AerSimulator()

# # --------------real Quantum computer --------------
# backend = service.least_busy(operational=True, simulator=False)

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
circuit_isa = pm.run(qc)

sampler = Sampler(backend)

# Turn on dynamical decoupling with sequence XpXm.
sampler.options.dynamical_decoupling.enable = True
sampler.options.dynamical_decoupling.sequence_type = "XpXm"

job = sampler.run([circuit_isa], shots=1000)
result = job.result()
print("Job id: ", job.job_id())

dist = result[0].data.meas.get_counts()
print("Dist: ", dist)

plot_distribution(dist)
plt.show() 


# Grover's algorithm
# https://learning.quantum.ibm.com/tutorial/grovers-algorithm