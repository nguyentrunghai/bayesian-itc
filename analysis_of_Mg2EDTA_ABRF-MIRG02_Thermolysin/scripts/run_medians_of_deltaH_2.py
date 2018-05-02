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

parser.add_argument( "--lognorP0_lognorLs_dir", type=str, default="bitc_mcmc_lognomP0_lognomL")
parser.add_argument( "--unifP0_sharplognorLs_dir",   type=str, default="bitc_mcmc_unifP0_sharplognomLs")
parser.add_argument( "--unifP0_lognorLs_dir",   type=str, default="bitc_mcmc_unifP0_lognomLs")

parser.add_argument( "--nonlinear_fit_result_file", type=str, default="origin_dg_dh_in_kcal_per_mole.dat")
parser.add_argument( "--experiment_names",  type=str, default=" ")
args = parser.parse_args()

TRACES_FILE = "traces.pickle"
VARIABLE = "DeltaH"

def _median_from_mcmc_samples(samples):
    return np.median( [np.median(sample) for sample in samples] )


experiment_names = args.experiment_names.split()

lognorP0_lognorLs_trace_files = [os.path.join(args.lognorP0_lognorLs_dir, exper, TRACES_FILE)
                                for exper in experiment_names]

unifP0_sharplognorLs_trace_files = [os.path.join(args.unifP0_sharplognorLs_dir, exper, TRACES_FILE)
                                for exper in experiment_names]

unifP0_lognorLs_trace_files = [os.path.join(args.unifP0_lognorLs_dir, exper, TRACES_FILE)
                                for exper in experiment_names]


lognorP0_lognorLs_samples = [pickle.load( open(trace_file , "r") )[VARIABLE] for trace_file in lognorP0_lognorLs_trace_files]



unifP0_sharplognorLs_samples = [pickle.load( open(trace_file , "r") )[VARIABLE] for trace_file in unifP0_sharplognorLs_trace_files]


unifP0_lognorLs_samples = [pickle.load( open(trace_file , "r") )[VARIABLE] for trace_file in unifP0_lognorLs_trace_files]


nonlinear_fit_results = pd.read_table(args.nonlinear_fit_result_file, sep='\s+')
nonlinear_fit_results = nonlinear_fit_results.reindex(experiment_names)

for exper in nonlinear_fit_results.index:
    if np.any(nonlinear_fit_results.loc[exper].isnull()):
        raise Exception(exper + " is null")

nonlinear_fit_means = nonlinear_fit_results[VARIABLE]
print "nonlinear least squares", np.median(nonlinear_fit_means)
print "BITC uniform R0 sharp lognormal Ls", _median_from_mcmc_samples(unifP0_sharplognorLs_samples)
print "BITC uniform R0 lognormal Ls", _median_from_mcmc_samples(unifP0_lognorLs_samples)
print "BITC lognormal R0 lognormal Ls", _median_from_mcmc_samples(lognorP0_lognorLs_samples)

