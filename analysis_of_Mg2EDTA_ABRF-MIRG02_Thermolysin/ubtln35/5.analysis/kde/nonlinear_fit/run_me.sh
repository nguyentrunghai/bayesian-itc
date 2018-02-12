#!/bin/bash

export SCRIPT="../../../../scripts/run_kde_2d.py"

export MCMC_DIR="../../../4.gaussian_mcmc"

export EXPER="18052014ubtln35test1 18052014ubtln35test2 19052014ubtln35test1 19052014ubtln35test2 ubtln35test1 ubtln35test2 ubtln35k ubtln35L ubtln35m ubtln35o"

python $SCRIPT --mcmc_dir $MCMC_DIR --ordered_experiment_names "$EXPER"
