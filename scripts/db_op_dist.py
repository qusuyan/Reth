#! /usr/bin/python

import os, sys
from multiprocessing import Pool

import pandas as pd

def get_file_dist(file):
    df = pd.read_csv(file)
    return df.groupby(["table", "op"]).size()

csv_dir = sys.argv[1]
out_csv = sys.argv[2]

dfs = []
with Pool(processes=40) as pool:
    results = []
    for csv_file in os.listdir(csv_dir):
        csv_path = os.path.join(csv_dir, csv_file)
        p = pool.apply_async(get_file_dist, (csv_path,))
        results.append(p)

    for p in results:
        dfs.append(p.get())

df = pd.concat(dfs)
df = df.groupby(["table", "op"]).sum().reset_index(name ='count')
df = df.sort_values(['table', 'count'])

df.to_csv(out_csv)
print(df.to_string())
