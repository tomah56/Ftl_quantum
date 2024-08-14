from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
 
# Create empty circuit
example_circuit = QuantumCircuit(2)
example_circuit.measure_all()
 
# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
service = QiskitRuntimeService()
# backend = service.least_busy(operational=True, simulator=False)

# there are no simulators. 
# backend = service.backends(simulator=True, operational=True)

backend_list = service.backends(simulator=False, operational=True)
# [<IBMBackend('ibm_brisbane')>, <IBMBackend('ibm_kyoto')>, <IBMBackend('ibm_osaka')>, <IBMBackend('ibm_sherbrooke')>]

for backend in backend_list:
    # Extract the text between the single quotes using string methods
    # start_index = backend.find("'") + 1  # Find the position of the first quote
    # end_index = backend.rfind("'")       # Find the position of the last quote
    # backend_name = backend[start_index:end_index]  # Extract the substring
    print(
        f"Name: {backend.name}\n"
        f"Version: {backend.version}\n"
        f"No. of qubits: {backend.num_qubits}\n"
        f"jobs in queue: {backend.status().pending_jobs}\n"
    )

    # Print the extracted backend name
    # print(backend_name)

# backend = service.backend("ibm_kyoto")
 
# print(
#     f"Name: {backend.name}\n"
#     f"Version: {backend.version}\n"
#     f"No. of qubits: {backend.num_qubits}\n"
#     f"jobs in queue: {backend.status().pending_jobs}\n"
# )
 
# print(backend)

# status = backend.status()
# is_operational = status.operational
# jobs_in_queue = status.pending_jobs

# print(f"Operation of {status.name}")
# print(is_operational)
# print("Quee")
# print(jobs_in_queue)

# sampler = Sampler(backend)
# job = sampler.run([example_circuit])
# print(f"job id: {job.job_id()}")
# result = job.result()
# print(result)



# print(backend_simu.__len__())  # T
# print(backend_list.__len__())  # T
# print(dir(backend_list))
# obj_type = type(backend_simu)
