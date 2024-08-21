from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
import math
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution
import matplotlib.pyplot as plt

# service = QiskitRuntimeService()
service = QiskitRuntimeService()


def grover_oracle(marked_states, n):
    """Build a Grover oracle for multiple marked states

    Here we assume all input marked states have the same number of bits

    Parameters:
        marked_states (str or list): Marked states of oracle

    Returns:
        QuantumCircuit: Quantum circuit representing Grover oracle
    """
    if not isinstance(marked_states, list):
        marked_states = [marked_states]
    # Compute the number of qubits in circuit
    num_qubits = n

    qc = QuantumCircuit(num_qubits)
    # Mark each target state in the input list
    for target in marked_states:
        # Flip target bit-string to match Qiskit bit-ordering
        rev_target = target[::-1]
        # Find the indices of all the '0' elements in bit-string
        zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
        # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
        # where the target bit-string has a '0' entry
        qc.x(zero_inds)
        qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
        qc.x(zero_inds)
    return qc

def create_diffuser(n):
    """Create the Grover diffuser."""
    diffuser = QuantumCircuit(n)
    diffuser.h(range(n))
    diffuser.x(range(n))
    diffuser.h(n-1)
    diffuser.mcx(list(range(n-1)), n-1)  # Multi-controlled X gate
    diffuser.h(n-1)
    diffuser.x(range(n))
    diffuser.h(range(n))
    return diffuser.to_gate()

marked_states = ["011", "100"]

oracle = grover_oracle(marked_states)
# oracle.draw(output="mpl", style="iqp")
# plt.show() 

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

# Execute the circuit on a simulator ----- SIMU -------
# backend = AerSimulator()

# real Quantum computer
backend = service.least_busy(operational=True, simulator=False)


target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)

circuit_isa = pm.run(qc)

sampler = Sampler(backend)
# sampler.options.default_shots = 10_000
job = sampler.run([circuit_isa], shots=5000)
result = job.result()
print("Job id: ", job.job_id())

dist = result[0].data.meas.get_counts()
print("Dist: ", dist)

# ----- end SIMU -----
# allopt =  {'000': 0, '001': 0, '010': 0, '101': 0, '110': 0, '111': 0}

# combined_dict = {**allopt, **dist}

# # Sort the combined dictionary by the key names
# sorted_dict = dict(sorted(combined_dict.items()))

# plot_distribution(sorted_dict)
plot_distribution(dist)
plt.show() 








# Grover's algorithm
# https://learning.quantum.ibm.com/tutorial/grovers-algorithm