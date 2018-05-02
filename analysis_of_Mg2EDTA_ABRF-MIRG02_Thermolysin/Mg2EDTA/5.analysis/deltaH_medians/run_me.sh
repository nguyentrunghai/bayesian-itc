#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_medians_of_deltaH.py"

export MCMC_LOGNORMAL_R0="/home/tnguye46/bayesian_itc/Mg2EDTA/2.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export MCMC_UNIFORM_R0="/home/tnguye46/bayesian_itc/Mg2EDTA/2.bitc_mcmc_unifP0_sharplognomLs/repeat_0"

export NONLIN_RES="/home/tnguye46/bayesian_itc/Mg2EDTA/3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat"

export EXPE="Mg1EDTAp1a Mg1EDTAp1b Mg1EDTAp1c Mg1EDTAp1d Mg1EDTAp1e Mgp5EDTAp05a Mgp5EDTAp05b Mgp5EDTAp05c Mgp5EDTAp05e Mgp5EDTAp05f Mgp5EDTAp05g Mgp5EDTAp05h Mgp5EDTAp05i Mgp5EDTAp05j"

python $SCRIPT --bitc_mcmc_lognormalR0_dir $MCMC_LOGNORMAL_R0 --bitc_mcmc_uniformR0_dir $MCMC_UNIFORM_R0 --nonlinear_fit_result_file $NONLIN_RES --experiment_names "$EXPE"

