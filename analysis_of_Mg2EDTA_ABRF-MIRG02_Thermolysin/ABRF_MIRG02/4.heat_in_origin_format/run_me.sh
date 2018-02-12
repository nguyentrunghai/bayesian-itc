#!/bin/bash

export SCRIPT="../../scripts/run_write_heat_in_origin_format.py"

export EXP_DES_PAR_FILE="../1.experimental_desgin_parameters/abrf_mirg02_experimental_desgin_parameters.dat"

export DIG_HEAT_DIR="../2.digitized_heat"

python $SCRIPT --experimental_desgin_parameters_file $EXP_DES_PAR_FILE --digitized_heat_dir $DIG_HEAT_DIR

