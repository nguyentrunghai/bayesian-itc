#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_kullback_leibler_divergence.py"

export BITC_KDE="/home/tnguye46/bayesian_itc/ABRF_MIRG02/8.analysis/kde/bitc"

export NONLIN_KDE="/home/tnguye46/bayesian_itc/ABRF_MIRG02/8.analysis/kde/nonlinear_fit"

export EXPER="1_MCS-ITC 3_VP-ITC  5_VP-ITC 6_VP-ITC 7_MCS-ITC 8_VP-ITC 9_VP-ITC 11_VP-ITC 12_VP-ITC 13_VP-ITC"

python $SCRIPT --bitc_kde_dir $BITC_KDE --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER"

