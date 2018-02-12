
import argparse
import os

import numpy as np

from _data_files import read_experimental_design_parameters, write_heat_in_origin_format


def _kcal_per_mol_of_injectant_2_micro_cal(injection_heat, injection_volume, syringe_concentration):
    """
    injection_heat : float, in units of kcal/mol of injectant
    injection_volume : float, in units of micro L
    syringe_concentration : in units of mili M
    """
    vol_in_liter = injection_volume * 10.**(-6)
    concen_in_M  = syringe_concentration * 10.**(-3)
    number_of_mol = concen_in_M * vol_in_liter
    
    heat_in_kcal_per_mol = injection_heat * number_of_mol
    heat_in_micro_cal    = heat_in_kcal_per_mol * 10.**(9)

    return heat_in_micro_cal


def _read_digitized_heat(csv_file):
    heats = np.loadtxt(csv_file, delimiter=",")[:,-1]
    return heats



parser = argparse.ArgumentParser()

parser.add_argument( "--experimental_desgin_parameters_file",  type=str, default="experimental_desgin_parameters.dat")
parser.add_argument( "--digitized_heat_dir",  type=str, default="digitized_heat")

args = parser.parse_args()


parameters = read_experimental_design_parameters(args.experimental_desgin_parameters_file)
exper_names = parameters.keys()

for exper_name in exper_names:
    digitized_heat_file = os.path.join(args.digitized_heat_dir, exper_name+".csv")
    heats = _read_digitized_heat(digitized_heat_file)

    injection_volume = parameters[exper_name]["injection_volume"]
    syringe_concentration = parameters[exper_name]["syringe_concentration"]

    heats_in_micro_cal = [ _kcal_per_mol_of_injectant_2_micro_cal(heat, injection_volume, syringe_concentration) for heat in heats ]

    write_heat_in_origin_format(heats_in_micro_cal, injection_volume, exper_name+".DAT")

print "DONE"


