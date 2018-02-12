#!/bin/bash

export SCRIPT="../../../scripts/run_plot_ci_convergence.py"

export MCMC_DIR="../../5.bitc_mcmc"

export EXPERIMENT="1_MCS-ITC"

python $SCRIPT --repeated_bitc_mcmc_dir $MCMC_DIR --experiment $EXPERIMENT

