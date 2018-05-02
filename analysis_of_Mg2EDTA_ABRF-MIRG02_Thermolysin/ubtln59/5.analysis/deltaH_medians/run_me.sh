#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_medians_of_deltaH_2.py"

export LNP0_LNLS_DIR="/home/tnguye46/bayesian_itc/ubtln59/2.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export UNIFP0_SHARPLNLS="/home/tnguye46/bayesian_itc/ubtln59/2.bitc_mcmc_unifP0_sharplognomLs/repeat_0"

export UNIFP0_LNLS="/home/tnguye46/bayesian_itc/ubtln59/2.bitc_mcmc_unifP0_lognomLs/repeat_0"


export NONLIN_RES="/home/tnguye46/bayesian_itc/ubtln59/3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPE="ubtln59a ubtln59a21082014 ubtln59altesProtein ubtln59b ubtln59b21082014 ubtln59c ubtln59c21082014 ubtln59d ubtln59neuesProtein"

python $SCRIPT --lognorP0_lognorLs_dir $LNP0_LNLS_DIR --unifP0_sharplognorLs_dir $UNIFP0_SHARPLNLS --unifP0_lognorLs_dir $UNIFP0_LNLS --nonlinear_fit_result_file $NONLIN_RES --experiment_names "$EXPE"

