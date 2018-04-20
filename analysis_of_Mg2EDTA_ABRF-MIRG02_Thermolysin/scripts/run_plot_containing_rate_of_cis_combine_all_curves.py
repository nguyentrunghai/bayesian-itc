"""
combine three curves into one plot
"""
from __future__ import print_function

import os
import argparse
import pickle

from _confidence_intervals import plot_containing_rates

parser = argparse.ArgumentParser()

parser.add_argument( "--log_normal_results_dir",     type=str, default="log_nomal_4_conce")
parser.add_argument( "--uniform_results_dir",type=str, default="uniform_prior_4_cell_concen")
parser.add_argument( "--parameter",                 type=str, default="DeltaG")

args = parser.parse_args()

MARKERS = ("o", "<", ">")
COLORS = ("r", "b", "g")

XLABEL = "predicted"
YLABEL = "observed"

log_normal_results_file = os.path.join(args.log_normal_results_dir, args.parameter+"_results.pkl")
uniform_results_file = os.path.join(args.uniform_results_dir, args.parameter+"_results.pkl")
print("log_normal_results_file", log_normal_results_file)
print("uniform_results_file", uniform_results_file)

log_normal_results = pickle.load(open(log_normal_results_file, "r"))
uniform_results = pickle.load(open(uniform_results_file, "r"))

out = args.parameter + ".pdf"

xs = [ log_normal_results["LEVELS_PERCENT"], log_normal_results["LEVELS_PERCENT"], uniform_results["LEVELS_PERCENT"] ]
ys = [ log_normal_results["g_rates"], log_normal_results["b_rates"], uniform_results["b_rates"] ]
yerrs = [ [None for _ in log_normal_results["LEVELS_PERCENT"]], log_normal_results["b_rate_errors"],
         uniform_results["b_rate_errors"] ]

plot_containing_rates(xs, ys, out,
                        observed_rate_errors=yerrs,
                        xlabel=XLABEL,
                        ylabel=YLABEL,
                        xlimits=[0, 100],
                        ylimits=[0, 100],
                        colors=COLORS,
                        markers=MARKERS,
                        markersize=5)