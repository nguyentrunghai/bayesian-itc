#!/bin/bash

export SCRIPT="../../../scripts/run_plot_kullback_leibler_divergence.py"

export BITC_KDE="../kde/bitc"

export NONLIN_KDE="../kde/nonlinear_fit"

export EXPER="ubtln59a ubtln59a21082014 ubtln59altesProtein ubtln59b ubtln59b21082014 ubtln59c ubtln59c21082014 ubtln59d ubtln59neuesProtein"

python $SCRIPT --bitc_kde_dir $BITC_KDE --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER"

