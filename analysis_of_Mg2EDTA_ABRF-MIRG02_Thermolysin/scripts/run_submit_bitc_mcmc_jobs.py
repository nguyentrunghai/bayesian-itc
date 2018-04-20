
import os
import glob
import argparse
parser = argparse.ArgumentParser()

parser.add_argument( "--itc_data_dir",     type=str, default="/home/tnguye46/bayesian_itc_reproduce/ubtln59/1.itc_origin_heat_files")
parser.add_argument( "--heat_data_dir",    type=str, default="/home/tnguye46/bayesian_itc_reproduce/ubtln59/1.itc_origin_heat_files")

parser.add_argument( "--exclude_experiments",   type=str, default="")

parser.add_argument( "--script",                type=str, default ="/home/tnguye46/opt/src/bayesian-itc/scripts/bitc_mcmc.py")
parser.add_argument( "--heat_file_suffix",      type=str, default =".TXT")

parser.add_argument( "--dc",                    type=float, default=0.1)      # cell concentration relative uncertainty
parser.add_argument( "--ds",                    type=float, default=0.001)      # syringe concentration relative uncertainty

parser.add_argument( "--dummy_itc_file",        action="store_true", default=False)

parser.add_argument( "--uniform_cell_concentration",        action="store_true", default=False)
parser.add_argument( "--uniform_syringe_concentration",     action="store_true", default=False)
parser.add_argument( "--concentration_range_factor",        type=float, default=100.)

parser.add_argument( "--niters",            type=int, default=11000000)
parser.add_argument( "--nburn",             type=int, default=1000000)
parser.add_argument( "--nthin",             type=int, default=2000)

parser.add_argument( "--verbosity",         type=str, default="-vvv")

args = parser.parse_args()

TRACES_FILE = "traces.pickle"

itc_data_files = glob.glob(os.path.join(args.itc_data_dir, "*.itc"))
itc_data_files = [os.path.basename(f) for f in itc_data_files]

exper_names = [f.split(".itc")[0] for f in itc_data_files]
for name in exper_names:
    if not os.path.isfile( os.path.join(args.heat_data_dir, name + args.heat_file_suffix) ):
        print "WARNING: Integrated heat file for " + name + " does not exist"
exper_names = [name for name in exper_names if os.path.isfile( os.path.join(args.heat_data_dir, name + args.heat_file_suffix) ) ]


exclude_experiments = args.exclude_experiments.split()
exper_names = [name for name in exper_names if name not in exclude_experiments]

print "Will run these ", exper_names

for name in exper_names:
    out_dir = os.path.abspath(name)
    if not os.path.isdir(name):
        os.makedirs(name)
    itc_file = os.path.join(args.itc_data_dir, name+".itc")
    integ_file = os.path.join(args.heat_data_dir, name + args.heat_file_suffix)

    qsub_file = os.path.join(out_dir, name+"_mcmc.job")
    log_file  = os.path.join(out_dir, name+"_mcmc.log")

    if args.dummy_itc_file:
        dummy_itc_file = ''' --dummy_itc_file '''
    else:
        dummy_itc_file = ''' '''

    if args.uniform_cell_concentration:
        uniform_cell_concentration = ''' --uniform_cell_concentration '''
    else:
        uniform_cell_concentration = ''' '''

    if args.uniform_syringe_concentration:
        uniform_syringe_concentration = ''' --uniform_syringe_concentration '''
    else:
        uniform_syringe_concentration = ''' '''

    qsub_script = '''#!/bin/bash
#PBS -S /bin/bash
#PBS -o %s '''%log_file + '''
#PBS -j oe
#PBS -l nodes=1:ppn=1,mem=2048mb,walltime=72:00:00

source /home/tnguye46/opt/module/anaconda.sh
cd ''' + out_dir + '''\n''' + \
    '''date\n''' + \
    '''python ''' + args.script + ''' twocomponent ''' + itc_file + ''' ''' + integ_file + \
    ''' --dc %f '''%args.dc + \
    ''' --ds %f '''%args.ds + \
    dummy_itc_file + uniform_cell_concentration + uniform_syringe_concentration + \
    ''' --concentration_range_factor %f '''%args.concentration_range_factor + \
    ''' --niters %d '''%args.niters + \
    ''' --nburn %d '''%args.nburn + \
    ''' --nthin %d '''%args.nthin + \
    args.verbosity + \
    '''\ndate \n'''
    if (not os.path.isfile(TRACES_FILE)) or (os.path.getsize(TRACES_FILE) == 0):
        print "Submitting " + qsub_file
        open(qsub_file, "w").write(qsub_script)
        os.system("qsub %s"%qsub_file)
    else:
        print TRACES_FILE + " exists, skip"


