"""
run simulated heat
"""

import argparse

import matplotlib.pyplot as plt
import numpy
import pymc

parser = argparse.ArgumentParser()

parser.add_argument( "--true_DeltaG_kcal_per_mol",  type=float, default=-10)
parser.add_argument( "--true_DeltaH_kcal_per_mol",  type=float, default=-5)
parser.add_argument( "--true_DeltaH_0_micro_cal",   type=float, default=0.5)
parser.add_argument( "--sigma_micro_cal",           type=float, default=1.)

parser.add_argument( "--stated_Ls_mM",              type=float, default=1.)
parser.add_argument( "--stated_R0_mM",              type=float, default=0.1)
parser.add_argument( "--concentration_uncertainty", type=float, default=0.1)

parser.add_argument( "--cell_vol_mili_litter",              type=float, default=1.43)
parser.add_argument( "--injection_vol_micro_litter",        type=float, default=12.)

parser.add_argument( "--number_of_injections",        type=int, default=24)

parser.add_argument( "--number_of_sim_exper",        type=int, default=50)

parser.add_argument( "--name_suffix",        type=str, default="sim")

parser.add_argument( "--experimental_design_out",        type=str, default="experimental_desgin_parameters.dat")

parser.add_argument( "--sim_heat_out",        type=str, default="sim_heats.pdf")

args = parser.parse_args()


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


class _LogNormal(object):
    def __init__(self, name, stated_concentration, uncertainty_percent):
        """
        :param name: str
        :param stated_concentration: float, mM
        :param uncertainty: float, 0 < uncertainty < 1
        """
        m = stated_concentration
        uncertainty = stated_concentration * uncertainty_percent
        v = uncertainty ** 2
        model = pymc.Lognormal(name,
                              mu = numpy.log( m / numpy.sqrt(1 + ( v / (m**2) ) ) ),
                              tau = 1.0 / numpy.log( 1 + (v / (m**2)) ),
                              value = m)

        setattr(self, name, model)


def _run_mcmc(model, iter, burn, thin):
    mcmc = pymc.MCMC(model)
    mcmc.sample(iter=iter, burn=burn, thin=thin)
    #pymc.Matplot.plot(mcmc)
    traces = {}
    for s in mcmc.stochastics:
        traces[s.__name__] = s.trace(chain=None)
    return traces


def _sample_lognormal(name, stated_concentration, uncertainty_percent,
                     nsamples, burn=100, thin=100):
    model = _LogNormal(name, stated_concentration, uncertainty_percent)
    iter = nsamples * thin + burn
    traces = _run_mcmc(model, iter, burn, thin)
    return traces[name]


def _cal_2_kcal_per_mol_of_injectant(qn_cal, injection_vol_micro_litter, stated_Ls_mM):
    """
    """
    vol_in_liter = injection_vol_micro_litter * 10. ** (-6)
    concen_in_M = stated_Ls_mM * 10. ** (-3)
    number_of_mol = concen_in_M * vol_in_liter

    qn_kcal = qn_cal * 10**(-3)
    qn_kcal_per_mol_of_injectant = qn_kcal / number_of_mol
    return qn_kcal_per_mol_of_injectant


def _write_heat_to_csv(qn_cal, injection_vol_micro_litter, stated_Ls_mM, out):
    qn_kcal_per_mol_of_injectant = _cal_2_kcal_per_mol_of_injectant(qn_cal, injection_vol_micro_litter, stated_Ls_mM)
    with open(out, "w") as handle:
        for q in qn_kcal_per_mol_of_injectant:
            handle.write("%0.15f, %0.15f\n"%(0., q))
    return None


def _write_exper_design_file(number_of_sim_exper, device,
                             stated_Ls_mM, stated_R0_mM,
                             number_of_injections,
                             injection_vol_micro_litter,
                             out):
    """
    """
    # unimportant
    test_inj = 0.
    time_interval = 300
    stir_speed = 410

    out_str = "#   0               1                       2                           3                           4"
    out_str += "                   5                   6                   7                       8\n"
    out_str +="# index     Calorimeter     [CBS] (syringe) (mili M)    [CA II] (cell) (mili M)     "
    out_str += "micro L Test injection   No. of injections   micro L injected     Time interval(s)        Stir speed (rpm)\n"

    for i in range(number_of_sim_exper):
        out_str += "%5d %12s %23.5f %23.5f %25.5f %20d %25.5f %20d %20d\n" %(i, device, stated_Ls_mM, stated_R0_mM, test_inj,
                                                                             number_of_injections, injection_vol_micro_litter,
                                                                             time_interval, stir_speed)
    open(out, "w").write(out_str)
    return None


# -----
figure_size=(3.2, 2.4)
lw=1.0
font = {"fontname": "Arial"}
fontsize=14
dpi=300


TEMPERATURE = 298.15
KB = 0.0019872041      # in kcal/mol/K
BETA = 1 / TEMPERATURE / KB

V0_litter = args.cell_vol_mili_litter * 10**(-3)
DeltaVn_liiter = [args.injection_vol_micro_litter * 10**(-6) for _ in range(args.number_of_injections)]

P0s = _sample_lognormal("P0", args.stated_R0_mM, args.concentration_uncertainty, args.number_of_sim_exper)
Lss = _sample_lognormal("Ls", args.stated_Ls_mM, args.concentration_uncertainty, args.number_of_sim_exper)

true_DeltaH_0_cal = args.true_DeltaH_0_micro_cal * 10**(-6)
sigma_cal = args.sigma_micro_cal * 10**(-6)


plt.figure(figsize=figure_size)
plt.ticklabel_format(style="sci", axis="y", scilimits=(0,0))


for i in range(args.number_of_sim_exper):
    qn_cal = expected_injection_heats(V0_litter, DeltaVn_liiter, P0s[i], Lss[i],
                                  args.true_DeltaG_kcal_per_mol, args.true_DeltaH_kcal_per_mol,
                                  true_DeltaH_0_cal, BETA, args.number_of_injections)

    qn_cal = qn_cal + numpy.random.normal(loc=0., scale=sigma_cal, size=args.number_of_injections)

    out_file = "%d_"%i + args.name_suffix + ".csv"
    _write_heat_to_csv(qn_cal, args.injection_vol_micro_litter, args.stated_Ls_mM, out_file)

    injection_indices = numpy.arange(args.number_of_injections) + 1
    plt.plot(injection_indices, qn_cal, linestyle="-", marker=None, ms=3, lw=lw)

plt.xlabel("$n$", fontsize=fontsize, **font)
plt.ylabel("$q^*_n$ (cal)", fontsize=fontsize, **font)
plt.tight_layout()
plt.savefig(args.sim_heat_out)


_write_exper_design_file(args.number_of_sim_exper, args.name_suffix,
                         args.stated_Ls_mM, args.stated_R0_mM,
                         args.number_of_injections,
                         args.injection_vol_micro_litter,
                         args.experimental_design_out)