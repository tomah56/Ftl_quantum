from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

service = QiskitRuntimeService()

job = service.job('cv29g28t1eag0085j9xg')
job_result = job.result()

pub_result = job.result()[0]
print("pub results:",  pub_result)
values = pub_result.data.meas.get_counts()
print("values:", values)
# print(job_result)
plot_histogram(values)
plt.show() 