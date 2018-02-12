#!/bin/bash

export SCRIPT="../../../scripts/run_plot_kullback_leibler_divergence.py"

export BITC_KDE="../kde/bitc"

export NONLIN_KDE="../kde/nonlinear_fit"

export EXPER="18052014ubtln35test1 18052014ubtln35test2 19052014ubtln35test1 19052014ubtln35test2 ubtln35test1 ubtln35test2 ubtln35k ubtln35L ubtln35m ubtln35o"

python $SCRIPT --bitc_kde_dir $BITC_KDE --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER"

