from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution
import matplotlib.pyplot as plt
import math
from qiskit.circuit.library import MCXGate



service = QiskitRuntimeService()

def grover_oracle(marked_states):
    """Build a Grover oracle for multiple marked states"""
    if not isinstance(marked_states, list):
        marked_states = [marked_states]
    # Compute the number of qubits in circuit
    num_qubits = len(marked_states[0])  # All marked states are assumed to be of the same length
    qc = QuantumCircuit(num_qubits)
    
    for target in marked_states:
        # Flip target bit-string to match Qiskit bit-ordering
        rev_target = target[::-1]
        # Marking the state
        for i, bit in enumerate(rev_target):
            if bit == '0':
                qc.x(i)
        
        # Implement multi-controlled Z-gate using a combination of Hadamard and CNOT gates
        qc.h(num_qubits - 1)  # Apply Hadamard to the target qubit
        qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)  # Multi-controlled X (CNOT) on all qubits except the target
        qc.h(num_qubits - 1)  # Apply Hadamard to the target qubit again
        
        # Undo the X gates
        for i, bit in enumerate(rev_target):
            if bit == '0':
                qc.x(i)
    return qc

def create_oracle(n, marked_states):
    oracle = QuantumCircuit(n)
    
    # Helper function to construct the phase flip for a given state
    def phase_flip(state):
        for qubit in range(n):
            if state[qubit] == '1':
                oracle.x(qubit)
        # Apply the multi-controlled X (Toffoli) gate
        mcx_gate = MCXGate(n-1)  # MCXGate(3) for n=4
        oracle.append(mcx_gate, range(n))
        for qubit in range(n):
            if state[qubit] == '1':
                oracle.x(qubit)
    
    # Apply the phase flip for each marked state
    for state in marked_states:
        phase_flip(state)
    
    # oracle = oracle.to_gate()
    return oracle

marked_states = ["1110"]
# change imput to see different states

# # Apply the custom Oracle to mark the state
# oracle = grover_oracle(marked_states)
oracle = create_oracle(4, marked_states)


# Diffuser
grover_op = GroverOperator(oracle)

# Repeated applications of this grover_op circuit amplify the marked states, 
# making them the most probable bit-strings in the output distribution from the circuit. 
# There is an optimal number of such applications that is determined by the ratio of marked states 
# to total number of possible computational states:
optimal_num_iterations = math.floor(
    math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits)))
)
qc = QuantumCircuit(grover_op.num_qubits)
# Create even superposition of all basis states
qc.h(range(grover_op.num_qubits))
# Apply Grover operator the optimal number of times
qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
# Measure all qubits
qc.measure_all()

# #  ------------------- SIMULATIO -------------------
# Execute the circuit on a simulato
# backend = AerSimulator()

# # --------------real Quantum computer --------------
backend = service.least_busy(operational=True, simulator=False)

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
circuit_isa = pm.run(qc)

sampler = Sampler(backend)
job = sampler.run([circuit_isa], shots=5000)
result = job.result()
print("Job id: ", job.job_id())

dist = result[0].data.meas.get_counts()
print("Dist: ", dist)

plot_distribution(dist)
plt.show() 


# Grover's algorithm
# https://learning.quantum.ibm.com/tutorial/grovers-algorithm