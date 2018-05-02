#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_kde_2d.py"

export MCMC_DIR="/home/tnguye46/bayesian_itc/ubtln59/2.bitc_mcmc_lognomP0_lognomLs/repeat_0"

export EXPER="ubtln59a ubtln59a21082014 ubtln59altesProtein ubtln59b ubtln59b21082014 ubtln59c ubtln59c21082014 ubtln59d ubtln59neuesProtein"

python $SCRIPT --mcmc_dir $MCMC_DIR --ordered_experiment_names "$EXPER"
