#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_kullback_leibler_divergence.py"

export SCRIPT2="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_kullback_leibler_divergence_2.py"

export LOGNORP0_LOGNORLS="/home/tnguye46/bayesian_itc/ubtln35/5.analysis/kde/lognomP0_lognomLs"

export UNIFP0_LOGNORLS="/home/tnguye46/bayesian_itc/ubtln35/5.analysis/kde/unifP0_lognomLs"

export NONLIN_KDE="/home/tnguye46/bayesian_itc/ubtln35/5.analysis/kde/nonlinear_fit"

export EXPER="18052014ubtln35test1 18052014ubtln35test2 19052014ubtln35test1 19052014ubtln35test2 ubtln35test1 ubtln35test2 ubtln35k ubtln35L ubtln35m ubtln35o"

#python $SCRIPT --bitc_kde_dir $LOGNORP0_LOGNORLS --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER" --out "kld_bitc_lognorR0_lognorLs_vs_nonlinear_fit.pdf"

#python $SCRIPT --bitc_kde_dir $UNIFP0_LOGNORLS --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER" --out "kld_bitc_unifR0_lognomLs_vs_nonlinear_fit.pdf"

python $SCRIPT2 --lognorP0_lognorLs_kde_dir $LOGNORP0_LOGNORLS --unifP0_lognorLs_kde_dir $UNIFP0_LOGNORLS --nonlinear_kde_dir $NONLIN_KDE --ordered_experiment_names "$EXPER"

