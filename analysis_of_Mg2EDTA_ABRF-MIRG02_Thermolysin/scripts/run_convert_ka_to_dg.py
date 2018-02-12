
import os
import glob
import argparse

import numpy as np

from _data_files import cell_concentration

KB = 0.0019872041   # kcal/mol/K
TEMPERATURE = 298.15

def _dG(K):
    """
    K is binding constant
    """
    return -KB * TEMPERATURE * np.log(K)

def _std_of_dG(K, std_of_K):
    """
    """
    return KB * TEMPERATURE * std_of_K / np.abs(K)

def _dS(dG, dH):
    return (dH - dG) / TEMPERATURE

def _std_of_dS(std_of_dH, std_of_dG):
    """
    """
    return np.sqrt(std_of_dH**2 + std_of_dG**2) / TEMPERATURE


parser = argparse.ArgumentParser()

parser.add_argument( "--origin_par_file",       type=str, default="origin_ka_dh.dat")

parser.add_argument( "--itc_file_dir",          type=str, default="itc_files")
parser.add_argument( "--input_energy_unit",     type=str, default="kcal_per_mole")

parser.add_argument( "--write_header",          action="store_true", default=False)

parser.add_argument( "--out",                   type=str, default="origin_dg_dh_in_kcal_per_mole.dat")

args = parser.parse_args()

assert args.input_energy_unit in ["kcal_per_mole", "cal_per_mole", "joule_per_mole"], "unknown energy unit: "+args.input_energy_unit

if args.input_energy_unit == "kcal_per_mole":
    unit_conv_factor = 1.
elif  args.input_energy_unit == "cal_per_mole":
    unit_conv_factor = 1./1000.
elif  args.input_energy_unit == "joule_per_mole":
    unit_conv_factor = 0.239006/1000.

itc_files = glob.glob( os.path.join( args.itc_file_dir, "*.itc" ) )
exper_names = [os.path.basename(f)[:-4] for f in itc_files]

input_lines = open(args.origin_par_file, "r").readlines()
input_lines = [ line for line in input_lines if not line.startswith("#") ]

out_header = " "*30 + " %15s %15s %15s %15s %15s %15s %15s %15s %15s %15s\n"%("N", "N_std",
                        "DeltaG", "DeltaG_std", "DeltaH", "DeltaH_std", "DeltaS", "DeltaS_std", "P0", "P0_std" )

if args.write_header:
    out_string = out_header
else:
    out_string = ""


for line in input_lines:

    entries = line.split()
    exper_name     = entries[0]

    if exper_name in exper_names:
        
        N      = float( entries[1] )
        N_std  = float( entries[2] )
        K      = float( entries[3] )
        K_std  = float( entries[4] )
        dH     = float( entries[5] ) * unit_conv_factor
        dH_std = float( entries[6] ) * unit_conv_factor

        dG     = _dG(K)
        dG_std = _std_of_dG(K, K_std)

        dS     = _dS(dG, dH)
        dS_std = _std_of_dS(dH_std, dG_std)

        itc_file = os.path.join(args.itc_file_dir, exper_name+".itc")
        Mt  = cell_concentration( itc_file, is_dummy_itc_file=True )
        P0 = Mt * N
        P0_std = Mt * N_std

        out_string += "%-30s %15.10f %15.10f %15.10f %15.10f %15.10f %15.10f %15.10f %15.10f %15.10f %15.10f\n" %(exper_name, N, N_std, 
                                            dG, dG_std, dH, dH_std, dS, dS_std, P0, P0_std)

open(args.out, "w").write(out_string)

