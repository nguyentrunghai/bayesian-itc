#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_medians_of_deltaH_2.py"

export LNP0_LNLS_DIR="/home/tnguye46/bayesian_itc/ubtln36/2.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export UNIFP0_SHARPLNLS="/home/tnguye46/bayesian_itc/ubtln36/2.bitc_mcmc_unifP0_sharplognomLs/repeat_0"

export UNIFP0_LNLS="/home/tnguye46/bayesian_itc/ubtln36/2.bitc_mcmc_unifP0_lognomLs/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc/ubtln36/3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"


export EXPE="19052014ubtln36test2 ubtln36a ubtln36a14082014 ubtln36b ubtln36b18082014 ubtln36c14082014 ubtln36d ubtln36e ubtln36f ubtln36g ubtln36h"

python $SCRIPT --lognorP0_lognorLs_dir $LNP0_LNLS_DIR --unifP0_sharplognorLs_dir $UNIFP0_SHARPLNLS --unifP0_lognorLs_dir $UNIFP0_LNLS --nonlinear_fit_result_file $NONLIN_RES --experiment_names "$EXPE"

