# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:45:56 2026

@author: danielle.veigel
"""
import Load_CP_Data as LD
import numpy as np
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
import Plotting_Functions as PF
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
import Smooth_and_Interpolate as SI
import Exp_CP_data_fitting as Exp_fit
import math

def FFT_EIS(time, Volt, Current, method, dt, window, max_f, directory, padding_factor=50, n_log_points = 100):

    ### Differentiate Currenet and Voltage Data ###
    dif_V = np.gradient(Volt, time)
    dif_I = np.gradient(Current, time)
    
    if method == "Smooth":
        time, dif_V, dif_I = SI.smooth_and_interpolate(time, dif_V, dif_I, dt, window)
    
    print("Differentiated Data:")
    dif_plot = PF.plot_DC(time, dif_V, dif_I, "d "+method+"/dt")
        
    #### Fourier Transforms ####
    # Add zeros to end of data to allow for more frequency points (spectral interpolation)
    N_0 = len(dif_I)
    N_fft = N_0*padding_factor
    print(f"FFT: original N={N_0}, zero-padded N={N_fft} (factor={padding_factor})")

    FT_V = np.fft.fft(dif_V, n=N_fft)
    FT_I = np.fft.fft(dif_I, n=N_fft)
    FT_f = np.fft.fftfreq(N_fft, dt)
    
    fig, ax1 = plt.subplots(figsize=(8,5))
    ax1.scatter(FT_f, np.abs(FT_V), label='Fourier Transform of dV/dt', c=np.angle(FT_V, deg=True), cmap = 'Blues', s = 10 )
    ax1.set_xscale('log')
    ax1.set_title('Fourier Transforms')
    ax1.set_ylabel('FFT(dV/dt)')
    ax2 = ax1.twinx()
    ax2.scatter(FT_f, np.abs(FT_I), label='Fourier Transform of dI/dt', c=np.angle(FT_I, deg=True), cmap = 'Greens', s = 10)
    ax2.set_ylabel('FFT(dI/dt)')
    fig.legend()
    plt.show()
    
    #### Calculate Impedance ####
    # Positive frequencies only (one-sided spectrum)
    pos_mask = (FT_f > 0) & (FT_f <= max_f)
    pos_f = FT_f[pos_mask]
    pos_FT_V = FT_V[pos_mask]
    pos_FT_I = FT_I[pos_mask]

    # Select log-spaced frequency points from the FFT grid
    # (FFT gives linear spacing; log-spacing matches EIS convention)
    n_points = n_log_points  # number of log-spaced points to extract
    f_min_avail = pos_f.min()
    f_max_avail = pos_f.max()
    log_f_targets = np.logspace(np.log10(f_min_avail), np.log10(f_max_avail), n_points)

    recovered_Z = np.array([])
    filtered_f = np.array([])
    seen_idx = set()

    for f_target in log_f_targets:
        idx = np.argmin(np.abs(pos_f - f_target))
        if idx not in seen_idx:          # avoid duplicate frequency points
            seen_idx.add(idx)
            filtered_f  = np.append(filtered_f,  pos_f[idx])
            recovered_Z = np.append(recovered_Z, pos_FT_V[idx] / pos_FT_I[idx])

    print(f"Recovered {len(filtered_f)} log-spaced impedance points "
          f"from {f_min_avail:.4f} Hz to {f_max_avail:.4f} Hz")
        
    Z_DC_plot = PF.plot_Z(recovered_Z, filtered_f)
    
    EIS_full_prompt = "Select full Impedance data file"
    EIS_data_full, measured_EIS_filepath = LD.load_txt_data(EIS_full_prompt, directory)
    Z_full = np.array([EIS_data_full[:, 1]+1j*EIS_data_full[:, 2]])
    Z_full = Z_full.T
    
    
    Z_comp_plot = PF.plot_Z_comp(Z_full, EIS_data_full[:, 0], recovered_Z, filtered_f)
    
    return(time, dif_V, dif_I, FT_f, FT_V, FT_I, filtered_f, recovered_Z, Z_full.T, dif_plot, fig, Z_DC_plot, Z_comp_plot, measured_EIS_filepath)

    