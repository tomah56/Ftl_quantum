from qiskit_aer.primitives import Sampler
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# quantum circuit to make a Bell state
# two qbut with 2 classical bit for mesurment
# bell = QuantumCircuit(2,2)
# two qubit no mesurment bits in simulations focusing on the quantum operation
bell = QuantumCircuit(2)
bell.h(0)
# Apply a CNOT gate with the first qubit as control and the second qubit as target
bell.cx(0, 1)
# bell.measure([0, 1], [0, 1])

bell.measure_all()

# Visualize the quantum circuit
bell.draw('mpl')
plt.show()
 
# execute the quantum circuit
quasi_dists = Sampler().run(bell, shots=500).result().quasi_dists[0]
print(quasi_dists)

# Plot results with custom options
plot_histogram(quasi_dists)

# Execute two-qubit Bell state again
# second_quasi_dists = Sampler().run(bell, shots=500).result().quasi_dists[0]
#  
# Plot results with custom options
# plot_histogram(
#     [quasi_dists, second_quasi_dists],
#     legend=["first", "second"],
#     sort="desc",
#     figsize=(15, 12),
#     color=["orange", "black"],
#     bar_labels=True,
# )

plt.show() 