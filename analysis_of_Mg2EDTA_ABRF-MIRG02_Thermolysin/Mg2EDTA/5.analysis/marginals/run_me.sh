#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_marginals.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc/Mg2EDTA/2.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export ITC_DIR="/home/tnguye46/bayesian_itc/Mg2EDTA/1.itc_origin_heat_files"

export EXPERIMENT="Mg1EDTAp1a"

python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --itc_files_dir $ITC_DIR --experiment $EXPERIMENT

