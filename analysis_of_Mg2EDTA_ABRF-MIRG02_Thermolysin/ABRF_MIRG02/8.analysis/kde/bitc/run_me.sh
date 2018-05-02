#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_kde_2d.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc/ABRF_MIRG02/5.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export EXPER="1_MCS-ITC 3_VP-ITC  5_VP-ITC 6_VP-ITC 7_MCS-ITC 8_VP-ITC 9_VP-ITC 11_VP-ITC 12_VP-ITC 13_VP-ITC"

python $SCRIPT --mcmc_dir $MCMC_DIR --ordered_experiment_names "$EXPER"
