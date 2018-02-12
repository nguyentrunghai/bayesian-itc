

import os
import argparse
import pickle

import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
sns.set_style("white")

from _confidence_intervals import bayesian_credible_interval
from _data_files import cell_concentration


def _plot_1d_kde(x, out, 
                xlabel=None, ylabel=None, 
                den_color="r",
                horizontal_line=None,
                lw=1.5,
                
                marker_at=None,
                line_color="k",
                marker_color="k",
                markersize=8,
                marker="v",
                nticks=6):
    """
    """
    figure_size = (3.2, 2.4)
    dpi = 300
    fontsize = 8
    font = { "fontname": "Arial"}

    plt.figure(figsize=figure_size)
    ax = sns.kdeplot(x, shade=True, color=den_color)

    if horizontal_line is not None:
        x1, x2, y = horizontal_line
        ax.plot([x1, x2], [y, y], marker="|", markersize=markersize, color=line_color, lw=lw)

    if marker_at is not None:
        x1, y1 = marker_at
        ax.plot([x1], [y1], marker=marker, markersize=markersize, color=marker_color)

    ax.locator_params(axis="x", nbins=nticks)
    ax.locator_params(axis="y", nbins=nticks)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=fontsize, **font)

    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=fontsize, **font)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None


def _plot_2d_kde(x, y, out, xlabel=None, ylabel=None, zlabel=None, nticks=10):
    """
    """
    sns.set(font_scale=0.75)
    figure_size = (3.2, 2.4)
    dpi = 300
    fontsize = 8
    font = { "fontname": "Arial"}

    # for more colormaps see http://matplotlib.org/examples/color/colormaps_reference.html
    my_cmap = plt.get_cmap('hot')

    plt.figure(figsize=figure_size)
    ax = sns.kdeplot(x, y, shade=True, cbar=True, cmap=my_cmap, cbar_kws={"label":zlabel} )

    ax.locator_params(axis="x", nbins=nticks)
    ax.locator_params(axis="y", nbins=nticks)

    #for tick in ax.xaxis.get_major_ticks():
        #tick.label.set_fontsize(fontsize)

    #for tick in ax.yaxis.get_major_ticks():
        #tick.label.set_fontsize(fontsize)

    if xlabel is not None:
        #plt.xlabel(xlabel, fontsize=fontsize, **font)
        plt.xlabel(xlabel)

    if ylabel is not None:
        #plt.ylabel(ylabel, fontsize=fontsize, **font)
        plt.ylabel(ylabel)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None

def _extract_dg_dh_p0_ls(trace_file):
    """
    """
    data = pickle.load( open(trace_file, "r") )

    dg = data["DeltaG"]
    dh = data["DeltaH"]
    p0 = data["P0"]
    ls = data["Ls"]

    tds = dh - dg

    return (dg, dh, tds, p0, ls)


parser = argparse.ArgumentParser()
parser.add_argument( "--bitc_mcmc_dir",     type=str, default="bitc_mcmc")
parser.add_argument( "--itc_files_dir",     type=str, default="itc_origin_files")
parser.add_argument( "--experiment",        type=str, default=" " )
parser.add_argument( "--level",             type=float, default=0.95)
args = parser.parse_args()

TRACES_FILE = "traces.pickle"
YLABEL = "Probability density"

itc_file = os.path.join(args.itc_files_dir, args.experiment+".itc") 
print itc_file

trace_file = os.path.join(args.bitc_mcmc_dir, args.experiment, TRACES_FILE)
print trace_file

dg, dh, tds, p0, ls = _extract_dg_dh_p0_ls(trace_file)

# dg
lower_dg, upper_dg, _, _ = bayesian_credible_interval(dg, args.level, bootstrap_repeats=1)
out = args.experiment + "_1d_dg.pdf"

_plot_1d_kde( dg, out, xlabel="$\Delta G$ (kcal/mol)", ylabel=YLABEL, horizontal_line=[lower_dg, upper_dg, 3], marker_at=None )


# dh
lower_dh, upper_dh, _, _ = bayesian_credible_interval(dh, args.level, bootstrap_repeats=1)
out = args.experiment + "_1d_dh.pdf"

_plot_1d_kde(dh, out, xlabel="$\Delta H$ (kcal/mol)", ylabel=YLABEL, horizontal_line=[lower_dh, upper_dh, 1.5], marker_at=None )

# dh
lower_tds, upper_tds, _, _ = bayesian_credible_interval(tds, args.level, bootstrap_repeats=1)
out = args.experiment + "_1d_tds.pdf"

_plot_1d_kde(tds, out, xlabel="$T \Delta S$ (kcal/mol)", ylabel=YLABEL, horizontal_line=[lower_tds, upper_tds, 1.5], marker_at=None )

# p0
lower_p0, upper_p0, _, _ = bayesian_credible_interval(p0, args.level, bootstrap_repeats=1)
stated_value = cell_concentration(itc_file, is_dummy_itc_file=True) 
out = args.experiment + "_1d_p0.pdf"

_plot_1d_kde( p0, out, xlabel="$[R]_0$ (mM)", ylabel=YLABEL, horizontal_line=[lower_p0, upper_p0, 35], marker_at=[stated_value, 4] )



# 2d
# dg dh
out = args.experiment + "_2d_dg_dh.pdf"
_plot_2d_kde(dg, dh, out, xlabel="$\Delta G$ (kcal/mol)", ylabel="$\Delta H$ (kcal/mol)", zlabel="Probability density")

# dg tds
out = args.experiment + "_2d_dg_tds.pdf"
_plot_2d_kde(dg, tds, out, xlabel="$\Delta G$ (kcal/mol)", ylabel="$T \Delta S$ (kcal/mol)", zlabel="Probability density")

# dh tds
out = args.experiment + "_2d_dh_tds.pdf"
_plot_2d_kde(dh, tds, out, xlabel="$\Delta H$ (kcal/mol)", ylabel="$T \Delta S$ (kcal/mol)", zlabel="Probability density")

# p0 dh
out = args.experiment + "_2d_p0_dh.pdf"
_plot_2d_kde(p0, dh, out, xlabel="$[R]_0$ (mM)", ylabel="$\Delta H$ (kcal/mol)", zlabel="Probability density")


