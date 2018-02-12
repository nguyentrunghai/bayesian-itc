
"""
write the top part for itc files

$ITC
$ 23                    # ExperimentMicroCal.number_of_injections 
$NOT
$ 25                    # ExperimentMicroCal.target_temperature ( C )
$ 60                    # ExperimentMicroCal.equilibration_time  (second)
$ 298                   # ExperimentMicroCal.stir_rate     ( ureg.revolutions_per_minute )
$ 5                     # ExperimentMicroCal.reference_power   ( ureg.microcalorie / ureg.second )
$ 2                     # ignored by ExperimentMicroCal
$ADCGainCode:  3        # ignored by ExperimentMicroCal 
$False,True,True        # ignored by ExperimentMicroCal
$ 12 , 24 , 276 , 2     # (injection_volume (microliter), injection_duration (second), spacing (second), filter_period (second) ) 
$ 12 , 24 , 276 , 2     # ... the same 
.
.
.
$ 12 , 24 , 276 , 2 
$ 12 , 24 , 276 , 2 
# 0                     # ignored by ExperimentMicroCal
# 1                     # ExperimentMicroCal.syringe_concentration['ligand']    (ureg.millimole / ureg.liter)
# 0.1                   # ExperimentMicroCal.cell_concentration['macromolecule']    (ureg.millimole / ureg.liter)
# 1.434                 # ExperimentMicroCal.cell_volume  (ureg.milliliter) 
# 25                    # ignored
# 28.8278               # ignored
# 16.14727              # ignored
?

"""

import argparse
import os

import numpy as np

from _data_files import read_experimental_design_parameters, write_dummy_itc_file


def _number_of_lines(csv_file):
    nlines = np.loadtxt(csv_file, delimiter=",").shape[0]
    return nlines



parser = argparse.ArgumentParser()

parser.add_argument( "--experimental_desgin_parameters_file",  type=str, default="experimental_desgin_parameters.dat")
parser.add_argument( "--digitized_heat_dir",  type=str, default="digitized_heat")

args = parser.parse_args()


parameters = read_experimental_design_parameters(args.experimental_desgin_parameters_file)
exper_names = parameters.keys()

for exper_name in exper_names:
    digitized_heat_file = os.path.join(args.digitized_heat_dir, exper_name+".csv")
    number_of_injections = _number_of_lines(digitized_heat_file)

    itc_file_name = exper_name + ".itc"
    write_dummy_itc_file( parameters[exper_name], itc_file_name, number_of_injections=number_of_injections)

print "DONE"

