import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import butter, filtfilt
from scipy import signal
import scipy.signal as signal
from datetime import datetime
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

predata_list = pd.read_csv(r'C:\Users\Desktop\FPdata.csv') # write the path to the concatenated data file

pda = np.array(predata_list)
temp_i = pda[:,0].astype(np.float)
temp_t = pda[:,1].astype(np.float)
temp_m = pda[:,2].astype(np.float)
temp_f = pda[:,3].astype(np.float)

#######################################

for i in range(temp_f.shape[0]):
    if temp_f[i] > 2000:
        temp_f[i] = temp_f[i] % 100

##################### cut of frequencies of second-order butterworth filters

N = 2    # Filter order
Wn_notch = 45, 55
Wn_bandpass_f = 1, 99
Wn_bandpass_p = 1, 38.5
##################### filter design

###band-stop filter (notch)
F, E = signal.butter(N, Wn_notch, btype='bandstop', analog=False, output='ba', fs=200)
###band-pass filter (high+low) for pressure
A, B = signal.butter(N, Wn_bandpass_p, btype='bandpass', analog=False, output='ba', fs=78)
###band-pass filter (high+low) for force
H, G = signal.butter(N, Wn_bandpass_f, btype='bandpass', analog=False, output='ba', fs=200)

##################### filtering force
f = signal.filtfilt(F, E, temp_f)
tempf = signal.filtfilt(H, G, f)
temp_f_filtered = f-tempf

##################### filtering index finger's pressure
tempi = signal.filtfilt(A, B, temp_i)
temp_i_filtered = temp_i-tempi

##################### filtering thumb's pressure
tempt = signal.filtfilt(A, B, temp_t)
temp_t_filtered = temp_t-tempt

##################### filtering middle finger's pressure
tempm = signal.filtfilt(A, B, temp_m)
temp_m_filtered = temp_m-tempm

######################### data reconstruction

dim = np.shape(temp_i_filtered)[0]
final_temp = np.zeros((dim, 4))
for i in range(dim):
        final_temp[i,0] = temp_i_filtered[i]
        final_temp[i,1] = temp_t_filtered[i]
        final_temp[i,2] = temp_m_filtered[i]
        final_temp[i,3] = temp_f_filtered[i]

np.savetxt('P_test.csv', final_temp[:,0:3], delimiter=",")
np.savetxt('F_test.csv', final_temp[:,3], delimiter=",")

######################### normalization

final_temp = preprocessing.normalize(final_temp, axis=0, norm='max')

######################### plotting normalized data

plt.plot((temp_f), 'b-', linewidth=1)
plt.plot((final_temp[:,3], 'r-', linewidth=1)
plt.show()

plt.plot(final_data[:,0], 'r-', linewidth=1)
plt.plot(final_data[:,1], 'b-', linewidth=1)
plt.plot(final_data[:,2], 'g-', linewidth=1)
plt.plot((final_temp[:,3]-3650)/100, 'y-', linewidth=1)
plt.show()

