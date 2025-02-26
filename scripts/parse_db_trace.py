#! /usr/bin/python

import os, sys
import re, datetime

from multiprocessing import Pool

# 2025-02-22T20:35:25.014414Z DEBUG reth_db::implementation::mdbx::cursor: Txn Ok(2571778) CursorSeek: Table=HashedAccounts Key=[22, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
db_trace_pattern = "(.*) DEBUG .* Txn Ok\((\d+)\) (.*)\n"

# def parse_datetime(ts):
#     return datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")

def parse_op(op):
    parsed = op.split(":")
    operation = parsed[0]
    if len(parsed) < 2:
        return (operation, {})
    params = parsed[1]
    pairs = params.strip().split(" ", 1)
    pairs = [pair.split("=") for pair in pairs]
    param_dict = {}
    for pair in pairs:
        if len(pair) < 2:
            continue
        else:
            cur_key = pair[0]
            for idx in range(1, len(pair)-1):
                split = pair[idx].rsplit(" ", 1)
                param_dict[cur_key] = split[0]
                cur_key = split[1]
            param_dict[cur_key] = pair[len(pair)-1]
    return (operation, param_dict)

def parse_db_trace(in_path, out_path): 
    with open(out_path, "w") as out_f:
        out_f.write("timestamp,txn_id,op,table,key\n")
        with open(in_path, "r") as in_f:
            for line in in_f:
                pattern = re.fullmatch(db_trace_pattern, line)
                if pattern is None:
                    continue
                (ts, txn_id, raw_op) = pattern.groups()
                (op, param_dict) = parse_op(raw_op)
                trace = (ts, txn_id, op, param_dict.get("Table"), param_dict.get("Key"))
                line = ",".join(['"' + item + '"' if item is not None else "" for item in trace]) + '\n'
                out_f.write(line)
    
log_dir = sys.argv[1]
out_dir = sys.argv[2]

with Pool(processes=40) as pool:
    results = []
    for log_file in os.listdir(log_dir):
        in_path = os.path.join(log_dir, log_file)
        out_path = os.path.join(out_dir, log_file + ".csv")
        p = pool.apply_async(parse_db_trace, (in_path, out_path))
        results.append(p)

    for p in results:
        p.wait()

