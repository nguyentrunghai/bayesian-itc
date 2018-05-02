
import copy
import numpy as np
from sklearn.neighbors import KernelDensity

import matplotlib.pyplot as plt
import seaborn as sns

def remove_outliers(x):
    assert x.ndim == 1, "x must be 1d ndarray"
    iqr = np.percentile(x, 75) - np.percentile(x, 25)
    std = iqr / 1.349 
    median = np.median(x)
    lower = median - 20.*std
    upper = median + 20.*std

    new_x = copy.deepcopy(x)

    for i in range(new_x.shape[0]):
        if new_x[i] < lower or new_x[i] > upper:
            print "outlier: z score = ", (new_x[i] - median)/std
            new_x[i] = np.random.normal(loc=median, scale=std)
    return new_x

def overal_min_max(list_of_samples):
    """
    list_of_samples     :   list of 1d ndarray
    return  overal_min, overal_max
    """
    assert isinstance(list_of_samples, list), "list_of_samples must be a list"
    for sample in list_of_samples:
        assert sample.ndim == 1, "samples in list_of_samples must be 1d ndarray"

    overal_min = np.min( [sample.min() for sample in list_of_samples] )
    overal_max = np.max( [sample.max() for sample in list_of_samples] )
    sdt = np.mean( [sample.std() for sample in list_of_samples] )
    extra = 0.01 * sdt

    overal_min -= extra
    overal_max += extra

    return overal_min, overal_max


# ERICA
# kernel based density propability
# xmin, xmax, ymin, ymax are the min and max of the x and y for the two compared samples
# bandwidth will be set to 0.03 at call of kde2D_PQ, as result of trial in the plots above
def kde2D_PQ(x, y, bandwidth, xmin, xmax, ymin, ymax, xbins=100j, ybins=100j, **kwargs):
    """ Build 2D kernel density estimate (KDE)."""

    # create grid of sample locations (default: xbins:100 x ybins:100)

    xx, yy = np.mgrid[xmin:xmax:xbins, ymin:ymax:ybins]

    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T

    kde_skl = KernelDensity(bandwidth=bandwidth, kernel='gaussian',**kwargs)
    kde_skl.fit(xy_train)

    #zl = kde_skl.score(xy_sample)
    # score_samples() returns the log-likelihood of the samples

    #z = np.exp(kde_skl.score_samples(xy_sample)/max(kde_skl.score_samples(xy_sample)))
    z = np.exp( kde_skl.score_samples(xy_sample) )

    bin_area = (xmax - xmin) * (ymax - ymin) / xbins.imag / ybins.imag

    #if (name1 == name2): plot_density(x, y, xx, yy, np.reshape(z, xx.shape), name1, bandwidth)
    #print "If the density is normalized, then its numerical integration is close to 1"
    #normalizing_const = numerically_integrate_density(bin_area, z)
    #print normalizing_const

    #z /= normalizing_const
    #print "after normalizing"
    #normalizing_const = numerically_integrate_density(bin_area, z)
    #print normalizing_const
    return bin_area, np.reshape(z, xx.shape)



def gaussian_kde_2d(x, y, xmin, xmax, ymin, ymax, bandwidth, xbins=20, ybins=20):
    """ Build 2D kernel density estimate (KDE)."""

    # xy_train with shape (nsamples, nfeatures)
    xy_train = np.hstack( [ x[:, np.newaxis], y[:, np.newaxis] ] )

    kde_skl = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
    kde_skl.fit(xy_train)

    # x moves along axis 1
    # y moves along axis 0
    x_grid, y_grid = np.meshgrid( np.linspace(xmin, xmax, xbins), np.linspace(ymin, ymax, ybins) )
    xy_sample = np.hstack( [ x_grid.ravel()[:, np.newaxis], y_grid.ravel()[:, np.newaxis] ] )

    density_grid = np.exp( kde_skl.score_samples(xy_sample) )
    density_grid = density_grid.reshape(x_grid.shape)

    return x_grid, y_grid, density_grid


def bin_area(x_grid, y_grid):
    """
    """
    x_bin_width = x_grid[0, 1] - x_grid[0, 0]
    y_bin_width = y_grid[1, 0] - y_grid[0, 0]
    return x_bin_width * y_bin_width 


def kullback_leibler_divergence(p, q, bin_area):
    assert p.shape == q.shape, "p and q must have the same shape"
    assert p.ndim == 2, "p must be 2d array"

    nx, ny = p.shape
    total = 0
    
    for i in range(nx):
        for j in range(ny):
            pc = p[i, j]
            qc = q[i, j]

            if(pc > 0 and qc > 0): 
                total += pc * (np.log(pc) - np.log(qc))

            elif(pc !=0 and qc == 0):
                total += pc * np.log(pc)

    return total * bin_area

def numerical_kl_div(bin_area, p, q):
    total = 0
    neg = 0                                                                                                                      
    for pr,qr in zip(p,q):
        for pc,qc in zip(pr,qr):
            if(pc > 0 and qc > 0): total += pc * (np.log(pc) - np.log(qc))
            elif(pc !=0 and qc == 0): total += pc * np.log(pc)
            #pc ==0 and qc != 0 = 0
            # pc ==0 and qc == 0 = 0
    return total * bin_area



def plot_pair_of_annotated_heatmap(data_1, data_2, out):
    """
    """
    figure_size=(6.4, 4.8)
    dpi=300
    sns.set(font_scale=0.70)

    vmin = np.min( [ data_1.min(),  data_2.min() ] )
    vmax = np.max( [ data_1.max(),  data_2.max() ] )

    fig, ax = plt.subplots(2,1, sharex=True, figsize=figure_size)
    my_cmap = plt.get_cmap('Reds')

    sns.heatmap(data_1, ax=ax[0], annot=True, fmt=".2f", linewidths=.5, cmap=my_cmap, xticklabels=False, yticklabels=False, vmin=vmin, vmax=vmax)
    sns.heatmap(data_2, ax=ax[1], annot=True, fmt=".2f", linewidths=.5, cmap=my_cmap, xticklabels=False, yticklabels=False, vmin=vmin, vmax=vmax)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None


def plot_triple_of_annotated_heatmap(data_1, data_2, data_3, out):
    """
    """
    figure_size=(6.4, 6.4)
    dpi=300
    sns.set(font_scale=0.70)

    vmin = np.min( [ data_1.min(),  data_2.min() ] )
    vmax = np.max( [ data_1.max(),  data_2.max() ] )

    fig, ax = plt.subplots(3,1, sharex=True, figsize=figure_size)
    my_cmap = plt.get_cmap('Reds')

    sns.heatmap(data_1, ax=ax[0], annot=True, fmt=".2f", linewidths=.5, cmap=my_cmap, xticklabels=False,
                yticklabels=False, vmin=vmin, vmax=vmax)

    sns.heatmap(data_2, ax=ax[1], annot=True, fmt=".2f", linewidths=.5, cmap=my_cmap, xticklabels=False,
                yticklabels=False, vmin=vmin, vmax=vmax)

    sns.heatmap(data_3, ax=ax[2], annot=True, fmt=".2f", linewidths=.5, cmap=my_cmap, xticklabels=False,
                yticklabels=False, vmin=vmin, vmax=vmax)

    plt.tight_layout()
    plt.savefig(out, dpi=dpi)
    return None

