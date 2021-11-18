import numpy as np
import matplotlib.pyplot as plt


results = np.load('TTT_lg.npy', allow_pickle=True).tolist()
tot = len(results)-1
rem_zeros = 0

lambda_1, lambda_2, lambda_3 = ([] for i in range(3))

for i in range(tot):
    lambda_1.append(np.real(results[i][0][0]))
    lambda_2.append(np.real(results[i][1][0]))
    lambda_3.append(np.real(results[i][2][0]))

count = 0
for item in lambda_1:
    if item < 10**(-1):
        count = count +1
print(count, tot)


########################## TO REMOVE ZERO VALUES
tot_1 = tot_2 = tot_3 = tot
if rem_zeros == 1:
    lambda_1_new = []
    for item in lambda_1:
        if abs(np.around(item, 6)) != 0.0:
            lambda_1_new.append(item)
    tot_1 = len(lambda_1_new)
    lambda_2_new = []
    for item in lambda_2:
        if abs(np.around(item, 6)) != 0.0:
            lambda_2_new.append(item)
    tot_2 = len(lambda_2_new)
    if tot_2 == 0:
        print('Warning - all lambda_2 values zero')
    lambda_3_new = []
    for item in lambda_3:
        if abs(np.around(item, 6)) != 0.0:
            lambda_3_new.append(item)
    tot_3 = len(lambda_3_new)
else:
    lambda_1_new = lambda_1
    lambda_2_new = lambda_2
    lambda_3_new = lambda_3



n_bins = 1500 # change for increased detail
rge = 1 # change for log or no log
bins = np.zeros(n_bins)
delta = rge/float(n_bins-1)
bins[0] = -0.5 * rge
list = []
for i in range(1, n_bins):
    bins[i] = bins[i - 1] + delta


prob_1, prob_2, prob_3 = (np.zeros(n_bins) for i in range(3))
for i in range(n_bins-1):
    prob_1[i] = np.count_nonzero(np.logical_and(bins[i] <= lambda_1_new, lambda_1_new < bins[i+1]))/(tot_1*delta)
    if tot_2 != 0:
        prob_2[i] = np.count_nonzero(np.logical_and(bins[i] <= lambda_2_new, lambda_2_new < bins[i+1]))/(tot_2*delta)
    prob_3[i] = np.count_nonzero(np.logical_and(bins[i] <= lambda_3_new, lambda_3_new < bins[i+1]))/(tot_3*delta)
np.save('prob_distros_lg.npy', [bins, prob_1, prob_2, prob_3])

