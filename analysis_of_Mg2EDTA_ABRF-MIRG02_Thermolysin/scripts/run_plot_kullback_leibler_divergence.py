
import os
import pickle
import argparse

import numpy as np

from _kde_kullback_leibler_divergence import plot_pair_of_annotated_heatmap, numerical_kl_div

parser = argparse.ArgumentParser()

parser.add_argument( "--bitc_kde_dir",              type=str, default="bitc")
parser.add_argument( "--nonlinear_kde_dir",         type=str, default="nonlinear_fit")

parser.add_argument( "--ordered_experiment_names",  type=str, default=" " )

parser.add_argument( "--out",                       type=str, default="kld_bitc_vs_nonlinear_fit.pdf" )

args = parser.parse_args()

ordered_experiment_names = args.ordered_experiment_names.split()

def _kld_matrix(kde_dir, ordered_experiment_names):
    nr_exper = len(ordered_experiment_names)
    kld_matrix = np.zeros([nr_exper, nr_exper], dtype=float)

    for i, exper_p in enumerate(ordered_experiment_names):
        density_file_p = os.path.join(kde_dir, exper_p+".pkl")
        print "density_file_p: ", density_file_p

        data_p = pickle.load( open(density_file_p, "r") )
        area_p = data_p["bin_area"]
        den_p  = data_p["density_grid"]

        for j, exper_q in enumerate(ordered_experiment_names):
            density_file_q = os.path.join(kde_dir, exper_q+".pkl")
            data_q = pickle.load( open(density_file_q, "r") )
            area_q = data_q["bin_area"]
            assert area_p == area_q, "area_p not equal area_q"

            den_q = data_q["density_grid"]
            kld_matrix[i, j] = numerical_kl_div(area_p, den_p, den_q)
    return kld_matrix

kld_matrix_bitc   = _kld_matrix(args.bitc_kde_dir, ordered_experiment_names)
kld_matrix_nonlin = _kld_matrix(args.nonlinear_kde_dir, ordered_experiment_names)

kld_matrix_bitc_log = np.log(kld_matrix_bitc)
kld_matrix_bitc_log[kld_matrix_bitc_log == -np.inf] = 1.

kld_matrix_nonlin_log = np.log(kld_matrix_nonlin)
kld_matrix_nonlin_log[kld_matrix_nonlin_log == -np.inf] = 1.


plot_pair_of_annotated_heatmap(kld_matrix_bitc_log, kld_matrix_nonlin_log, args.out)


