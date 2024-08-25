from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_distribution
import matplotlib.pyplot as plt
import numpy as np

service = QiskitRuntimeService()
job = service.job('cv3h8xb1vt8g008a36v0')

job_result = job.result()
pub_result = job.result()[0]
print("pub results:",  pub_result)
values = pub_result.data.c.get_counts()
# values = pub_result.data.meas.get_counts()
print("values:", values)

# plot_histogram(values)
plot_distribution(values)

plt.show() 