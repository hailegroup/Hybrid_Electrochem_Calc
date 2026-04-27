# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:31:50 2026

@author: danielle.veigel
"""
import numpy as np
from tkinter import ttk, filedialog, Tk

def load_txt_data(Prompt, directory):
    print("Select your file (window may be behind interpreter)")
    root=Tk()
    root.withdraw()
    input_folder = directory / "input data"
    root.attributes ('-topmost', True)
    file_path = filedialog.askopenfilename(
        title=Prompt,
        filetypes=[("Text files", "*.txt *.dat *.csv"), ("All files", "*.*")], initialdir=input_folder
    )

    if not file_path:
        return

    try:
        data = np.loadtxt(file_path)
    except ValueError:
        data = np.loadtxt(file_path, delimiter=",")
        
    print(f"There are {data.shape[0]} rows and {data.shape[1]} columns in this file.")

    return data, file_path
