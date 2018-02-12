#!/bin/bash

export SCRIPT="../../../scripts/run_injection_heat.py"

export TRACE="../../2.bitc_mcmc/repeat_0/Mg1EDTAp1a/traces.pickle"

python $SCRIPT --mcmc_trace_file $TRACE

