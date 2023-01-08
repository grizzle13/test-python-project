# %% Import packages

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd
# import tkinter as tk           # This would open a dialog to select a file but
# from tkinter import filedialog # it doesn't seem to work with the venv
# file_path = filedialog.askopenfilename()

# %% Import and plot raw data
data = pd.read_excel('/Users/briggssa/Repos/test-python-project/TestView_Data_1E-6_20221209.xlsx')
# print(data)
plt.plot(data.Stroke, data.Load)
plt.xlabel('Stroke (in)')
plt.ylabel('Load (lbs)')
plt.savefig('/Users/briggssa/Repos/test-python-project/true_data_raw.png')
plt.show()
# data1 = np.loadtxt("/Users/briggssa/Repos/test-python-project/test-data.csv", delimiter=",", dtype=int, skiprows=1)
# print(data1)

# %% Process raw data and plot processed data
sample_area = 0.05 # in^2
sample_gaugelength = 1.13 # in
Strain = (data.Stroke - data.Stroke[0]) / sample_gaugelength
Stress_psi = data.Load / sample_area
Stress_MPa = Stress_psi * 0.00689476
plt.plot(Strain, Stress_MPa)
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.title('Stress/Strain Plot for 316L in Molten FLiNaK at a Strain Rate of 1e-6 (in/in)/sec')
plt.savefig('/Users/briggssa/Repos/test-python-project/true_data_final.png')
plt.show()