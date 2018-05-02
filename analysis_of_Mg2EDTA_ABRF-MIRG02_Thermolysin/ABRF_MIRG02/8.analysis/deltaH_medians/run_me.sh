#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_medians_of_deltaH.py"

export MCMC_LOGNORMAL_R0="/home/tnguye46/bayesian_itc/ABRF_MIRG02/5.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export MCMC_UNIFORM_R0="/home/tnguye46/bayesian_itc/ABRF_MIRG02/5.bitc_mcmc_unifP0_sharplognomLs/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc/ABRF_MIRG02/6.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPE="1_MCS-ITC 3_VP-ITC  5_VP-ITC 6_VP-ITC 7_MCS-ITC 8_VP-ITC 9_VP-ITC 11_VP-ITC 12_VP-ITC 13_VP-ITC"

python $SCRIPT --bitc_mcmc_lognormalR0_dir $MCMC_LOGNORMAL_R0 --bitc_mcmc_uniformR0_dir $MCMC_UNIFORM_R0 --nonlinear_fit_result_file $NONLIN_RES --experiment_names "$EXPE"

