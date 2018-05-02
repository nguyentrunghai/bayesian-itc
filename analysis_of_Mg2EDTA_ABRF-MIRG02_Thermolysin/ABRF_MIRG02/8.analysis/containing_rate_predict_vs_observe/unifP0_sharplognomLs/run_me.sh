#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_containing_rate_of_cis.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc/ABRF_MIRG02/5.bitc_mcmc_unifP0_sharplognomLs/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc/ABRF_MIRG02/6.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPERIMENTS="1_MCS-ITC 3_VP-ITC  5_VP-ITC 6_VP-ITC 7_MCS-ITC 8_VP-ITC 9_VP-ITC 11_VP-ITC 12_VP-ITC 13_VP-ITC"

# DeltaG
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names "$EXPERIMENTS" --parameter "DeltaG" 


# DeltaH
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names "$EXPERIMENTS" --parameter "DeltaH"


