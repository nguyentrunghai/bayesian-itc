#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_kullback_leibler_divergence.py"

export SCRIPT2="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_kullback_leibler_divergence_2.py"

export LOGNORP0_LOGNORLS="/home/tnguye46/bayesian_itc/ubtln36/5.analysis/kde/lognomP0_lognomLs"

export UNIFP0_LOGNORLS="/home/tnguye46/bayesian_itc/ubtln36/5.analysis/kde/unifP0_lognomLs"

export NONLIN_KDE="/home/tnguye46/bayesian_itc/ubtln36/5.analysis/kde/nonlinear_fit"

export EXPER="19052014ubtln36test2 ubtln36a ubtln36a14082014 ubtln36b ubtln36b18082014 ubtln36c14082014 ubtln36d ubtln36e ubtln36f ubtln36g ubtln36h"

#python $SCRIPT --bitc_kde_dir $LOGNORP0_LOGNORLS --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER" --out "kld_bitc_lognorR0_lognorLs_vs_nonlinear_fit.pdf"

#python $SCRIPT --bitc_kde_dir $UNIFP0_LOGNORLS --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER" --out "kld_bitc_unifR0_lognomLs_vs_nonlinear_fit.pdf"

python $SCRIPT2 --lognorP0_lognorLs_kde_dir $LOGNORP0_LOGNORLS --unifP0_lognorLs_kde_dir $UNIFP0_LOGNORLS --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER"

