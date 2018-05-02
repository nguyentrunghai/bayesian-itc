#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_containing_rate_of_cis.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc/ubtln59/2.bitc_mcmc_unifP0_sharplognomLs/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc/ubtln59/3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPERIMENTS="ubtln59a ubtln59a21082014 ubtln59altesProtein ubtln59b ubtln59b21082014 ubtln59c ubtln59c21082014 ubtln59d ubtln59neuesProtein"

# DeltaG
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names "$EXPERIMENTS" --parameter "DeltaG" 


# DeltaH
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names "$EXPERIMENTS" --parameter "DeltaH"


