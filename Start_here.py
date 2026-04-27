# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:09:55 2026

@author: danielle.veigel
"""
import Load_CP_Data as LD
import numpy as np
from tkinter import ttk, filedialog, Tk
import matplotlib.pyplot as plt
import Plotting_Functions as PF
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
import Smooth_and_Interpolate as SI
import Exp_CP_data_fitting as FIT
import Convert_CP_to_EIS as DC_EIS
import export_dict_to_excel as Export
from pathlib import Path

Tk().withdraw()
directory = Path(__file__).resolve().parent
DC_Prompt = "Select file for DC data (no headers; time(s) V(V) I(mA))"

DC_data, DC_file_path = LD.load_txt_data(DC_Prompt, directory)

# Set what frequencies you want to recover from CA
f_max = .1

#if you want to use the smoothing method, set what you want your steps to be
window = 51 #Savitzky-Golay filter window length (must be odd)

#Do you want to try smoothing or fitting your data? "Smooth" or "Fit"
data_treatment = "Fit"

#establish figure list
figures = [0,0,0,0,0,0]
DC_data[:, 2] = DC_data[:, 2]/1000
print("loaded data:")
figures[2]=PF.plot_DC(DC_data[:, 0], DC_data[:, 1], DC_data[:, 2], "Raw")
print(len(DC_data[:,0]))

if data_treatment == "Smooth":
    #if the derivative data is not very smooth, make the last input (dt) larger or increase window size in Smooth and Interpolate function
    dt = 0.01
    time, Volt, Current = SI.smooth_and_interpolate(DC_data[:, 0], DC_data[:, 1], DC_data[:, 2], dt, window) 
elif data_treatment == "Fit":
    dt = 0.01
    time, Volt, Current= FIT.fit(DC_data[:, 0], DC_data[:, 1], DC_data[:, 2], "CA", dt)
    
print("Treated DC data:")
figures[3]=PF.plot_DC_comp(DC_data[:,0], DC_data[:,1], DC_data[:,2], time, Volt, Current)

dif_time, dif_V, dif_I, FT_f, FT_V, FT_I, filtered_f, recovered_Z, Z_full, figures[4], figures[5], figures[0], figures[1], EIS_filepath = DC_EIS.FFT_EIS(time, Volt, Current, data_treatment, dt, window, f_max, directory)
FT_Z = FT_V/FT_I

#Build Summary Dictionary
summary_dict = {
    "Selected freq range": filtered_f,
    "Recovered ZRe": recovered_Z.real,
    "Recovered ZIm": recovered_Z.imag,
    "Recovered Zabs": np.abs(recovered_Z),
    "Recovered Phase": np.arctan(recovered_Z.imag/recovered_Z.real)*180/np.pi,
    "Data Treatment": data_treatment,
    "Max freq": f_max,
    "Interpolation time step (s)": dt,
    "SavGol window length": window,
    "DC data filepath": DC_file_path,
    "exp EIS filepath": EIS_filepath
}

#Build Dictionary to Record all processing info
raw_dict = {
    "Imported time(s), V(V), I(A)": DC_data,
    "Treated Data time": time,
    "Treated Data Voltage": Volt,
    "Treated Data Current": Current,
    "Differentiated time": dif_time,
    "dV/dt": dif_V,
    "dI/dt": dif_I,
    "FFT frequencies": FT_f,
    "FFT Voltage real": FT_V.real,
    "FFT Voltage imag": FT_V.imag,
    "FFT Current real": FT_I.real,
    "FFT Current imag": FT_I.imag,
    "All recovered ZRe": FT_Z.real,
    "All recovered ZImag": FT_Z.imag
}

Export.export_to_excel(summary_dict, raw_dict, figures, directory)