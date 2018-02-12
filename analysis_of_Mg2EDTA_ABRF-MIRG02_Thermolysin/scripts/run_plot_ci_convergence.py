
import glob
import os
import argparse
import pickle

import numpy as np

from _confidence_intervals import ci_convergence, plot_ci_convergence

parser = argparse.ArgumentParser()
parser.add_argument( "--repeated_bitc_mcmc_dir",        type=str, default="bitc_mcmc")
parser.add_argument( "--repeat_prefix",                 type=str, default="repeat_")
parser.add_argument( "--experiment",                    type=str, default=" ")

parser.add_argument( "--level",                         type=float, default=0.95)

parser.add_argument( "--begin",                         type=int, default=50)
parser.add_argument( "--end",                           type=int, default=5000)
parser.add_argument( "--nr_of_stops",                   type=int, default=25)

args = parser.parse_args()

TRACES_FILE = "traces.pickle"

XLABEL  = "# samples"

YLABEL = {  "DeltaG"    :   "$\Delta G$ (kcal/mol)", 
            "DeltaH"    :   "$\Delta H$ (kcal/mol)", 
            "DeltaH_0"  :   "$\Delta H_0$ ($\mu$cal)",
            "P0"        :   "$[R]_0$ (mM)", 
            "Ls"        :   "$[L_T]_s$ (mM)", 
            "log_sigma" :   "$\ln \sigma$" }

list_of_stops = np.linspace(args.begin, args.end, args.nr_of_stops, dtype=int)
print "list_of_stops", list_of_stops

traces_files = glob.glob( os.path.join( args.repeated_bitc_mcmc_dir, args.repeat_prefix+"*", args.experiment, TRACES_FILE) )
print "traces_files:", traces_files

mcmc_samples = [ pickle.load( open(trace_file , "r") ) for trace_file in traces_files ]

for quantity in YLABEL:

    samples = [mcmc_sample[quantity] for mcmc_sample in mcmc_samples]

    lowers, uppers = ci_convergence(samples, list_of_stops, args.level, ci_type="bayesian")

    # change from cal to mu cal for "DeltaH_0"
    if quantity == "DeltaH_0":
        lowers *= 10**6
        uppers *= 10**6

    out = args.experiment + "_" + quantity + ".pdf"

    plot_ci_convergence(lowers, uppers, list_of_stops, XLABEL, YLABEL[quantity], out )


