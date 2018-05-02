#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_submit_bitc_mcmc_jobs.py"

export ITC_DIR="/home/tnguye46/bayesian_itc/Mg2EDTA/1.itc_origin_heat_files"

export HEAT_DIR="/home/tnguye46/bayesian_itc/Mg2EDTA/1.itc_origin_heat_files"

export HEAT_FILE_SUF=".DAT"

export DC=0.1

export DS=0.1

python $SCRIPT --itc_data_dir $ITC_DIR --heat_data_dir $HEAT_DIR --heat_file_suffix $HEAT_FILE_SUF --dc $DC --ds $DS

