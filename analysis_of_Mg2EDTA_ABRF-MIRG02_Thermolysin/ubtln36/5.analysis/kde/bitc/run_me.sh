#!/bin/bash

export SCRIPT="../../../../scripts/run_kde_2d.py"

export MCMC_DIR="../../../2.bitc_mcmc/repeat_0"

export EXPER="19052014ubtln36test2 ubtln36a ubtln36a14082014 ubtln36b ubtln36b18082014 ubtln36c14082014 ubtln36d ubtln36e ubtln36f ubtln36g ubtln36h"

python $SCRIPT --mcmc_dir $MCMC_DIR --ordered_experiment_names "$EXPER"
