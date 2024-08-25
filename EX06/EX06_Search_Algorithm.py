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

def create_oracle_mark_1111():
    """
    Create a quantum oracle that marks the state |1111⟩ for a n-qubit system.
    
    Parameters:
    n (int): Number of qubits (should be 4 for this example).

    Returns:
    QuantumCircuit: The oracle as a quantum circuit.
    """
    n = 4
    oracle = QuantumCircuit(n)
    # oracle.barrier()
    
    # Step 1: Apply X gates to all qubits to map |1111⟩ to |0000⟩
    # oracle.x(range(n))
    # oracle.h(n-1)  # Apply Hadamard to the last qubit
    # oracle.cz(0,1)
    # oracle.cz(0,2)
    oracle.cz(0,3)
    # oracle.cz(0,0)
    # oracle.h(3)  # Reapply Hadamard to the last qubit
    
    # # Step 2: Apply a multi-controlled Z gate (Toffoli gate in this case)
    oracle.mcx(list(range(n-1)), n-1)   # Multi-controlled X (flips the phase of |0000⟩ -> |1111⟩)
    
    # # Step 3: Reapply X gates to revert back to original basis
    oracle.x(range(n))
    
    return oracle.to_gate()

def grover_oracle_0110_1000():
    """Build a Grover oracle for multiple marked states

    Here we assume all input marked states have the same number of bits

    Parameters:
        marked_states (str or list): Marked states of oracle

    Returns:
        QuantumCircuit: Quantum circuit representing Grover oracle
    """
    # Compute the number of qubits in circuit
    num_qubits = 4

    qc = QuantumCircuit(num_qubits)
    # Mark each target state in the input list
    
        # Flip target bit-string to match Qiskit bit-ordering
    target = "0110"
    rev_target = target[::-1]
    # Find the indices of all the '0' elements in bit-string
    zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
    # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
    # where the target bit-string has a '0' entry
    qc.x(zero_inds)
    qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
    qc.x(zero_inds)

    # target = "1000"
    # rev_target = target[::-1]
    # # Find the indices of all the '0' elements in bit-string
    # zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
    # # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
    # # where the target bit-string has a '0' entry
    # qc.x(zero_inds)
    # qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
    # qc.x(zero_inds)

    # target = "1011"
    # rev_target = target[::-1]
    # # Find the indices of all the '0' elements in bit-string
    # zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
    # # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
    # # where the target bit-string has a '0' entry
    # qc.x(zero_inds)
    # qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
    # qc.x(zero_inds)

    return qc.to_gate()

def oracle_mark_1111_1010(n):
    """
    Create an oracle that marks the |1111⟩ and |1010⟩ states by flipping their phases.

    Parameters:
    n (int): The number of qubits.

    Returns:
    QuantumCircuit: The oracle as a quantum circuit.
    """
    oracle = QuantumCircuit(n)
    
    # Phase flip for |1111⟩
    oracle.x(range(n))                  # Apply X to all qubits to map |1111⟩ to |0000⟩
    oracle.h(n-1)                       # Apply Hadamard to the last qubit
    oracle.mcx(list(range(n-1)), n-1)   # Multi-controlled X (flips the phase of |0000⟩ -> |1111⟩)
    oracle.h(n-1)                       # Revert Hadamard on the last qubit
    oracle.x(range(n))                  # Revert X on all qubits

    # Phase flip for |1010⟩
    oracle.x([0, 2])                    # Apply X to qubits 0 and 2 to map |1010⟩ to |1111⟩
    oracle.h(n-1)                       # Apply Hadamard to the last qubit
    oracle.mcx(list(range(n-1)), n-1)   # Multi-controlled X (flips the phase of |1111⟩ -> |1010⟩)
    oracle.h(n-1)                       # Revert Hadamard on the last qubit
    oracle.x([0, 2])                    # Revert X on qubits 0 and 2
    
    # return oracle.to_gate(name="Oracle")
    return oracle.to_gate()

def oracle_oooo():
    n = 4
    oracle = QuantumCircuit(n)

    # Apply an X gate to each qubit to flip |0000> to |1111>
    # This step is optional since |0000> doesn't need X gates, but it's here for understanding.
    # No need to apply X gates here because we're working with |0000⟩.

    # Apply a multi-controlled Z gate (a.k.a. multi-controlled phase flip)
    oracle.h(n-1)              # Apply H-gate to the last qubit to make the MCZ operation
    oracle.mcx(list(range(n-1)), n-1)  # Multi-controlled X gate acting as MCZ
    oracle.h(n-1)              # Apply H-gate again to change basis back
    return oracle.to_gate()

def diffuser(n):
    """
    Create the Grover diffusion operator (inversion about the mean) for n qubits.

    Parameters:
    n (int): The number of qubits.

    Returns:
    QuantumCircuit: The diffuser as a quantum circuit.
    """
    diff = QuantumCircuit(n)
    
    # Apply Hadamard to all qubits
    diff.h(range(n))
    
    # Apply X (NOT) to all qubits
    diff.x(range(n))
    
    # Apply multi-controlled Z-gate (which is a multi-controlled X followed by a Hadamard)
    diff.h(n-1)                      # Apply Hadamard to the last qubit to prepare for the Z operation
    diff.mcx(list(range(n-1)), n-1)  # Multi-controlled X gate (acts as a Z on |1111⟩ after X gates)
    diff.h(n-1)                      # Revert Hadamard on the last qubit
    
    # Apply X (NOT) to all qubits again to revert the X transformation
    diff.x(range(n))
    
    # Apply Hadamard to all qubits again
    diff.h(range(n))
    
    return diff.to_gate()


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
    return qc.to_gate()

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

# Not any state can be selected in a given oracle. most state needs specific oracle to mark them.
# marked_states = ["0000"]
# marked_states = ["011", "100"]
n = 4
# # Apply the custom Oracle to mark the state
# oracle = create_oracle(4, marked_states)
# oracle = grover_oracle(marked_states)

grover_circuit = QuantumCircuit(n, n)
grover_circuit.h(range(n))  # Apply Hadamard gates to create superposition

# Apply the oracle
# oracle = oracle_oooo()
oracle = grover_oracle_0110_1000()
# oracle = create_oracle_mark_1111()

# oracle = oracle_mark_1111_1010(n)

# grover_circuit.append(oracle, range(n))

# Apply Grover's diffusion operator
diffuser_gate = diffuser(n)

# grover_circuit.append(diffuser_gate, range(n))

for _ in range(1):
    grover_circuit.append(oracle, range(n))
    grover_circuit.append(diffuser_gate, range(n))


grover_circuit.measure(range(n), range(n))

# #  ------------------- SIMULATIO -------------------
# Execute the circuit on a simulato
# backend = AerSimulator()

# # --------------real Quantum computer --------------
backend = service.least_busy(operational=True, simulator=False)

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
circuit_isa = pm.run(grover_circuit)
# circuit_isa = pm.run(qc)

sampler = Sampler(backend)

# Turn on dynamical decoupling with sequence XpXm.
sampler.options.dynamical_decoupling.enable = True
sampler.options.dynamical_decoupling.sequence_type = "XpXm"

job = sampler.run([circuit_isa], shots=1000)
result = job.result()
print("Job id: ", job.job_id())

# dist = result[0].data.meas.get_counts()
dist = result[0].data.c.get_counts()
print("Dist: ", dist)

plot_distribution(dist)
plt.show() 


# Grover's algorithm
# https://learning.quantum.ibm.com/tutorial/grovers-algorithm