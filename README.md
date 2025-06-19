# Mapping Dust Grain Temperature in a Molecular Cloud

This repository contains Python scripts used for mapping **dust grain temperatures** in a molecular cloud, using infrared data from the **DIRBE data cube** (`cube_dirbe.fits`).

The method is based on:

 Analyzing infrared fluxes at different wavelengths  
 Computing flux ratios (e.g., 240 µm / 100 µm)  
 Inverting Planck function to estimate temperature pixel-wise  
 Generating maps of fluxes and derived dust temperature

---

## Files

| File          | Description                              |
|---------------|------------------------------------------|
| `ex1.py`      | Planck function plots vs temperature      |
| `ex3.py`      | Flux ratio scatter plots                  |
| `ex3_1.py`    | Flux ratio image map                      |
| `ex5.py`      | Temperature inversion from flux ratios    |
| `ex6.py`      | Multi-panel plot of DIRBE flux maps       |
| `cube_dirbe.fits` | DIRBE infrared data cube              |

---

## How to run

You need:

- Python 3.x
- numpy
- scipy
- matplotlib
- astropy

Install dependencies:

```bash
pip install numpy scipy matplotlib astropy
