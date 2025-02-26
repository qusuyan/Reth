#! /usr/bin/python

import sys

import pandas as pd
from matplotlib import pyplot as plt

width=0.5
colors = {'CursorAppend': 'tab:blue', 'CursorAppendDuplicates': 'cornflowerblue', 'CursorDeleteCurrent': 'tab:orange',
          'CursorFirst': 'tab:green', 'CursorInsert': 'tab:red', 'CursorLast': 'tab:olive', 'CursorNext': 'aquamarine', 
          'CursorPrev': 'tab:gray', 'CursorSeek': 'seagreen', 'CursorSeekExact': 'tab:cyan', 
          'CursorUpsert': 'tab:purple', 'Get': 'skyblue', 'Put': 'tab:pink'}

csv = sys.argv[1]
out_dir = sys.argv[2]
df = pd.read_csv(csv)


fig, ax = plt.subplots()
bottom = {}
for (op, count_df) in df.groupby("op"):
    total_count = count_df.groupby('table')['count'].sum().reset_index()
    plt_bottom = [bottom.get(table, 0) for table in total_count['table']]
    plt.bar(total_count['table'], total_count['count'], width=width, label=op, bottom=plt_bottom, color=colors[op])
    for (idx, row) in total_count.iterrows():
        table = row["table"]
        bottom[table] = plt_bottom[idx] + row["count"]

# ax.set_yscale('log')
ax.legend(loc=(1.02, 0.1), prop={'size': 8})
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.subplots_adjust(left=0.08, bottom=0.42, right=0.7, top=0.95)
fig.savefig(f"{out_dir}/out.pdf", format="pdf")

ax.set_yscale('log')
fig.savefig(f"{out_dir}/out_log.pdf", format="pdf")
plt.close(fig=fig)

for (table_name, table_df) in df.groupby('table'):
    fig, ax = plt.subplots()
    chart_color = [colors[op] for op in table_df['op']]
    ax.pie(table_df['count'], labels=table_df['op'], colors=chart_color)
    # for (op, count_df) in table_df.groupby("op"):
    #     total_count = count_df['count'].sum()
    #     plt.bar(op, total_count, width=width)
    # ax.set_ylim(bottom=0)
    # ax.set_yscale('log')
    # ax.set_xticks(ax.get_xticks())
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    # plt.subplots_adjust(left=0.2, bottom=0.3, right=0.99, top=0.99)
    ax.legend(loc=(-0.3,0))
    fig.savefig(f"{out_dir}/{table_name}.pdf", format="pdf")
    plt.close(fig=fig)