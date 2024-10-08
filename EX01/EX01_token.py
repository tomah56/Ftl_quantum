from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
 
# initializing QiskitRuntimeService, if they were not previously saved you have to give your token.
service = QiskitRuntimeService()

# Why are the cloud simulators being retired?
# The cloud simulators are being retired for several reasons:

# Simulators have limitations
# Using quantum hardware builds unique skills
# Algorithms should be adapted for quantum hardware

print("List of Quantum Simulators:")
backend_simu = service.backends(simulator=True, operational=True)

if backend_simu.__len__() == 0: 
    print("    ---->There are no Quantum Simulators!")
else:
    for backend in backend_simu:
        print(
            f"Name: {backend.name}\n"
            f"Version: {backend.version}\n"
            f"jobs in queue: {backend.status().pending_jobs}\n"
        )

print("List of Quantum computers:")
backend_list = service.backends(simulator=False, operational=True)

if backend_list.__len__() == 0: 
    print("    ---->There are no availabe Quantum computers!")
else:
    for backend in backend_list:
        print(
            f"Name: {backend.name}\n"
            f"Version: {backend.version}\n"
            f"No. of qubits: {backend.num_qubits}\n"
            f"jobs in queue: {backend.status().pending_jobs}\n"
        )