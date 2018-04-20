
"""
contains functions that compute Gaussian CIs and Bayesian credible intervals
"""

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

import pymc


def gaussian_ci_from_sample(sample, level, bootstrap_repeats=1000):
    """
    sample  :   np.ndarray,  float, shape = (nsamples,)
    level   :   float, 0 < level < 1
    bootstrap_repeats   : int, number of bootstrap repeats to estimate standard errors for 
                                lower and upper 

    return  (lower, upper, lower_error, upper_error)
            lower   :   float, lower bound of the interval
            upper   :   float, upper bound of the interval
            lower_error   : float, bootstrap standard error of lower
            upper_error   : float, bootstrap standard error of upper
    """
    assert sample.ndim == 1, "sample must be 1D ndarray"
    assert  0. < level < 1., "level must be 0 < level < 1"
    
    level *= 100
    l_percentile = (100. - level) / 2
    u_percentile = 100. - l_percentile

    lower = np.percentile(sample, l_percentile)
    upper = np.percentile(sample, u_percentile)

    lower_error = np.std( [ np.percentile( np.random.choice(sample, size=sample.shape[0], replace=True), l_percentile ) 
                            for _ in range(bootstrap_repeats) ] )

    upper_error = np.std( [ np.percentile( np.random.choice(sample, size=sample.shape[0], replace=True), u_percentile ) 
                            for _ in range(bootstrap_repeats) ] )

    return (lower, upper, lower_error, upper_error)



def gaussian_ci_from_mean_std(mean, std, level):
    """
    mean    : float
    std     : float
    level   :   float, 0 < level < 1

    return  (lower, upper)
            lower   :   float, lower bound of the interval
            upper   :   float, upper bound of the interval
    """
    assert  0. < level < 1., "level must be 0 < level < 1"
    lower, upper = scipy.stats.norm.interval(level, loc=mean, scale=std)
    return (lower, upper)


def bayesian_credible_interval(sample, level, bootstrap_repeats=1000):
    """
    sample  :   np.ndarray,  float, shape = (nsamples,)
    level   :   float, 0 < level < 1
    bootstrap_repeats   : int, number of bootstrap repeats to estimate standard errors for 
                                lower and upper 

    return  (lower, upper, lower_error, upper_error)
            lower   :   float, lower bound of the interval
            upper   :   float, upper bound of the interval
            lower_error   : float, bootstrap standard error of lower
            upper_error   : float, bootstrap standard error of upper
    """
    assert  0. < level < 1., "level must be 0 < level < 1"

    alpha = 1. - level
    lower, upper = pymc.utils.hpd(sample, alpha)

    lowers = []
    uppers = []
    for _ in range(bootstrap_repeats):
        l, u = pymc.utils.hpd( np.random.choice(sample, size=sample.shape[0], replace=True), alpha )
        lowers.append(l)
        uppers.append(u)

    lower_error = np.std(lowers) 
    upper_error = np.std(uppers)

    return (lower, upper, lower_error, upper_error) 


def _contains_or_not(lower, upper, test_val):
    """
    lower   :   float
    upper   :   float
    test_val    :   float
    """
    assert lower < upper, "lower must be less than upper"
    return lower <= test_val <= upper


def _containing_rate(lowers, uppers, test_val):
    """
    lowers  :   list of floats
    uppers  :   list of floats
    test_val    : float

    retrurn 
            rate, float, rate of contaiing test_value
    """
    assert len(lowers) == len(uppers)
    rate = np.mean( [ _contains_or_not(lower, upper, test_val) for lower, upper in zip(lowers, uppers) ] )
    return rate


def rate_of_containing_from_means_stds(means, stds, level, estimate_of_true="median"):
    """
    means   :   list of float
    stds    :   list of float
    level   :   float, 0 < level < 1

    return 
            rate    : float
    """
    assert estimate_of_true in ["mean", "median"], "estimate_of_true must be either 'mean' or 'median'"
    
    lowers = []
    uppers = []

    for mu, sigma in zip(means, stds):
        l, u = gaussian_ci_from_mean_std(mu, sigma, level) 
        lowers.append(l)
        uppers.append(u)

    if estimate_of_true == "median":
        true_val = np.median(means)
    elif estimate_of_true == "mean":
        true_val = np.mean(means)

    rate = _containing_rate(lowers, uppers, true_val)
    return rate


def rate_of_containing_from_sample(samples, level, estimate_of_true="median", ci_type="bayesian", bootstrap_repeats=100):
    """
    samples :   list of 1d np.ndarray
    level   :   float, 0 < level < 1
    estimate_of_true    :   str
    ci_type             :   str
    bootstrap_repeats   :   int

    return  (rate, rate_error)
            rate        :   float
            rate_error    :   float
    """
    assert estimate_of_true in ["mean", "median"], "estimate_of_true must be either 'mean' or 'median'"
    assert ci_type in ["bayesian", "gaussian"], "ci_type must be either 'bayesian' or 'gaussian'"

    lowers = []
    uppers = []
    for sample in samples:

        if ci_type == "gaussian":
            lower, upper, _, _ = gaussian_ci_from_sample(sample, level, bootstrap_repeats=1)

        elif ci_type == "bayesian":
            lower, upper, _, _ = bayesian_credible_interval(sample, level, bootstrap_repeats=1)

        lowers.append(lower)
        uppers.append(upper)

    if estimate_of_true == "median":
        true_val = np.median( [np.median(sample) for sample in samples] )

    elif estimate_of_true == "mean":
        true_val = np.mean( [np.mean(sample) for sample in samples] )

    rate = _containing_rate(lowers, uppers, true_val)

    # bootstraping
    rates = []
    for _ in range(bootstrap_repeats):

        lowers = []
        uppers = []

        for sample in samples:

            rand_sample = np.random.choice(sample, size=sample.shape[0], replace=True)

            if ci_type == "gaussian":
                lower, upper, _, _ = gaussian_ci_from_sample(rand_sample, level, bootstrap_repeats=1)

            elif ci_type == "bayesian":
                lower, upper, _, _ = bayesian_credible_interval(rand_sample, level, bootstrap_repeats=1)

            lowers.append(lower)
            uppers.append(upper)

        rates.append( _containing_rate(lowers, uppers, true_val) )

    rate_error = np.std(rates)

    return (rate, rate_error)


def ci_convergence(repeated_samples, list_of_stops, level, ci_type="bayesian"):
    """
    repeated_samples    :   list of 1d ndarray
    list_of_stops       :   array of int
    level               : float 0 < level < 1
    ci_type             : str, must be either "bayesian" or "gaussian"

    return (lowers, uppers)
            lowers  :   ndarray of shape = ( len(repeated_samples), len(list_of_stops) )
            uppers  :   ndarray of shape = ( len(repeated_samples), len(list_of_stops) )
    """
    assert ci_type in ["bayesian", "gaussian"], "ci_type must be either 'bayesian' or 'gaussian'"
    assert isinstance(list_of_stops, (list, np.ndarray)), "list_of_stops must be a list or ndarray"
    assert isinstance(repeated_samples, list), "repeated_samples must be a list"
    for sample in repeated_samples:
        assert sample.ndim == 1, "sample must be 1d ndarray"

    lowers = np.zeros([len(repeated_samples), len(list_of_stops)], dtype=float)
    uppers = np.zeros([len(repeated_samples), len(list_of_stops)], dtype=float)

    for i, sample in enumerate(repeated_samples):
        for j, stop in enumerate(list_of_stops):

            sub_sample = sample[0:stop]

            if ci_type == "bayesian":
                l, u, _, _ = bayesian_credible_interval(sub_sample, level, bootstrap_repeats=1)
            elif ci_type == "gaussian":
                l, u, _, _ = gaussian_ci_from_sample(sub_sample, level, bootstrap_repeats=1)

            lowers[i, j] = l
            uppers[i, j] = u
    return lowers, uppers


def plot_vertically_stacked_cis(  lowers, uppers, xlabel, out,
                                    lower_errors=None, 
                                    upper_errors=None,
                                    centrals=None,

                                    xlimits=None,
                                    nticks=6,

                                    main_lw=2.0,
                                    error_lw=4.0,
                                    central_lw=1.5,

                                    main_color="k",
                                    error_color="r",
                                    central_color="g",

                                    fontsize=8,
                                    figure_size=(3.2, 2.4),
                                    dpi=300,
                                    font = {"fontname": "Arial"}
                                    ):
    """
    lowers  :   array-like, float
    uppers  :   array-like, float
    xlabel  :   str
    out     :   str
    lower_stds  :   None or array-like of floats
    upper_stds  :   None or array-like of floats
    centrals    :   None or list of floats
    xlimits     :   None or [float, float]
    """
    assert len(lowers) == len(uppers), "lowers and uppers must have the same len"
    if (lower_errors is not None) and (upper_errors is not None):
        assert len(lower_errors) == len(upper_errors) == len(lowers), "lowers, lower_errors and upper_errors must have the same len"

    plt.figure(figsize=figure_size)

    xs = zip(lowers, uppers)
    ys = [ [i, i] for i in range(len(lowers)) ]

    for i in range(len(xs)):
        plt.plot(xs[i], ys[i], linestyle="-", color=main_color, lw=main_lw)

    if (lower_errors is not None) and (upper_errors is not None):
        l_err_bars = [ [val - err, val + err] for val, err in zip(lowers, lower_errors) ]
        u_err_bars = [ [val - err, val + err] for val, err in zip(uppers, upper_errors) ]

        for i in range( len(l_err_bars) ):
            plt.plot(l_err_bars[i], ys[i], linestyle="-", color=error_color, lw=error_lw)
            plt.plot(u_err_bars[i], ys[i], linestyle="-", color=error_color, lw=error_lw)

    if centrals is not None:
        y_min = np.min(ys)
        y_max = np.max(ys)

        for central in centrals:
            plt.plot([central, central], [y_min, y_max], linestyle="-", color=central_color, lw=central_lw)

    ax = plt.axes()
    ax.locator_params(axis='x', nbins=nticks)

    lower_y = np.min(ys) - 1
    upper_y = np.max(ys) + 1
    ax.set_ylim([lower_y, upper_y])

    if xlimits is not None:
        ax.set_xlim([xlimits[0], xlimits[1]])

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    ax.get_yaxis().set_visible(False)
    plt.xlabel(xlabel, fontsize=fontsize, **font)
    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None


def plot_containing_rates(predicted_rates, observed_rates, out, 
                            observed_rate_errors=None,
                            show_diagonal_line=True,
                            
                            xlabel="predicted",
                            ylabel="observed",
                            xlimits=[0, 100],
                            ylimits=[0, 100],
                            nticks=6,

                            colors=None,
                            markers=None,
                            markersize=5,

                            diagonal_line_style="-",
                            diagonal_line_w=1.,
                            diagonal_line_c="k",

                            aspect="equal",
                            figure_size=(3.2, 3.2),
                            dpi=300,
                            fontsize=8,
                            font = {"fontname": "Arial"}
                            ):
    """
    """
    assert isinstance(predicted_rates, list), "predicted_rates must be a list"
    assert isinstance(observed_rates, list), "predicted_rates must be a list"

    assert len(predicted_rates) == len(observed_rates), "predicted_rates and observed_rates do not have the same len"

    if observed_rate_errors is not None:
        assert len(observed_rates) == len(observed_rate_errors), "observed_rates and observed_rate_errors do not have the same len"
    else:
        observed_rate_errors = [[None for _ in line] for line in predicted_rates]

    if colors is None:
        colors = ["k" for _ in range(len(predicted_rates))]

    if markers is None:
        markers = ["o" for _ in range(len(predicted_rates))]

    plt.figure(figsize=figure_size)
    ax = plt.axes()

    for i in range(len(predicted_rates)):
        for j in range( len(predicted_rates[i]) ):
            plt.errorbar( predicted_rates[i][j], observed_rates[i][j], yerr=observed_rate_errors[i][j], marker=markers[i],
                          ms=markersize, c=colors[i], linestyle="None")

    if show_diagonal_line:
        plt.plot( xlimits, ylimits, linestyle=diagonal_line_style, lw=diagonal_line_w, color=diagonal_line_c )

    ax.set_xlim(xlimits)
    ax.set_ylim(ylimits)

    plt.axis(aspect=aspect)

    ax.locator_params(axis='x', nbins=nticks)
    ax.locator_params(axis='y', nbins=nticks)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    plt.xlabel(xlabel, fontsize=fontsize, **font)
    plt.ylabel(ylabel, fontsize=fontsize, **font)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    
    return None


def plot_ci_convergence(lowers, uppers, list_of_stops, xlabel, ylabel, out, 
                        xlimits=None,
                        ylimits=None,

                        repeats_linestyle="-",
                        mean_linestyle="-",
                        repeats_lw=0.8,
                        mean_lw=1.0,
                        
                        repeats_colors=None,
                        repeats_alpha=1.0,
                        mean_color=None,
                        mean_alpha=1.0,

                        x_nticks=6,
                        y_nticks=10,
                        figure_size=(3.2, 2.4),
                        dpi=300,
                        fontsize=8,
                        font = {"fontname": "Arial"}
                        ):
    """
    lowers  :   ndarray of shape = ( n_repeated_samples, n_stops )
    uppers  :   ndarray of shape = ( n_repeated_samples, n_stops )
    """
    assert lowers.shape == uppers.shape, "lowers and uppers must have the same shape"
    assert lowers.ndim == 2, "lowers must be 2d array"
    assert lowers.shape[-1] == len(list_of_stops), "lowers.shape[-1] must be the same as len(list_of_stops)"

    list_of_stops = np.asarray(list_of_stops)

    plt.figure(figsize=figure_size)
    ax = plt.axes()

    nrepeats = lowers.shape[0]

    if repeats_colors is None:
        repeats_colors = ["k" for _ in range(nrepeats)]

    if mean_color is None:
        mean_color = "r"

    for repeat in range(nrepeats):
        plt.plot(list_of_stops, lowers[repeat], linestyle=repeats_linestyle, color=repeats_colors[repeat], lw=repeats_lw, alpha=repeats_alpha)
        plt.plot(list_of_stops, uppers[repeat], linestyle=repeats_linestyle, color=repeats_colors[repeat], lw=repeats_lw, alpha=repeats_alpha)

    lower_mean  = lowers.mean(axis=0)
    lower_error = lowers.std(axis=0)

    upper_mean  = uppers.mean(axis=0)
    upper_error = uppers.std(axis=0)

    # error bars to be one standard error
    lower_error /= 2.
    upper_error /= 2.

    plt.errorbar(list_of_stops, lower_mean, yerr=lower_error, linestyle=mean_linestyle, color=mean_color, lw=mean_lw, alpha=mean_alpha)
    plt.errorbar(list_of_stops, upper_mean, yerr=upper_error, linestyle=mean_linestyle, color=mean_color, lw=mean_lw, alpha=mean_alpha)

    if xlimits is not None:
        ax.set_xlim(xlimits)

    if ylimits is not None:
        ax.set_ylim(ylimits)

    ax.locator_params(axis='x', nbins=x_nticks)
    ax.locator_params(axis='y', nbins=y_nticks)
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontsize)

    plt.xlabel(xlabel, fontsize=fontsize, **font)
    plt.ylabel(ylabel, fontsize=fontsize, **font)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)

    return None


