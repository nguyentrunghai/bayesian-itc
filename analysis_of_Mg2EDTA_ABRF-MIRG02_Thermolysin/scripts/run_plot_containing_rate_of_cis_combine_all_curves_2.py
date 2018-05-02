"""
combine three curves into one plot
"""
from __future__ import print_function

import os
import argparse
import pickle

from _confidence_intervals import plot_containing_rates

parser = argparse.ArgumentParser()

parser.add_argument( "--lognomP0_lognomLs_dir",     type=str, default="lognomP0_lognomLs")
parser.add_argument( "--unifP0_sharplognomLs_dir",type=str, default="unifP0_sharplognomLs")
parser.add_argument( "--unifP0_lognomLs_dir",type=str, default="unifP0_lognomLs")

parser.add_argument( "--parameter",                 type=str, default="DeltaG")

args = parser.parse_args()

MARKERS = ("o", "<", ">", "s")
COLORS = ("r", "b", "g", "k")

XLABEL = "predicted"
YLABEL = "observed"

lognomP0_lognomLs_results_file = os.path.join(args.lognomP0_lognomLs_dir, args.parameter+"_results.pkl")
unifP0_sharplognomLs_results_file = os.path.join(args.unifP0_sharplognomLs_dir, args.parameter+"_results.pkl")
unifP0_lognomLs_results_file = os.path.join(args.unifP0_lognomLs_dir, args.parameter+"_results.pkl")


print("lognomP0_lognomLs_results_file", lognomP0_lognomLs_results_file)
print("unifP0_sharplognomLs_results_file", unifP0_sharplognomLs_results_file)
print("unifP0_lognomLs_results_file", unifP0_lognomLs_results_file)

lognomP0_lognomLs_results = pickle.load(open(lognomP0_lognomLs_results_file, "r"))
unifP0_sharplognomLs_results = pickle.load(open(unifP0_sharplognomLs_results_file, "r"))
unifP0_lognomLs_results = pickle.load(open(unifP0_lognomLs_results_file, "r"))

out = args.parameter + ".pdf"

xs = [ lognomP0_lognomLs_results["LEVELS_PERCENT"], lognomP0_lognomLs_results["LEVELS_PERCENT"],
       unifP0_sharplognomLs_results["LEVELS_PERCENT"], unifP0_lognomLs_results["LEVELS_PERCENT"]]

ys = [ lognomP0_lognomLs_results["g_rates"], lognomP0_lognomLs_results["b_rates"],
       unifP0_sharplognomLs_results["b_rates"], unifP0_lognomLs_results["b_rates"] ]

yerrs = [ [None for _ in lognomP0_lognomLs_results["LEVELS_PERCENT"]], lognomP0_lognomLs_results["b_rate_errors"],
          unifP0_sharplognomLs_results["b_rate_errors"], unifP0_lognomLs_results["b_rate_errors"] ]

plot_containing_rates(xs, ys, out,
                        observed_rate_errors=yerrs,
                        xlabel=XLABEL,
                        ylabel=YLABEL,
                        xlimits=[0, 100],
                        ylimits=[0, 100],
                        colors=COLORS,
                        markers=MARKERS,
                        markersize=5)