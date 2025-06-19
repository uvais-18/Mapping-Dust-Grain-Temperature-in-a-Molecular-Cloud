# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 10:57:50 2025

@author: aayan
"""

# Mapping Dust Grain Temperature in a Molecular Cloud


import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cst
from astropy.io import fits
from scipy import optimize

# ----------- Load FITS data ----------
hdul = fits.open("cube_dirbe.fits")
data = hdul[0].data
header = hdul[0].header

# Bands
data_1_25 = data[0]
data_100 = data[7]
data_140 = data[8]
data_240 = data[9]

# ----------- Plot Planck function  ----------

def planck_func(x, T):
    h = cst.Planck
    c = cst.c
    k = cst.Boltzmann
    return 2*h*c**2 / x**5 * (1 / (np.exp(h*c / (x*k*T)) - 1))

T_array = np.array([5, 20, 100, 500])
wavelengths = np.array([1.25, 2.2, 3.5, 4.9, 12, 25, 60, 100, 140, 240]) * 1e-6

plt.figure()
for T in T_array:
    B = planck_func(wavelengths, T)
    plt.plot(np.log10(wavelengths), np.log10(B), label=f"{T} K")

plt.xlabel('log10(Wavelength) [m]', fontsize=14)
plt.ylabel('log10(B_lambda)', fontsize=14)
plt.legend()
plt.title('Planck Function vs Wavelength')
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------- Flux ratio scatter plots  ----------

plt.figure()
plt.scatter(data_100.flatten(), data_240.flatten(), label='100 vs 240 µm', s=1)
plt.xlabel('100 µm Flux')
plt.ylabel('240 µm Flux')
plt.legend()
plt.title('Scatter: 100 µm vs 240 µm')
plt.tight_layout()
plt.show()

plt.figure()
plt.scatter(data_140.flatten(), data_240.flatten(), label='140 vs 240 µm', s=1)
plt.xlabel('140 µm Flux')
plt.ylabel('240 µm Flux')
plt.legend()
plt.title('Scatter: 140 µm vs 240 µm')
plt.tight_layout()
plt.show()

# ----------- Flux ratio image  ----------

ndata = data_240 / data_100
plt.figure()
plt.imshow(ndata, origin='lower', cmap='inferno')
plt.colorbar(label='240 µm / 100 µm Flux Ratio')
plt.title('Flux Ratio Map: 240 µm / 100 µm')
plt.tight_layout()
plt.show()

# ----------- Invert temperature from ratio  ----------

# Build theoretical ratio from Planck function
T_fit = np.linspace(14, 19, 100)
flux_240 = planck_func(240e-6, T_fit)
flux_100 = planck_func(100e-6, T_fit)
ratio_theoretical = flux_240 / flux_100

# Fit exponential
def model(x, a, b, c):
    return b * np.exp(-a * x) + c

def inverse_model(ratio, a, b, c):
    return -1/a * np.log((ratio - c) / b)

params, _ = optimize.curve_fit(model, T_fit, ratio_theoretical)
a_fit, b_fit, c_fit = params

# Compute temperature map
ratio_obs = data_240 / data_100
temp_map = inverse_model(ratio_obs, a_fit, b_fit, c_fit)

# Plot temperature map
plt.figure()
plt.imshow(temp_map, origin='lower', cmap='plasma')
plt.colorbar(label='Dust Temperature [K]')
plt.title('Dust Temperature Map (from 240/100 ratio)')
plt.tight_layout()
plt.show()

# ----------- Multi-panel map  ----------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

im1 = axs[0, 0].imshow(data_1_25, origin='lower', cmap='viridis')
axs[0, 0].set_title("1.25 µm Flux")
plt.colorbar(im1, ax=axs[0, 0])

im2 = axs[0, 1].imshow(data_100, origin='lower', cmap='viridis')
axs[0, 1].set_title("100 µm Flux")
plt.colorbar(im2, ax=axs[0, 1])

im3 = axs[1, 0].imshow(data_140, origin='lower', cmap='viridis')
axs[1, 0].set_title("140 µm Flux")
plt.colorbar(im3, ax=axs[1, 0])

im4 = axs[1, 1].imshow(data_240, origin='lower', cmap='viridis')
axs[1, 1].set_title("240 µm Flux")
plt.colorbar(im4, ax=axs[1, 1])

plt.tight_layout()
plt.show()
