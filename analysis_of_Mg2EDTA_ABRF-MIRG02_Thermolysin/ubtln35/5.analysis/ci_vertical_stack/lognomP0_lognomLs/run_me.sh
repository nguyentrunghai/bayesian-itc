#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_bci_vs_gci.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc/ubtln35/2.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc/ubtln35/3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPE1="18052014ubtln35test1 18052014ubtln35test2 19052014ubtln35test1 19052014ubtln35test2 ubtln35test1 ubtln35test2 ubtln35k ubtln35L ubtln35m ubtln35o"


# DeltaG
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1" --parameter "DeltaG" --xlimits "-10.5 -8" 


# DeltaH
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1"  --parameter "DeltaH" --xlimits "-8 -3"

# P0
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1"  --parameter "P0" --xlimits "0.01 0.03" 

