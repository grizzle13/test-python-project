# %% Import packages

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd

# %% Hello world!!


def hello_world():
    """Prints "Hello world!"
    Also, this is how you comment functions.
    """
    print("Hello world!")


hello_world()
# %% Import and plot raw data
data = pd.read_excel(
    "/Users/briggssa/Repos/test-python-project/TestView_Data_1E-6_20221209.xlsx"
)
# print(data)
plt.plot(data.Stroke, data.Load)
plt.xlabel("Stroke (in)")
plt.ylabel("Load (lbs)")
plt.savefig("/Users/briggssa/Repos/test-python-project/true_data_raw.png")
plt.show()
# data1 = np.loadtxt("/Users/briggssa/Repos/test-python-project/test-data.csv", delimiter=",", dtype=int, skiprows=1)
# print(data1)

# %% Process raw data and plot processed data
sample_area = 0.05  # in^2
sample_gaugelength = 1.13  # in
Strain = (data.Stroke - data.Stroke[0]) / sample_gaugelength
Stress_psi = data.Load / sample_area
Stress_MPa = Stress_psi * 0.00689476
plt.plot(Strain, Stress_MPa)
plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")
plt.title(
    "Stress/Strain Plot for 316L in Molten FLiNaK at a Strain Rate of 1e-6 (in/in)/sec"
)
plt.savefig("/Users/briggssa/Repos/test-python-project/true_data_final.png")
plt.show()
# %% Matplotlib Testing
test_data = pd.read_csv("/Users/briggssa/Repos/test-python-project/test-data.csv")
print(test_data)

plt.plot(test_data.x, test_data.y)
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("/Users/briggssa/Repos/test-python-project/test_data.png")
plt.show()

# fig, ax = plt.subplots()
# ax.plot([1, 2, 3, 4], [1, 4, 2, 3]);
# data3=data2.x**2
# print(data3)
# Install Python Flask
