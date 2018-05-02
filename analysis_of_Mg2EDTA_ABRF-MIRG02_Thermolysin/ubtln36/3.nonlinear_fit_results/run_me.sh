#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_convert_ka_to_dg.py"

export ITC_DIR="/home/tnguye46/bayesian_itc/ubtln36/1.itc_origin_heat_files"

python $SCRIPT --origin_par_file origin_ka_dh_cal_per_mole.txt --itc_file_dir $ITC_DIR --input_energy_unit "cal_per_mole" --write_header --out tmp_1.dat


python $SCRIPT --origin_par_file origin_ka_dh_joule_per_mole.txt --itc_file_dir $ITC_DIR --input_energy_unit "joule_per_mole" --out tmp_2.dat

cat tmp_1.dat tmp_2.dat > origin_dg_dh_in_kcal_per_mole.dat
rm tmp_1.dat tmp_2.dat
