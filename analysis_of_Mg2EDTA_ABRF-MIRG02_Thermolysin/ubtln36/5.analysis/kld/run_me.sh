#!/bin/bash

export SCRIPT="../../../scripts/run_plot_kullback_leibler_divergence.py"

export BITC_KDE="../kde/bitc"

export NONLIN_KDE="../kde/nonlinear_fit"

export EXPER="19052014ubtln36test2 ubtln36a ubtln36a14082014 ubtln36b ubtln36b18082014 ubtln36c14082014 ubtln36d ubtln36e ubtln36f ubtln36g ubtln36h"

python $SCRIPT --bitc_kde_dir $BITC_KDE --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER"

