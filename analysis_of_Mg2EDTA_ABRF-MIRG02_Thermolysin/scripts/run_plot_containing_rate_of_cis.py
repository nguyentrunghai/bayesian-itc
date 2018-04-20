
import os
import argparse
import pickle

import numpy as np
import pandas as pd

from _confidence_intervals import rate_of_containing_from_sample, rate_of_containing_from_means_stds, plot_containing_rates

parser = argparse.ArgumentParser()

parser.add_argument( "--bitc_mcmc_dir",             type=str, default="bitc_mcmc")
parser.add_argument( "--nonlinear_fit_result_file", type=str, default="origin_dg_dh_in_kcal_per_mole.dat")

parser.add_argument( "--ordered_experiment_names",  type=str, default=" " )
parser.add_argument( "--parameter",                 type=str, default="DeltaG")
parser.add_argument( "--central",                   type=str, default="median")

args = parser.parse_args()

assert args.central in ["mean", "median"], "wrong central"

print "ploting " + args.parameter

TRACES_FILE = "traces.pickle"
XLABEL = "predicted"
YLABEL = "observed"

LEVELS_PERCENT = np.linspace(10., 95., num=18)
print "LEVELS_PERCENT", LEVELS_PERCENT
LEVELS = LEVELS_PERCENT / 100.

ordered_experiment_names = args.ordered_experiment_names.split()

# bayesian cis

mcmc_trace_files = [os.path.join(args.bitc_mcmc_dir, exper_name, TRACES_FILE) for exper_name in ordered_experiment_names]
samples = [ pickle.load( open(trace_file , "r") )[args.parameter] for trace_file in mcmc_trace_files ]

b_rates = []
b_rate_errors = []
for level in LEVELS:
    print level
    rate, rate_error = rate_of_containing_from_sample(samples, level, estimate_of_true=args.central, ci_type="bayesian", bootstrap_repeats=1000)

    rate *= 100
    rate_error *= 100

    b_rates.append(rate)
    b_rate_errors.append(rate_error)

# error bars to be one standard error
b_rate_errors = [e/2. for e in b_rate_errors]

out = args.parameter + "_bayesian.pdf"
plot_containing_rates([LEVELS_PERCENT], [b_rates], out,
                        observed_rate_errors=[b_rate_errors],
                        xlabel=XLABEL,
                        ylabel=YLABEL,
                        xlimits=[0, 100],
                        ylimits=[0, 100])

# nonlinear ls cis

nonlinear_fit_results = pd.read_table(args.nonlinear_fit_result_file, sep='\s+')
nonlinear_fit_results = nonlinear_fit_results.reindex(ordered_experiment_names)

for exper in nonlinear_fit_results.index:
    if np.any(nonlinear_fit_results.loc[exper].isnull()):
        raise Exception(exper + " is null")

means = nonlinear_fit_results[ args.parameter ]
stds  = nonlinear_fit_results[ args.parameter + "_std" ]

g_rates = []
for level in LEVELS:
    g_rate = rate_of_containing_from_means_stds(means, stds, level, estimate_of_true=args.central)

    g_rate *= 100
    g_rates.append(g_rate)

out = args.parameter + "_nonlinear_ls.pdf"
plot_containing_rates([LEVELS_PERCENT], [g_rates], out,
                        observed_rate_errors=None,
                        xlabel=XLABEL,
                        ylabel=YLABEL,
                        xlimits=[0, 100],
                        ylimits=[0, 100])


# dump result
pickle.dump({"LEVELS_PERCENT":LEVELS_PERCENT, "b_rates":b_rates, "b_rate_errors":b_rate_errors, "g_rates":g_rates},
            open(args.parameter + "_results.pkl", "w"))
