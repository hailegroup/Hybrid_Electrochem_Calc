# Hybrid_Electrochem_Calc
This code takes a text file of DC (chronoamperometry to chronopotentiometry) data and calculates corresponding AC (EIS) data. It will plot this against the rest of your EIS data. 
For DC data, time should be in s, voltage in V, and current in mA. 

There are only four common packages required outside of Python-standard library. If you want to create a specific virtual environment and install dependencies anyways:
in bash:
pip install -r requirements.txt

For Linux users, you will need tkinter as well (pre-installed for Mac and Windows)
