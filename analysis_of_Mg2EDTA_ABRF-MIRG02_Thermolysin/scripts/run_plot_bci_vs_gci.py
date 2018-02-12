

import os
import glob
import pickle
import argparse

import pandas as pd
import numpy as np

from _confidence_intervals import bayesian_credible_interval, gaussian_ci_from_mean_std, plot_vertically_stacked_cis

parser = argparse.ArgumentParser()

parser.add_argument( "--bitc_mcmc_dir",             type=str, default="bitc_mcmc")
parser.add_argument( "--nonlinear_fit_result_file", type=str, default="origin_dg_dh_in_kcal_per_mole.dat")

parser.add_argument( "--ordered_experiment_names_1",  type=str, default=" " )
parser.add_argument( "--ordered_experiment_names_2",  type=str, default=" " )

parser.add_argument( "--parameter",                 type=str, default="DeltaG")
parser.add_argument( "--level",                     type=float, default=0.95)
parser.add_argument( "--central",                   type=str, default="median")
parser.add_argument( "--xlimits",                   type=str, default=None )

args = parser.parse_args()

assert args.central in ["mean", "median"], "wrong central"

print "ploting " + args.parameter

TRACES_FILE = "traces.pickle"
XLABELS = {"DeltaG":"$\Delta G$ (kcal/mol)", "DeltaH":"$\Delta H$ (kcal/mol)", "P0":"$[R]_0$ (mM)" }

ordered_experiment_names_1 = args.ordered_experiment_names_1.split()
ordered_experiment_names_2 = args.ordered_experiment_names_2.split()

ordered_experiment_names = ordered_experiment_names_1 + ordered_experiment_names_2
print ordered_experiment_names

use_two_centrals_for_P0 = False
if len(ordered_experiment_names_2) > 0:
    use_two_centrals_for_P0 = True
    print "use two centrals for P0"
else:
    print "use one central for P0"

if args.xlimits is None:
    xlimits = None
else:
    xlimits = [ float(s) for s in args.xlimits.split() ]

print "xlimits = ", xlimits

# bayesian cis

mcmc_trace_files = {exper : os.path.join(args.bitc_mcmc_dir, exper, TRACES_FILE) for exper in ordered_experiment_names}
samples = { exper : pickle.load( open(mcmc_trace_files[exper] , "r") )[args.parameter] for exper in ordered_experiment_names }

lowers          = []
uppers          = []
lower_errors    = []
upper_errors    = []

for exper in ordered_experiment_names:
    lower, upper, lower_error, upper_error = bayesian_credible_interval(samples[exper], args.level, bootstrap_repeats=1000) 

    lowers.append(lower)
    uppers.append(upper)
    lower_errors.append(lower_error)
    upper_errors.append(upper_error)

if args.central == "median":
    b_centrals = [ np.median( [np.median(sample) for sample in samples.values()] ) ]

elif args.central == "mean":
    b_centrals = [ np.mean( [ np.mean(sample) for sample in samples.values() ] ) ]

if use_two_centrals_for_P0 and args.parameter == "P0":
    if args.central == "median":
        b_centrals =  [ np.median( [ np.median(samples[exper]) for exper in ordered_experiment_names_1 ] ) ]
        b_centrals += [ np.median( [ np.median(samples[exper]) for exper in ordered_experiment_names_2 ] ) ]

    elif args.central == "mean":
        b_centrals =  [ np.mean( [ np.mean(samples[exper]) for exper in ordered_experiment_names_1 ] ) ]
        b_centrals += [ np.mean( [ np.mean(samples[exper]) for exper in ordered_experiment_names_2 ] ) ]

out = args.parameter + "_bayesian_cis.pdf"
xlabel = XLABELS[args.parameter]

# error bars to be one standard error
lower_errors = [l/2. for l in lower_errors]
upper_errors = [u/2. for u in upper_errors]

plot_vertically_stacked_cis(  lowers, uppers, xlabel, out,
                            lower_errors=lower_errors,
                            upper_errors=upper_errors,
                            centrals=b_centrals,
                            xlimits=xlimits )


# nonlinear ls cis

nonlinear_fit_results = pd.read_table(args.nonlinear_fit_result_file, sep='\s+')
nonlinear_fit_results = nonlinear_fit_results.reindex(ordered_experiment_names)

for exper in nonlinear_fit_results.index:
    if np.any(nonlinear_fit_results.loc[exper].isnull()):
        raise Exception(exper + " is null")

means = nonlinear_fit_results[ args.parameter ]
stds  = nonlinear_fit_results[ args.parameter + "_std" ]

g_lowers  = []
g_uppers  = []

for mu, sigma in zip(means, stds):
    l, u = gaussian_ci_from_mean_std(mu, sigma, args.level)
    g_lowers.append(l)
    g_uppers.append(u)

if args.central == "median":
    g_centrals = [np.median(means)]
elif args.central == "mean":
    g_centrals = [np.mean(means)]

if use_two_centrals_for_P0 and args.parameter == "P0":
    if args.central == "median":
        g_centrals =  [ np.median( [ means[exper] for exper in ordered_experiment_names_1 ] ) ]
        g_centrals += [ np.median( [ means[exper] for exper in ordered_experiment_names_2 ] ) ]
        
    elif args.central == "mean":
        g_centrals =  [ np.mean( [ means[exper] for exper in ordered_experiment_names_1 ] ) ]
        g_centrals += [ np.mean( [ means[exper] for exper in ordered_experiment_names_2 ] ) ]

out = args.parameter + "_nonlinear_ls_cis.pdf"

plot_vertically_stacked_cis(  g_lowers, g_uppers, xlabel, out,
                            centrals=g_centrals,
                            xlimits=xlimits )

