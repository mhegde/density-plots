'''
Generates density scatter plots
Author: Mudra Hegde
Email: mhegde@broadinstitute.org
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, pearsonr
import argparse, matplotlib


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, help='Input file')
    parser.add_argument('--col1', type=str, help='x-axis values')
    parser.add_argument('--col2', type=str, help='y-axis values')
    return parser


def generate_figure(df, col1, col2):
    x = np.array(df.ix[:, col1])
    y = np.array(df.ix[:, col2])
    corr = np.round(pearsonr(x, y)[0],2)
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]
    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=20, edgecolor='')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_tick_params(bottom='on', top='off')
    ax.yaxis.set_tick_params(left='on', right='off')
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_linewidth(2.0)
    ax.spines['left'].set_position('zero')
    ax.spines['left'].set_linewidth(2.0)
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
    ]
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=1,linestyle='dashed',linewidth=2.0)
    ax.set_aspect('equal')
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel(args.col1, fontsize=18, labelpad=220)
    ax.set_ylabel(args.col2, fontsize=18, labelpad=220)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)
    ax.text(np.min(ax.get_xlim())+1,np.max(ax.get_ylim())-0.5,'r = '+str(corr))
    fig.savefig(col1+'_'+col2+'_'+'density_plot.pdf')
    return



if __name__ == '__main__':
    matplotlib.rc('pdf', fonttype=42)
    args = get_parser().parse_args()
    input_df = pd.read_table(args.input_file)
    input_df = input_df.dropna()
    col1 = args.col1
    col2 = args.col2
    generate_figure(input_df, col1, col2)