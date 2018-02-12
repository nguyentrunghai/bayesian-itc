#!/bin/bash

export SCRIPT="../../../scripts/run_plot_ci_convergence.py"

export MCMC_DIR="../../2.bitc_mcmc"

export EXPERIMENT="18052014ubtln35test1"

python $SCRIPT --repeated_bitc_mcmc_dir $MCMC_DIR --experiment $EXPERIMENT

