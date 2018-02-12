#!/bin/bash

export SCRIPT="../../../scripts/run_plot_bci_vs_gci.py"

export MCMC_DIR="../../2.bitc_mcmc/repeat_0"

export NONLIN_RES="../../3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPE1="Mg1EDTAp1a Mg1EDTAp1b Mg1EDTAp1c Mg1EDTAp1d Mg1EDTAp1e"

export EXPE2="Mgp5EDTAp05a Mgp5EDTAp05b Mgp5EDTAp05c Mgp5EDTAp05e Mgp5EDTAp05f Mgp5EDTAp05g Mgp5EDTAp05h Mgp5EDTAp05i Mgp5EDTAp05j"

# DeltaG
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1" --ordered_experiment_names_2 "$EXPE2" --parameter "DeltaG" --xlimits "-10 -8" 


# DeltaH
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1" --ordered_experiment_names_2 "$EXPE2"  --parameter "DeltaH" --xlimits "-3.5 -1.5"

# P0
python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --nonlinear_fit_result_file $NONLIN_RES --ordered_experiment_names_1 "$EXPE1" --ordered_experiment_names_2 "$EXPE2"  --parameter "P0" --xlimits "0.02 0.12"

