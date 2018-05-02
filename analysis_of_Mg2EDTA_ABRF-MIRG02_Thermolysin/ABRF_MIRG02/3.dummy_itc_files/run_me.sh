#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_write_dummy_itc_files.py"

export EXP_DES_PAR_FILE="/home/tnguye46/bayesian_itc/ABRF_MIRG02/1.experimental_desgin_parameters/abrf_mirg02_experimental_desgin_parameters.dat"

export DIG_HEAT_DIR="/home/tnguye46/bayesian_itc/ABRF_MIRG02/2.digitized_heat"

python $SCRIPT --experimental_desgin_parameters_file $EXP_DES_PAR_FILE --digitized_heat_dir $DIG_HEAT_DIR

