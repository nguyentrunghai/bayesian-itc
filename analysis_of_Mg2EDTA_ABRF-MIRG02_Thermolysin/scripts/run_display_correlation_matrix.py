
import os
import glob
import pickle
import argparse

import numpy as np

TRACES_FILE = "traces.pickle"


def _covariance(a, b):
    return np.cov(a,b)[0,1]


def _correlation(a, b):
    return np.corrcoef(a,b)[0,1]                                                                                                                                    


def correlation_matrix(mcmc_samples):
    """
    """
    variables = sorted(mcmc_samples.keys())
    corr_matrix = np.zeros([len(variables), len(variables)], dtype=float)

    for i in range(len(variables)):
        for j in range(len(variables)):
            corr_matrix[i,j] = _correlation(mcmc_samples[variables[i]], mcmc_samples[variables[j]])
    return variables, corr_matrix


def display_correlation_matrix(corr_matrix, variables):
    """
    """
    text_string = "".join(["{:^12}".format("")] + ["{:^10}".format(c) for c in variables] ) + "\n\n\n"
    for i in range(corr_matrix.shape[0]):
        text_string += "".join(["{:<12}".format(variables[i])] + ["{:^10.4f}".format(n) for n in corr_matrix[i]] ) + "\n\n\n"
    return text_string


def display_correlation_matrix_with_mean_std(mean_matrix, std_matrix, variables):
    """
    """
    assert mean_matrix.shape == std_matrix.shape, "mean_matrix and std_matrix must have the same shape"
    text_string = "".join(["{:^12}".format("")] + ["{:^30}".format(c) for c in variables] ) + "\n\n\n"
    for i in range(mean_matrix.shape[0]):
        text_string += "".join(["{:<12}".format(variables[i])] + ["{:<12.10f}({:>11.10f})     ".format(m, s) for m, s in zip(mean_matrix[i], std_matrix[i]) ] ) + "\n\n"
    return text_string


parser = argparse.ArgumentParser()
parser.add_argument( "--repeated_bitc_mcmc_dir",        type=str, default="bitc_mcmc")
parser.add_argument( "--repeat_prefix",                 type=str, default="repeat_")
parser.add_argument( "--experiment",                    type=str, default=" ")
args = parser.parse_args()

traces_files = glob.glob( os.path.join( args.repeated_bitc_mcmc_dir, args.repeat_prefix+"*", args.experiment, TRACES_FILE) )
print "traces_files:", traces_files

repeated_samples = [ pickle.load( open(trace_file , "r") ) for trace_file in traces_files ]

corr_matrices = []
variables = []
for samples in repeated_samples:
    var, corr_matrix = correlation_matrix(samples)
    corr_matrices.append(corr_matrix)
    variables.append(var)

corr_matrices = np.array(corr_matrices)
mean_matrix = corr_matrices.mean(axis=0)
std_matrix  = corr_matrices.std(axis=0)

print "variables", variables
text_string = display_correlation_matrix_with_mean_std(mean_matrix, std_matrix, variables[0])
print "\n\n" + text_string

