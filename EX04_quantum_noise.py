from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

 
# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
service = QiskitRuntimeService()
 
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# quantum circuit to make a Bell state
# two qbut with 2 classical bit for mesurment
bell = QuantumCircuit(2,2)


bell.h(0)
# Apply a CNOT gate with the first qubit as control and the second qubit as target
bell.cx(0, 1)
# bell.measure([0, 1], [0, 1])

bell.measure_all()

# Visualize the quantum circuit
# bell.draw('mpl')
# plt.show()

# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
transplie_opti = pm.run(bell)

sampler = Sampler(backend)
# execute the quantum circuit
results = sampler.run([transplie_opti], shots=500).result()
print("results:", results)

pub_result = results[0]
print("pub results:",  pub_result)
values = pub_result.data.meas.get_counts()
print("values:", values)
plot_histogram(values)
plt.show() 
