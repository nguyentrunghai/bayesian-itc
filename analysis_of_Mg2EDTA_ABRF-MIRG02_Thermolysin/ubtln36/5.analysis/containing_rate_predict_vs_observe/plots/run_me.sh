#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_plot_containing_rate_of_cis_combine_all_curves_2.py"

export LNP0_LNLS_DIR="/home/tnguye46/bayesian_itc/ubtln36/5.analysis/containing_rate_predict_vs_observe/lognomP0_lognomLs"

export UNP0_SHARPLNLS_DIR="/home/tnguye46/bayesian_itc/ubtln36/5.analysis/containing_rate_predict_vs_observe/unifP0_sharplognomLs"

export UNP0_LNLS_DIR="/home/tnguye46/bayesian_itc/ubtln36/5.analysis/containing_rate_predict_vs_observe/unifP0_lognomLs"


python $SCRIPT --lognomP0_lognomLs_dir $LNP0_LNLS_DIR --unifP0_sharplognomLs_dir $UNP0_SHARPLNLS_DIR --unifP0_lognomLs_dir $UNP0_LNLS_DIR --parameter "DeltaG"

python $SCRIPT --lognomP0_lognomLs_dir $LNP0_LNLS_DIR --unifP0_sharplognomLs_dir $UNP0_SHARPLNLS_DIR --unifP0_lognomLs_dir $UNP0_LNLS_DIR --parameter "DeltaH"
