"""
to get medians of Delta H for Bayesian ITC with different concentration priors
and for nonlinear regression
"""

import os
import argparse
import pickle

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument( "--bitc_mcmc_lognormalR0_dir", type=str, default="bitc_mcmc")
parser.add_argument( "--bitc_mcmc_uniformR0_dir",   type=str, default="bitc_mcmc_uniform_prior_4_cell_concen")
parser.add_argument( "--nonlinear_fit_result_file", type=str, default="origin_dg_dh_in_kcal_per_mole.dat")
parser.add_argument( "--experiment_names",  type=str, default=" ")
args = parser.parse_args()

TRACES_FILE = "traces.pickle"
VARIABLE = "DeltaH"

def _median_from_mcmc_samples(samples):
    return np.median( [np.median(sample) for sample in samples] )


experiment_names = args.experiment_names.split()

mcmc_lognormalR0_trace_files = [os.path.join(args.bitc_mcmc_lognormalR0_dir, exper, TRACES_FILE)
                                for exper in experiment_names]

mcmc_uniformR0_trace_files = [os.path.join(args.bitc_mcmc_uniformR0_dir, exper, TRACES_FILE)
                                for exper in experiment_names]

lognormalR0_samples = [pickle.load( open(trace_file , "r") )[VARIABLE] for trace_file in mcmc_lognormalR0_trace_files]

uniformR0_samples = [pickle.load( open(trace_file , "r") )[VARIABLE] for trace_file in mcmc_uniformR0_trace_files]

nonlinear_fit_results = pd.read_table(args.nonlinear_fit_result_file, sep='\s+')
nonlinear_fit_results = nonlinear_fit_results.reindex(experiment_names)

for exper in nonlinear_fit_results.index:
    if np.any(nonlinear_fit_results.loc[exper].isnull()):
        raise Exception(exper + " is null")

nonlinear_fit_means = nonlinear_fit_results[VARIABLE]
print "nonlinear least squares", np.median(nonlinear_fit_means)
print "BITC uniform R0", _median_from_mcmc_samples(uniformR0_samples)
print "BITC lognormal R0", _median_from_mcmc_samples(lognormalR0_samples)

