from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

service = QiskitRuntimeService()
# service = QiskitRuntimeService(
#     channel='ibm_quantum',
#     instance='ibm-q/open/main',
#     token='***'
# )


# for EX04
# job = service.job('ctz4rx3zzp40008h2kqg')
# job_result = job.result()

# pub_result = job.result()[0]
# print("pub results:",  pub_result)
# values = pub_result.data.meas.get_counts()
# print("values:", values)
# # print(job_result)
# plot_histogram(values)
# plt.show() 

#  for EX05
# Balancend function job
job = service.job('cv29g28t1eag0085j9xg')

# Constant function job
# job = service.job('cv28srq184p00089kv0g')


# print("job: ", job.properties())
# print("job: ", dir(job.properties()))

job_result = job.result()

pub_result = job.result()[0]
print("pub results:",  pub_result)
# values = pub_result.data.meas.get_counts()
# print("values:", dir(pub_result.data))
# print("values:", pub_result.data.values())

# values = pub_result.data.meas.get_counts()
values = pub_result.data.c.array 
values = pub_result.data.c.get_counts()

print("values:", values)

# results = np.array(values)

# # Convert the results into bitstrings
# bitstrings = ['{:04b}'.format(int(res)) for res in results.flatten()]

# # Count the occurrences of each bitstring
# counts = Counter(bitstrings)

# # Sort the bitstrings to display them in order
# sorted_bitstrings = sorted(counts.keys())

# # Prepare data for the histogram
# x_values = sorted_bitstrings
# y_values = [counts[bitstring] for bitstring in sorted_bitstrings]

# # Plot the histogram
# plt.figure(figsize=(10, 6))
# plt.bar(x_values, y_values, color='blue')
# plt.xlabel('Bitstring Outcome')
# plt.ylabel('Count')
# plt.title('Histogram of Quantum Measurement Outcomes')
# plt.show()


# values2 = pub_result.data.evs
# values = pub_result.data.values()
# print("values:",values2)


# print(job_result)
# plot_histogram(values)
# plt.show() 




# To get counts for a particular pub result, use 
#
# pub_result = job_result[<idx>].data.<classical register>.get_counts()
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register. 
# You can use circuit.cregs to find the name of the classical registers.