#!/bin/bash

export SCRIPT="../../../../scripts/run_kde_2d.py"

export MCMC_DIR="../../../4.gaussian_mcmc"

export EXPER="ubtln59a ubtln59a21082014 ubtln59altesProtein ubtln59b ubtln59b21082014 ubtln59c ubtln59c21082014 ubtln59d ubtln59neuesProtein"

python $SCRIPT --mcmc_dir $MCMC_DIR --ordered_experiment_names "$EXPER"
