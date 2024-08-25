from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator


print(" |Φ⁺⟩ = (|00⟩ - |11⟩) / √2 ")
bell = QuantumCircuit(2)

# Bell State |Φ⁺⟩ = (|00⟩ - |11⟩) / √2
bell.h(0)
# Apply a CNOT gate with the first qubit as control and the second qubit as target
bell.cx(0, 1)
# Apply a Z gate on the first qubit to create a phase shift
bell.z(0)

bell.measure_all()

# Visualize the quantum circuit
bell.draw('mpl')
plt.show()
 
backend = AerSimulator()
sampler = Sampler(backend)
job = sampler.run([bell], shots=500)
result = job.result()
print("Job id: ", job.job_id())
dist = result[0].data.meas.get_counts()
print("Dist: ", dist)
plot_histogram(dist)
plt.show() 

print(" |Ψ⁺⟩ = (|01⟩ + |10⟩) / √2 ")

bell = QuantumCircuit(2)
# Apply an X gate on the second qubit
bell.x(1)
bell.h(0)
# Apply a CNOT gate with the first qubit as control and the second qubit as target
bell.cx(0, 1)
# Visualize the quantum circuit
bell.draw('mpl')
plt.show()

bell.measure_all()
 
backend = AerSimulator()
sampler = Sampler(backend)
job = sampler.run([bell], shots=500)
result = job.result()
print("Job id: ", job.job_id())
dist = result[0].data.meas.get_counts()
print("Dist: ", dist)
plot_histogram(dist)
plt.show() 

print(" |Ψ⁺⟩ = (|01⟩ - |10⟩) / √2 ")

bell = QuantumCircuit(2)
# Apply an X gate on the second qubit
bell.x(1)
bell.h(0)
# Apply a CNOT gate with the first qubit as control and the second qubit as target
bell.cx(0, 1)
# Apply a Z gate on the first qubit to create a phase shift
bell.z(0)
# Visualize the quantum circuit
bell.draw('mpl')
plt.show()

bell.measure_all()
 
backend = AerSimulator()
sampler = Sampler(backend)
job = sampler.run([bell], shots=500)
result = job.result()
print("Job id: ", job.job_id())
dist = result[0].data.meas.get_counts()
print("Dist: ", dist)
plot_histogram(dist)
plt.show() 