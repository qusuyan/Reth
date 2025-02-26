#! /usr/bin/python

import sys

import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.stats

colors = {'CursorAppend': 'tab:blue', 'CursorAppendDuplicates': 'cornflowerblue', 'CursorDeleteCurrent': 'tab:orange',
          'CursorFirst': 'tab:green', 'CursorInsert': 'tab:red', 'CursorLast': 'tab:olive', 'CursorNext': 'aquamarine', 
          'CursorPrev': 'tab:gray', 'CursorSeek': 'seagreen', 'CursorSeekExact': 'tab:cyan', 
          'CursorUpsert': 'tab:purple', 'Get': 'skyblue', 'Put': 'tab:pink'}

csv = sys.argv[1]
out_dir = sys.argv[2]
df = pd.read_csv(csv)

max = df["count"].max()
max_bin = math.ceil(max / 100) * 100
# num_bins = 100
# bin_size = max_bin / num_bins
# bins = np.arange(0, max_bin + bin_size, bin_size)
# print(bins)
ticks = (1, 5, 20, 50, 200, 1000, 10000, 100000, 2000000)

for ((table_name,), table_df) in df.groupby(["table"]):
    fig, ax = plt.subplots()
    marker_sz=5
    for ((op,), count_df) in table_df.groupby(["op"]):
        print(table_name, op)
        counts = count_df["count"]
        # counts = pd.concat([counts, pd.Series([max_bin + 1])])
        # ax.hist(counts, bins=bins, cumulative=True, histtype='step', label=op)
        ecdf = scipy.stats.ecdf(counts).cdf
        quantiles = np.concatenate(([-1.0,], np.log(ecdf.quantiles), np.log([2*max_bin,])))
        probabilities = np.concatenate(([0.0], ecdf.probabilities, [1.0]))
        ax.step(quantiles, probabilities * len(probabilities), where="post", label=op, color=colors[op], marker='o', markersize=marker_sz, zorder=999-marker_sz)
        marker_sz += 1.5
    ax.legend()
    ax.set_xticks(np.log(ticks))
    ax.set_xticklabels(ticks)
    ax.set_xlim(0, np.log(max_bin))
    ax.set_xlabel("# Times the Key Accessed")
    ax.set_ylabel("Cumulative Count")
    fig.savefig(f"{out_dir}/{table_name}.pdf", format="pdf")
    plt.close(fig=fig)
    
