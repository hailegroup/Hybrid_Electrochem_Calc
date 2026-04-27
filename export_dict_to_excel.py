# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:28:07 2026

@author: danielle.veigel (Generated Using Microsoft CoPilot)
"""

import pandas as pd
import numpy as np
from tkinter import Tk, filedialog

def export_to_excel(summary_dict, raw_dict, figures, directory):
    """
    Exports:
    - Sheet 1: Figures (6 figures arranged 2x3)
    - Sheet 2: Summary (dictionary)
    - Sheet 3: Raw Data (dictionary)

    Each dictionary key becomes a header.
    Each value is written starting at the next empty column.
    If a value has more columns than rows, it is transposed.
    """
    print("Save your files (window may be behind interpreter)")
    # Hide the Tkinter root window
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    Output_folder = directory / "output data"
    # Ask user for save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Excel File As", initialdir=Output_folder
    )

    if not file_path:
        print("Export cancelled.")
        return

    # Create Excel writer
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        
        workbook = writer.book

        # ---------------------------------------------------------
        # 1. FIGURES SHEET
        # ---------------------------------------------------------
        worksheet_fig = workbook.add_worksheet("Figures")
        writer.sheets["Figures"] = worksheet_fig
        
        if figures:
            row_height = 30   # vertical spacing
            col_width = 16     # horizontal spacing
        
            for i, fig in enumerate(figures):
                img_path = f"figure_{i+1}.png"
                fig.savefig(img_path, dpi=150, bbox_inches="tight")
        
                row = (i //2) * row_height
                col = (i % 2) * col_width
        
                worksheet_fig.insert_image(row, col, img_path)

        # --- Helper function to write a dictionary to a sheet ---
        def write_dict_to_sheet(data_dict, sheet_name):
            col_pointer = 0  # track next empty column

            for key, value in data_dict.items():

                # Convert value to DataFrame safely
                if isinstance(value, (int, float, complex, str)):
                    # Wrap scalars or strings into a 1-row DataFrame
                    df = pd.DataFrame([value])
                
                elif isinstance(value, dict):
                    # Convert dict to a single-row DataFrame
                    df = pd.DataFrame([value])
                
                else:
                    # Assume it's array-like (list, np.array, DataFrame, Series)
                    df = pd.DataFrame(value)


                # Transpose if more columns than rows
                if df.shape[1] > df.shape[0]:
                    df = df.T
                
                # Set column headers to the dictionary key
                df.columns = [key] * df.shape[1]

                # Write header
                df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    startrow=0,
                    startcol=col_pointer,
                    header=True,
                    index=False
                )
                
                # After writing df.to_excel(...)
                worksheet = writer.sheets[sheet_name]
                
                for j, col_name in enumerate(df.columns):
                    # Get the Excel column index
                    col_idx = col_pointer + j
                
                    # Compute max width: header vs. data
                    max_len = max(
                        len(str(col_name)),
                        *(len(str(x)) for x in df[col_name].values)
                    )
                
                    # Add a little padding
                    worksheet.set_column(col_idx, col_idx, max_len)


                # Move pointer to next empty column
                col_pointer += df.shape[1]

        # Write both dictionaries
        write_dict_to_sheet(summary_dict, "Summary")
        write_dict_to_sheet(raw_dict, "Raw Data")

    print(f"Excel file saved to: {file_path}")
