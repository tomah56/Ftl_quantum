from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

service = QiskitRuntimeService()
# service = QiskitRuntimeService(
#     channel='ibm_quantum',
#     instance='ibm-q/open/main',
#     token='***'
# )
job = service.job('ctz4rx3zzp40008h2kqg')
job_result = job.result()

pub_result = job.result()[0]
print("pub results:",  pub_result)
values = pub_result.data.meas.get_counts()
print("values:", values)
# print(job_result)
plot_histogram(values)
plt.show() 
# To get counts for a particular pub result, use 
#
# pub_result = job_result[<idx>].data.<classical register>.get_counts()
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register. 
# You can use circuit.cregs to find the name of the classical registers.