import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as spi


################################### To plot the chosen density fields
# data = np.load('rho_2_sm.npy')
# sl = data[64]
# newsl = np.zeros((100, 100))
# for i in range(100):
#     for j in range(100):
#         newsl[i][j] = sl[i+14][j+14]
# np.save('small_field.npy', newsl)
# plt.axes(aspect='equal')
# plt.contourf(np.log(newsl), 100)
# plt.xticks([])
# plt.yticks([])
# plt.show()



################################################## PROBABILITY DISTROS
for case in ['prob_distros_lg', 'prob_distros_sm']:
    data = np.load('{}{}'.format(case, '.npy'), allow_pickle=True).tolist()
    bins = data[0]
    prob_1, prob_2, prob_3 = (data[i + 1] for i in range(3))


    ################# if zeros delete
    comb_1, comb_2, comb_3 = ([] for i in range(3))
    comb_1_n, comb_2_n, comb_3_n = ([] for i in range(3))
    bins_1, bins_2, bins_3 = ([] for i in range(3))
    for i in range(len(bins)):
        comb_1.append([bins[i], prob_1[i]])
        comb_2.append([bins[i], prob_2[i]])
        comb_3.append([bins[i], prob_3[i]])


    for i in comb_1:
        if i[1] != 0.:
            comb_1_n.append(i)
    lent = len(comb_1_n)
    prob_1 = []
    for i in range(lent):
        bins_1.append(comb_1_n[i][0])
        prob_1.append(comb_1_n[i][1])

    for i in comb_2:
        if i[1] != 0.:
            comb_2_n.append(i)
    lent = len(comb_2_n)
    prob_2 = []
    for i in range(lent):
        bins_2.append(comb_2_n[i][0])
        prob_2.append(comb_2_n[i][1])

    for i in comb_3:
        if i[1] != 0.:
            comb_3_n.append(i)
    lent = len(comb_3_n)
    prob_3 = []
    for i in range(lent):
        bins_3.append(comb_3_n[i][0])
        prob_3.append(comb_3_n[i][1])


    plt.figure(figsize=(4.5,3.5))
    plt.scatter(bins_1, prob_1, s=1, alpha=0.4)
    plt.scatter(bins_2, prob_2, s=1, alpha=0.4)
    plt.scatter(bins_3, prob_3, s=1, alpha=0.4)
    f1 = spi.splrep(bins_1, prob_1, s=0.9)
    f2 = spi.splrep(bins_2, prob_2, s=0.9)
    f3 = spi.splrep(bins_3, prob_3, s=0.9)

    xnew_1 = np.arange(min(bins_1), max(bins_1), (max(bins_1)-min(bins_1))*2/(len(bins_1)))
    xnew_2 = np.arange(min(bins_2), max(bins_2), (max(bins_2)-min(bins_2))*2/(len(bins_2)))
    xnew_3 = np.arange(min(bins_3), max(bins_3), (max(bins_3)-min(bins_3))*2/(len(bins_3)))

    ynew1 = spi.splev(xnew_1, f1, der=0)
    ynew2 = spi.splev(xnew_2, f2, der=0)
    ynew3 = spi.splev(xnew_3, f3, der=0)


    plt.plot(xnew_1,ynew1, label='$\lambda_1$')
    plt.plot(xnew_2,ynew2, label='$\lambda_2$')
    plt.plot(xnew_3,ynew3, label='$\lambda_3$')
    plt.ylim(0, 35) #change range depending on log or no log
    plt.xlim(-0.4, 0.4)
    plt.legend(frameon=False)
    plt.xlabel('$\lambda$')
    plt.ylabel('p($\lambda$)')
    plt.tight_layout()
    plt.savefig('{}{}'.format(case, '.jpg'))

plt.show()



