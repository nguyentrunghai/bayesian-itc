
import argparse
import pickle

import pymc
import pandas as pd

class _UncorrGaussians:
    def __init__(self, mus, sigmas):
        """
        mus, sigmas are dict, var -> value
        """
        for var in mus:
            assert var in sigmas, var + " in mus but not in sigmas"

        for var in sigmas:
            assert var in mus, var + " in sigmas but not in mus"

        variables = mus.keys()
        for var in variables:
            mu = mus[var]
            tau = 1./( sigmas[var]**2 )
            setattr( self, var, pymc.Normal(var, mu=mu, tau=tau) )


def _run_mcmc(model, iter, burn, thin):
    mcmc = pymc.MCMC(model)
    mcmc.sample(iter=iter, burn=burn, thin=thin)
    pymc.Matplot.plot(mcmc)
    traces = {}
    for s in mcmc.stochastics:
        traces[s.__name__] = s.trace(chain=None)
    return traces

def _read_nonlinear_fit_results(file_name, experiment_name, variables=["DeltaG", "DeltaH", "P0"]):
    """
    return mus, sigs which are dic mapping exper to dic mapping variable to float
    """
    results = pd.read_table(file_name, sep='\s+')

    mus  = { variable : results.loc[experiment_name, variable] for variable in variables}
    sigs = { variable : results.loc[experiment_name, variable+"_std"] for variable in variables} 
    return mus, sigs


parser = argparse.ArgumentParser()
parser.add_argument( "--nonlinear_fit_results_file",    type=str, default="origin_dg_dh_in_kcal_per_mole.dat")
parser.add_argument( "--experiment",                    type=str, default=" ")

parser.add_argument( "--iter",           type=int, default = 310000)
parser.add_argument( "--burn",           type=int, default = 10000)
parser.add_argument( "--thin",           type=int, default = 100)

args = parser.parse_args()

VARIABLES = ["DeltaG", "DeltaH", "P0"]
print "variables", VARIABLES
mus, sigs = _read_nonlinear_fit_results(args.nonlinear_fit_results_file, args.experiment, variables=VARIABLES)
print "Inputs:"
for var in mus:
    print "%-10s(std) = %15.5f (%15.5f)"%(var, mus[var], sigs[var])

model = _UncorrGaussians(mus, sigs)
traces = _run_mcmc(model, iter=args.iter, burn=args.burn, thin=args.thin)
pickle.dump(traces, open("traces.pickle", "w"))

print "\n"
print "MCMC estimates:"
for var in traces:
    print "%-10s(std) = %15.5f (%15.5f)"%(var, traces[var].mean(), traces[var].std())
print "DONE"


