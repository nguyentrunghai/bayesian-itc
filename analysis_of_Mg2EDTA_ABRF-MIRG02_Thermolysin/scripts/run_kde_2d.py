
import os
import argparse
import pickle

from _kde_kullback_leibler_divergence import overal_min_max, kde2D_PQ, remove_outliers

parser = argparse.ArgumentParser()

parser.add_argument( "--mcmc_dir",                  type=str, default="bitc_mcmc")
parser.add_argument( "--ordered_experiment_names",  type=str, default=" " )

parser.add_argument( "--x",                         type=str, default="DeltaG" )
parser.add_argument( "--y",                         type=str, default="DeltaH" )

parser.add_argument( "--bandwidth",                 type=float, default=0.03 )

args = parser.parse_args()

XBINS = 50j
YBINS = 50j

TRACES_FILE = "traces.pickle"

ordered_experiment_names = args.ordered_experiment_names.split()

mcmc_trace_files = [os.path.join(args.mcmc_dir, exper_name, TRACES_FILE) for exper_name in ordered_experiment_names]
xs = [ pickle.load( open(trace_file , "r") )[args.x] for trace_file in mcmc_trace_files ]
ys = [ pickle.load( open(trace_file , "r") )[args.y] for trace_file in mcmc_trace_files ]

xs = [remove_outliers(x) for x in xs]
ys = [remove_outliers(y) for y in ys]

xmin, xmax = overal_min_max(xs)
ymin, ymax = overal_min_max(ys)
print "xmin, xmax: ", xmin, xmax
print "ymin, ymax: ", ymin, ymax

for exper, x, y in zip(ordered_experiment_names, xs, ys):
    print exper
    bin_area, density_grid = kde2D_PQ(x, y, args.bandwidth, xmin, xmax, ymin, ymax, xbins=XBINS, ybins=YBINS)
    data = {"bin_area":bin_area, "density_grid":density_grid}

    out = exper + ".pkl"

    pickle.dump(data, open(out, "w") )
