#!/bin/bash

export SCRIPT="../../../scripts/run_display_correlation_matrix.py"

export MCMC_DIR="../../2.bitc_mcmc"

export EXPERIMENT="Mg1EDTAp1a"

python $SCRIPT --repeated_bitc_mcmc_dir $MCMC_DIR --experiment $EXPERIMENT

