#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_bci_vs_gci.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc_reproduce/ABRF_MIRG02/5.bitc_mcmc/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc_reproduce/ABRF_MIRG02/6.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPE="1_MCS-ITC 3_VP-ITC  5_VP-ITC 6_VP-ITC 7_MCS-ITC 8_VP-ITC 9_VP-ITC 11_VP-ITC 12_VP-ITC 13_VP-ITC"

# DeltaG
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE" --parameter "DeltaG" --xlimits "-9.0 -7.0"


# DeltaH
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE" --parameter "DeltaH" --xlimits "-14.0 -2.0"

# P0
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE" --parameter "P0" --xlimits "0.0 0.06"

