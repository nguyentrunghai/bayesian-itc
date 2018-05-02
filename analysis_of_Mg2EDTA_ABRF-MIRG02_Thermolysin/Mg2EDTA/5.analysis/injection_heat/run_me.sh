#!/bin/bash

export SCRIPT="/home/tnguye46/opt/src/bayesian-itc/analysis_of_Mg2EDTA_ABRF-MIRG02_Thermolysin/scripts/run_injection_heat.py"

export TRACE="/home/tnguye46/bayesian_itc/Mg2EDTA/2.bitc_mcmc_lognomP0_lognomLs/repeat_0/Mg1EDTAp1a/traces.pickle"

python $SCRIPT --mcmc_trace_file $TRACE

