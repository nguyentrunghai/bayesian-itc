
import os
import argparse

import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument( "--script",                        type=str, default="/home/tnguye46/bayesian_itc_reproduce/scripts/uncorr_gaussians_mcmc.py")
parser.add_argument( "--nonlinear_fit_results_file",    type=str, default="/home/tnguye46/bayesian_itc_reproduce/ubtln59/3.nonlinear_fit_results/origin_dg_dh_in_kcal_per_mole.dat")

parser.add_argument( "--iter",           type=int, default=310000)
parser.add_argument( "--burn",           type=int, default=10000)
parser.add_argument( "--thin",           type=int, default=100)
args = parser.parse_args()

experiment_names = pd.read_table(args.nonlinear_fit_results_file, sep='\s+').index
experiment_names = list(experiment_names)
print "experiment_names", experiment_names

for experiment in experiment_names:
    out_dir = os.path.abspath(experiment)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    qsub_file = os.path.join(out_dir, experiment+"_mcmc.job")
    log_file  = os.path.join(out_dir, experiment+"_mcmc.log")

    qsub_script = '''#!/bin/bash
#PBS -S /bin/bash
#PBS -o %s '''%log_file + '''
#PBS -j oe
#PBS -l nodes=1:ppn=1,mem=2048mb,walltime=72:00:00

source /home/tnguye46/opt/module/anaconda.sh
cd ''' + out_dir + '''\n''' + \
    '''date\n''' + \
    '''python ''' + args.script + " --nonlinear_fit_results_file " + args.nonlinear_fit_results_file + \
    " --experiment " + experiment +\
    " --iter %d "%args.iter + \
    " --burn %d "%args.burn + \
    " --thin %d "%args.thin + \
    '''\ndate \n'''

    print "Submitting " + qsub_file
    open(qsub_file, "w").write(qsub_script)
    os.system("qsub %s"%qsub_file)


