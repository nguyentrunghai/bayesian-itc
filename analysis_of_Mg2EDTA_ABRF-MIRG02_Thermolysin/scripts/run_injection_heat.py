

import argparse
import pickle
import numpy

import matplotlib
import matplotlib.pyplot as plt

# copied from bayesian_itc
def expected_injection_heats(V0, DeltaVn, P0, Ls, DeltaG, DeltaH, DeltaH_0, beta, N):
    """
    Expected heats of injection for two-component binding model.

    ARGUMENTS
    V0 - cell volume (liter)
    DeltaVn - injection volumes (liter)
    P0 - Cell concentration (millimolar)
    Ls - Syringe concentration (millimolar)
    DeltaG - free energy of binding (kcal/mol)
    DeltaH - enthalpy of binding (kcal/mol)
    DeltaH_0 - heat of injection (cal)
    beta - inverse temperature * gas constant (mole / kcal)
    N - number of injections

    Returns
    -------
    expected injection heats -

    """

    Kd = numpy.exp(beta * DeltaG)   # dissociation constant (M)
    N = N

    # Compute complex concentrations.
    # Pn[n] is the protein concentration in sample cell after n injections
    # (M)
    Pn = numpy.zeros([N])
    # Ln[n] is the ligand concentration in sample cell after n injections
    # (M)
    Ln = numpy.zeros([N])
    # PLn[n] is the complex concentration in sample cell after n injections
    # (M)
    PLn = numpy.zeros([N])
    dcum = 1.0  # cumulative dilution factor (dimensionless)
    for n in range(N):
        # Instantaneous injection model (perfusion)
        # TODO: Allow injection volume to vary for each injection.
        # dilution factor for this injection (dimensionless)
        d = 1.0 - (DeltaVn[n] / V0)
        dcum *= d  # cumulative dilution factor
        # total quantity of protein in sample cell after n injections (mol)
        P = V0 * P0 * 1.e-3 * dcum
        # total quantity of ligand in sample cell after n injections (mol)
        L = V0 * Ls * 1.e-3 * (1. - dcum)
        # complex concentration (M)
        PLn[n] = (0.5 / V0 * ((P + L + Kd * V0) - ((P + L + Kd * V0) ** 2 - 4 * P * L) ** 0.5))
        # free protein concentration in sample cell after n injections (M)
        Pn[n] = P / V0 - PLn[n]
        # free ligand concentration in sample cell after n injections (M)
        Ln[n] = L / V0 - PLn[n]

    # Compute expected injection heats.
    # q_n_model[n] is the expected heat from injection n
    q_n = numpy.zeros([N])
    # Instantaneous injection model (perfusion)
    # first injection
    q_n[0] = (DeltaH * V0 * PLn[0])*1000 + DeltaH_0
    for n in range(1, N):
        d = 1.0 - (DeltaVn[n] / V0)  # dilution factor (dimensionless)
        # subsequent injections
        q_n[n] = (DeltaH * V0 * (PLn[n] - d * PLn[n - 1])) * 1000 + DeltaH_0

    return q_n


def linear_regression(x, y):
    """
    """
    z = numpy.polyfit(x, y, 1)
    a = z[0]        # slope
    b = z[1]        # intercept
    return lambda u: a*u + b



#-------------

parser = argparse.ArgumentParser()

parser.add_argument( "--mcmc_trace_file",   type=str, default="traces.pickle")
parser.add_argument( "--out",   type=str, default="injection_heat.pdf")

args = parser.parse_args()

TEMPERATURE = 298.15
KB = 0.0019872041      # in kcal/mol/K
BETA = 1 / TEMPERATURE / KB

figure_size=(3.2, 2.4)
lw=1.0
font = {"fontname": "Arial"}
fontsize=14
dpi=300


data   = pickle.load(open(args.mcmc_trace_file, "r"))
P0     = data["P0"]
Ls     = data["Ls"]
DeltaH = data["DeltaH"]

DeltaG_mean   = data["DeltaG"].mean()
DeltaH_0_mean = data["DeltaH_0"].mean()

N = 23
V0 = 1.43 * 10**(-3)         #  liter
DeltaVn = [12.*10**(-6) for _ in range(N)]   #  liter

P0s = numpy.array([0.075, 0.080, 0.085, 0.090, 0.095, 0.100])

predicted_Ls     = linear_regression( P0, Ls )( P0s )
predicted_DeltaH = linear_regression( P0, DeltaH )( P0s )

plt.figure(figsize=figure_size)
plt.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
for p0, ls, dh in zip(P0s, predicted_Ls, predicted_DeltaH):
    qn = expected_injection_heats(V0, DeltaVn, p0, ls, DeltaG_mean, dh, DeltaH_0_mean, BETA, N)
    injection_indices = numpy.arange(N) + 1

    plt.plot(injection_indices, qn, linestyle="-", marker="o", ms=3, lw=lw)

plt.xlabel("$n$", fontsize=fontsize, **font)
plt.ylabel("$q^*_n$ (cal)", fontsize=fontsize, **font)
legends = ["%0.3f"%p0 for p0 in P0s]
plt.legend(legends, loc='lower right', fancybox=False, fontsize=8)
plt.tight_layout()
plt.savefig(args.out)

