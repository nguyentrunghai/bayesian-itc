#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_ci_convergence.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc/Mg2EDTA/2.bitc_mcmc_lognomP0_lognomLs"

export EXPERIMENT="Mg1EDTAp1a"

python $SCRIPT --repeated_bitc_mcmc_dir $MCMC_DIR --experiment $EXPERIMENT

