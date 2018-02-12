#!/bin/bash

export SCRIPT="../../../scripts/run_plot_marginals.py"

export MCMC_DIR="../../2.bitc_mcmc/repeat_0"

export ITC_DIR="../../1.itc_origin_heat_files"

export EXPERIMENT="Mg1EDTAp1a"

python $SCRIPT --bitc_mcmc_dir $MCMC_DIR --itc_files_dir $ITC_DIR --experiment $EXPERIMENT

