#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_submit_bitc_mcmc_jobs.py"

export ITC_DIR="/home/tnguye46/bayesian_itc/ABRF_MIRG02/3.dummy_itc_files"

export HEAT_DIR="/home/tnguye46/bayesian_itc/ABRF_MIRG02/4.heat_in_origin_format"

export HEAT_FILE_SUF=".DAT"

export DS=0.001

export UNIFP0=" --uniform_cell_concentration "

export CONC_RANGE_FAC=10

export DUM_ITC=" --dummy_itc_file "

python $SCRIPT --itc_data_dir $ITC_DIR --heat_data_dir $HEAT_DIR --heat_file_suffix $HEAT_FILE_SUF --ds $DS $DUM_ITC $UNIFP0 --concentration_range_factor $CONC_RANGE_FAC

