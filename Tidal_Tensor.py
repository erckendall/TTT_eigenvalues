import numpy as np
import pyfftw
import random


n_samples = 15000 # random samples
dnty = np.load('rho_2_sm.npy')
dnty = np.log(dnty) # change for log or no log

delta = (dnty - np.average(dnty))/np.average(dnty)
resol = np.shape(dnty)[0]


# SET UP K-SPACE FOR RHO (REAL)
rkvec = 2 * np.pi * np.fft.fftfreq(resol, gridlength / float(resol))
krealvec = 2 * np.pi * np.fft.rfftfreq(resol, gridlength / float(resol))
rkxarray, rkyarray, rkzarray = np.meshgrid(rkvec, rkvec, krealvec, sparse=True, indexing='ij')
rkarray2 = rkxarray**2+rkyarray**2+rkzarray**2

# FIND FOURIER SPACE OVERDENSITY
rfft_delta = pyfftw.builders.rfftn(delta, axes=(0, 1, 2)) #Doesn't ever refer to real space coords
delta_k = rfft_delta(delta)
phi_k = delta_k*(rkarray2**-1)
phi_k[0,0,0] = 0.
Tidal_k = dict([])
k_vals = dict([(0,rkxarray), (1,rkyarray), (2, rkzarray)])
for i in range(3):
    for j in range(3):
        Tidal_k['{}{}{}'.format('Tk_', i, j)] = k_vals[i]*k_vals[j]*phi_k

# MAKE IT TRACELESS
for i in range(3):
    for j in range(3):
        if i == j:
            Tidal_k['{}{}{}'.format('Tk_', i, j)] = Tidal_k['{}{}{}'.format('Tk_', i, j)] - delta_k/3.
        else:
            Tidal_k['{}{}{}'.format('Tk_', i, j)] = Tidal_k['{}{}{}'.format('Tk_', i, j)]

Tidal = dict([])
irfft_funct = pyfftw.builders.irfftn(rkarray2, axes=(0, 1, 2))

cnt = -1
lst = []
for i in range(3):
    for j in range(3):
        cnt = cnt + 1
        lst.append(irfft_funct(Tidal_k['{}{}{}'.format('Tk_', i, j)]).copy())

ind_list = []
for i in range(resol):
    for j in range(resol):
        for k in range(resol):
            ind_list.append([i,j,k])

sample_list = random.sample(ind_list, n_samples)
results = []
for a in sample_list:
    matrx = np.zeros((3, 3))
    cnt = -1
    for i in range(3):
        for j in range(3):
            cnt = cnt + 1
            arr = lst[cnt]
            matrx[i][j] = np.real(arr[a[0], a[1], a[2]])
    diag = np.linalg.eig(matrx)
    new = np.real(diag[0]).tolist()
    if new[0] == 0 and new[1] == 0 and new[2] == 0:
        print('All eigenvalues zero')
    else:
        sml = new.index(min(new))
        lge = new.index(max(new))
        ord = [0,1,2]
        ord.remove(sml)
        ord.remove(lge)
        mid = ord[0]
        new = [[diag[0][lge],diag[1][lge]], [diag[0][mid],diag[1][mid]], [diag[0][sml],diag[1][sml]], a, delta[a[0], a[1], a[2]]]
        results.append(new)
results.append(resol)
np.save('TTT_sm.npy', results)

