#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_convert_ka_to_dg.py"

export ORIGIN_PAR_FILE="table3_ka_dh_in_kcal_per_mole.dat"

export ITC_DIR="/home/tnguye46/bayesian_itc/ABRF_MIRG02/3.dummy_itc_files"

export ENERGY_UNIT="kcal_per_mole"

export OUT="origin_dg_dh_in_kcal_per_mole.dat"

python $SCRIPT --origin_par_file $ORIGIN_PAR_FILE --itc_file_dir $ITC_DIR --input_energy_unit $ENERGY_UNIT --write_header --out $OUT

