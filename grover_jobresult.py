from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_distribution
import matplotlib.pyplot as plt
import numpy as np

service = QiskitRuntimeService()
job = service.job('cv2z5yqfkm5g008pqs7g')

job_result = job.result()
pub_result = job.result()[0]
print("pub results:",  pub_result)
values = pub_result.data.c.get_counts()
print("values:", values)

# plot_histogram(values)
plot_distribution(values)

plt.show() 