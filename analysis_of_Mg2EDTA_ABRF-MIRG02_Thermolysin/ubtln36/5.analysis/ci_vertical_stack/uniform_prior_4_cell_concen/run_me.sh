#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_bci_vs_gci.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc_reproduce/ubtln36/2.bitc_mcmc_uniform_prior_4_cell_concen/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc_reproduce/ubtln36/3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPE1="19052014ubtln36test2 ubtln36a ubtln36a14082014 ubtln36b ubtln36b18082014 ubtln36c14082014 ubtln36d ubtln36e ubtln36f ubtln36g ubtln36h"

# DeltaG
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1" --parameter "DeltaG" --xlimits "-10 -8" 


# DeltaH
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1"  --parameter "DeltaH" --xlimits "-6 -2"

# P0
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1"  --parameter "P0" --xlimits "0.015 0.035"

