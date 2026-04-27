# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:49:24 2026

@author: danielle.veigel
"""
import numpy as np
import matplotlib.pyplot as plt

def plot_Z(Z, f):
    neg_Z_Im = np.array([])
    theta = np.array([])
    for current_Z in Z:
        neg_Z_Im = np.append(neg_Z_Im, -1*current_Z.imag)
        theta = np.append(theta, np.arctan(current_Z.imag/current_Z.real)*180/np.pi)
    
    fig, axs = plt.subplot_mosaic([['Z', 'abs|Z|'], ['Z', 'theta']], figsize = (10,5), layout='constrained')
    axs['Z'].scatter(Z.real, neg_Z_Im, c=f, cmap = 'plasma', s = 10)
    axs['Z'].set_xlabel('ZRe')
    axs['Z'].set_ylabel('-ZIm')
    axs['Z'].set_aspect('equal')
    axs['Z'].set_title('Nyquist')

    axs['abs|Z|'].scatter(np.log10(f), np.log10(np.abs(Z)), c=f, cmap = 'plasma', s = 10)
    axs['abs|Z|'].set_ylabel('log(|Z|)\Ohm')
    axs['abs|Z|'].set_title('Magnitude Z and Theta')
    axs['theta'].scatter(np.log10(f), theta, c=f, cmap = 'plasma', s = 10)
    axs['theta'].set_ylabel('Theta')
    axs['theta'].set_xlabel('log(f)')

    plt.show()
    
    return fig

def plot_Z_comp(ref_Z, ref_f, Z_exp, f_exp):
    neg_Z_Im = np.array([])
    theta = np.array([])
    for current_Z in ref_Z:
        neg_Z_Im = np.append(neg_Z_Im, -1*current_Z.imag)
        theta = np.append(theta, np.arcsin(current_Z.imag/np.abs(current_Z))*180/np.pi)

    neg_Z2_Im = np.array([])
    theta2 = np.array([])
    for current_Z in Z_exp:
        neg_Z2_Im = np.append(neg_Z2_Im, -1*current_Z.imag)
        theta2 = np.append(theta2, np.arcsin(current_Z.imag/np.abs(current_Z))*180/np.pi)
    
    fig, axs = plt.subplot_mosaic([['Z', 'abs|Z|'], ['Z', 'theta']], figsize = (10,5), layout='constrained')
    axs['Z'].plot(ref_Z.real, neg_Z_Im, label='Simulated EIS')
    axs['Z'].scatter(Z_exp.real, neg_Z2_Im, label='Recovered from CP', c=f_exp, cmap = 'plasma', s = 10)
    axs['Z'].set_xlabel('ZRe')
    axs['Z'].set_ylabel('-ZIm')
    axs['Z'].set_aspect('equal')
    axs['Z'].set_title('Nyquist')
    fig.legend(loc='upper left')

    axs['abs|Z|'].plot(np.log10(ref_f), np.log10(np.abs(ref_Z)), label='Simulated EIS')
    axs['abs|Z|'].scatter(np.log10(f_exp), np.log10(np.abs(Z_exp)), label='Recovered from CP', c=f_exp, cmap = 'plasma', s = 10)
    axs['abs|Z|'].set_ylabel('log(|Z|)\Ohm')
    axs['abs|Z|'].set_title('Magnitude Z and Theta')
    axs['theta'].plot(np.log10(ref_f), theta, label='Simulated EIS')
    axs['theta'].scatter(np.log10(f_exp), theta2, label='Recovered from CP', c=f_exp, cmap = 'plasma', s = 10)
    axs['theta'].set_ylabel('Theta')
    axs['theta'].set_xlabel('log(f)')

    plt.show()
    return fig

def plot_DC(time,V,I, status):
    fig, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(time, V, label = status + "Voltage")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel(status+ " Voltage (V)")
    ax1.set_xscale('linear')
    ax1.set_title(status + ": CP or CA data")
    ax1.grid(True)
    
    # Optional: show current profile on second axis
    ax2 = ax1.twinx()
    ax2.plot(time, I, linestyle = "--",color='green', label=status + 'Current Profile')
    ax2.set_ylabel(status + " Current (A)")
    plt.legend()
    plt.show()
    
    return fig
    
def plot_DC_comp(exp_t, exp_V, exp_I, sim_t, sim_V, sim_I):
    
    fig = plt.figure(figsize=(8,6))
    plt.plot(exp_t, exp_V, 'k.', label='Voltage Data')
    plt.plot(sim_t, sim_V, 'r-', label='Fitted Data')
    plt.legend()
    plt.ylabel('Voltage')
    
    plt.figure(figsize=(8,6))
    plt.plot(exp_t, exp_I, 'k.', label='Data')
    plt.plot(sim_t, sim_I,
             'r-', linewidth=2, label='Fit')
    
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Current')
    plt.show()
    
    plt.tight_layout()
    plt.show()
    
    return fig    