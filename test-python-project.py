# %% Import packages

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd
import pathlib
# import tkinter as tk           # This would open a dialog to select a file but
# from tkinter import filedialog # it doesn't seem to work with the venv
# file_path = filedialog.askopenfilename()

# %% Import raw data
data_dir = r'/Users/briggssa/Repos/test-python-project/'
data_file = r'TestView_Data_1E-6_20221209.xlsx'
data_type = pathlib.Path(data_file).suffix
data_path = data_dir
data_path += data_file
if data_type == '.xlsx':
    data_name = data_file[0:-5]
    data = pd.read_excel(data_path)
elif data_type == '.csv':
    data_name = data_file[0:-4]
    data = pd.read_csv(data_path)
else:
    print('Invalid data type')
    stop()

## The following lines will plot the raw data
# plt.plot(data.Stroke, data.Load)
# plt.xlabel('Stroke (in)')
# plt.ylabel('Load (lbs)')
# plt.savefig('/Users/briggssa/Repos/test-python-project/true_data_raw.png')
# plt.show()

# %% Process raw data and plot processed data
sample_area = 0.025 # in^2
sample_gaugelength = 1.13 # in
Strain = (data.Stroke - data.Stroke[0]) / sample_gaugelength
Stress_psi = data.Load / sample_area
Stress_MPa = Stress_psi * 0.00689476
plt.plot(Strain, Stress_MPa)
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.title('Stress/Strain Plot for 316L in Molten FLiNaK at a Strain Rate of 1e-6 (in/in)/sec')
plot_file_type = '.png'
plot_out_path = data_dir # Will output plot in same directory with same name as input file
plot_out_path += data_name
plot_out_path += plot_file_type
plt.grid(True)
plt.savefig(plot_out_path)
plt.show()

# %%