#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_delay_by_velocity.py

Draw boxplots of end-to-end delay grouped by vehicle velocity.

Features:
- Read multiple txt files (or folder with pattern) containing delay column.
- Either supply a list of velocities matching the input files, or auto-detect
  a velocity column inside files (common names: 'Velocity', 'velocity', 'speed').
- Optionally split velocities into two groups (low/high) using a threshold so
  they are drawn in different colors (mimics original split in your script).
- Plot boxplots for each velocity group, overlay mean points and a mean-line.
- Save figure to file.

Usage examples:
  # 1) Provide input files and matching velocities (order matters)
  python plot_delay_by_velocity.py \
    --inputs v2v_info-01.txt v2v_info-02.txt v2v_info-03.txt v2v_info-04.txt \
    --velocities 50 60 70 80 \
    --delay-name delay --out plot_delay.png --dpi 600

  # 2) Read all txt in a folder, auto-detect velocity column inside files
  python plot_delay_by_velocity.py --input-folder data/ --pattern "*.txt" \
    --delay-name delay --vel-col-name Velocity --out results/delay_by_vel.png

  # 3) Provide velocities but ask to split low/high by threshold 50
  python plot_delay_by_velocity.py --inputs f1.txt f2.txt ... --velocities 0 20 30 40 50 60 70 80 \
    --split-threshold 50 --out fig.png

Dependencies:
  pandas, numpy, matplotlib

Author: (refactored)
"""
import argparse
import glob
import os
import sys
from typing import List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Common candidate names for delay/velocity columns to try when user didn't specify
DEFAULT_DELAY_NAMES = ['delay', 'delay(ms)', 'delay_ms', 'rtt', 'RTT', 'Delay']
DEFAULT_VEL_NAMES = ['Velocity', 'velocity', 'speed', 'Speed', 'VEL']

def parse_args():
    p = argparse.ArgumentParser(description="Plot delay boxplots grouped by vehicle velocity.")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--inputs', nargs='+', help='List of input text files (in order).')
    group.add_argument('--input-folder', help='Folder containing input files to process (use with --pattern).')
    p.add_argument('--pattern', default='*.txt', help='Glob pattern for input-folder (default: *.txt)')
    p.add_argument('--velocities', nargs='+', type=float, help='List of velocities (one per input file).')
    p.add_argument('--vel-col-name', help="If provided, script will extract a velocity column from files (useful when files contain mixed velocities).")
    p.add_argument('--delay-name', help="Column name for delay (if missing, script will try common candidates).")
    p.add_argument('--delay-col', type=int, help='Zero-based column index for delay (fallback if name not found).')
    p.add_argument('--skip-rows', type=int, default=1, help='Header rows to skip when reading (default 1). If files have no header, set 0.')
    p.add_argument('--sep', default='ws', choices=['ws', ',', '\\t', ' '], help="Separator: 'ws' = whitespace (default).")
    p.add_argument('--out', default='delay_by_velocity.png', help='Output figure file path (png/jpg/pdf supported).')
    p.add_argument('--dpi', type=int, default=300, help='Figure DPI (default 300).')
    p.add_argument('--figsize', nargs=2, type=float, default=(9.0,6.0), help='Figure size in inches, two floats: width height (default 9 6).')
    p.add_argument('--split-threshold', type=float, default=None, help='If provided, split velocities into two groups: <threshold and >=threshold.')
    p.add_argument('--median-line', action='store_true', help='Plot median line instead of mean-line (default shows mean markers and connecting mean line).')
    p.add_argument('--quiet', action='store_true', help='Suppress console messages.')
    return p.parse_args()

def find_files_from_folder(folder: str, pattern: str) -> List[str]:
    pattern_path = os.path.join(folder, pattern)
    files = sorted(glob.glob(pattern_path))
    return files

def read_delay_from_file(path: str, delay_name: Optional[str], delay_col: Optional[int], sep: str, skip_rows: int):
    # Read with pandas trying robustness
    if sep == 'ws':
        read_kwargs = dict(delim_whitespace=True, engine='python')
    else:
        sep_actual = {'\\t':'\t'}.get(sep, sep)
        read_kwargs = dict(sep=sep_actual)

    try:
        df = pd.read_csv(path, header=0 if skip_rows>0 else None, skiprows=0 if skip_rows==0 else 0, encoding='utf-8', **read_kwargs)
    except Exception:
        # fallback: read whole file as whitespace-separated
        df = pd.read_csv(path, delim_whitespace=True, engine='python', header=0 if skip_rows>0 else None, encoding='utf-8')

    # If header rows to skip > 0, we consider that header is present; else header absent.
    # Determine delay column
    col_name = None
    if delay_name and delay_name in df.columns:
        col_name = delay_name
    else:
        # try default names
        for cand in DEFAULT_DELAY_NAMES:
            if cand in df.columns:
                col_name = cand
                break

    if col_name is not None:
        series = pd.to_numeric(df[col_name], errors='coerce')
    elif delay_col is not None:
        # use positional index
        try:
            series = pd.to_numeric(df.iloc[:, delay_col], errors='coerce')
        except Exception:
            raise ValueError(f"Cannot read delay from column index {delay_col} in file {path}")
    else:
        # as last resort, try first numeric column
        numeric_cols = [c for c in df.columns if pd.to_numeric(df[c], errors='coerce').notna().any()]
        if numeric_cols:
            series = pd.to_numeric(df[numeric_cols[0]], errors='coerce')
        else:
            raise ValueError(f"Could not detect a delay column in {path}; please pass --delay-name or --delay-col")

    # drop NaN
    series = series.dropna().astype(float)
    return series

def read_velocity_from_file(path: str, vel_col_name: Optional[str], sep: str, skip_rows: int):
    if not vel_col_name:
        return None
    if sep == 'ws':
        read_kwargs = dict(delim_whitespace=True, engine='python')
    else:
        sep_actual = {'\\t':'\t'}.get(sep, sep)
        read_kwargs = dict(sep=sep_actual)
    df = pd.read_csv(path, header=0 if skip_rows>0 else None, encoding='utf-8', **read_kwargs)
    if vel_col_name in df.columns:
        return pd.to_numeric(df[vel_col_name], errors='coerce').dropna().astype(float)
    else:
        return None

def prepare_data(input_files: List[str], args):
    # returns dict: {velocity_label: numpy array of delays}
    per_vel_data = {}
    if args.velocities:
        if len(args.velocities) != len(input_files):
            raise ValueError("Length of --velocities must equal number of input files")
        for fpath, vel in zip(input_files, args.velocities):
            delays = read_delay_from_file(fpath, args.delay_name, args.delay_col, args.sep, args.skip_rows)
            per_vel_data[str(int(vel))] = delays.values
    else:
        # try to auto-detect velocity column inside files if vel_col_name provided
        if args.vel_col_name:
            # aggregate rows grouped by velocity (could be multiple velocities per file)
            agg = {}
            for f in input_files:
                try:
                    vel_series = read_velocity_from_file(f, args.vel_col_name, args.sep, args.skip_rows)
                    delay_series = read_delay_from_file(f, args.delay_name, args.delay_col, args.sep, args.skip_rows)
                except Exception as e:
                    print(f"Warning reading {f}: {e}", file=sys.stderr)
                    continue
                if vel_series is None:
                    continue
                # align lengths if necessary
                minlen = min(len(vel_series), len(delay_series))
                vel_series = vel_series.iloc[:minlen]
                delay_series = delay_series.iloc[:minlen]
                for v, d in zip(vel_series.values, delay_series.values):
                    key = str(int(v)) if (pd.notna(v) and float(v).is_integer()) else str(round(float(v),2))
                    agg.setdefault(key, []).append(float(d))
            per_vel_data = {k: np.array(v) for k,v in agg.items()}
        else:
            # fallback: treat each file as one velocity group and label by filename
            for f in input_files:
                delays = read_delay_from_file(f, args.delay_name, args.delay_col, args.sep, args.skip_rows)
                label = os.path.splitext(os.path.basename(f))[0]
                per_vel_data[label] = delays.values
    return per_vel_data

def split_groups(per_vel_data: dict, threshold: Optional[float]):
    """
    If threshold is provided, keys that represent numeric velocities are split into
    low (<threshold) and high (>=threshold). Non-numeric keys remain in 'other'.
    Returns tuple (low_dict, high_dict, other_dict)
    """
    low, high, other = {}, {}, {}
    for k,v in per_vel_data.items():
        try:
            kv = float(k)
            if threshold is None:
                other[k] = v
            else:
                if kv < threshold:
                    low[k] = v
                else:
                    high[k] = v
        except Exception:
            other[k] = v
    return low, high, other

def make_boxplot(per_vel_data: dict, args):
    # sort keys numerically if possible
    def key_sort(k):
        try:
            return float(k)
        except Exception:
            return k
    keys_sorted = sorted(list(per_vel_data.keys()), key=key_sort)
    data_list = [per_vel_data[k] for k in keys_sorted]

    # arrange groups if split-threshold provided
    if args.split_threshold is not None:
        low, high, other = split_groups(per_vel_data, args.split_threshold)
        # order: low (sorted), high (sorted), then other (sorted)
        low_k = sorted(low.keys(), key=key_sort)
        high_k = sorted(high.keys(), key=key_sort)
        other_k = sorted(other.keys(), key=key_sort)
        ordered_keys = low_k + high_k + other_k
        data_list = [per_vel_data[k] for k in ordered_keys]
        colors = ['tab:blue']*len(low_k) + ['k']*len(high_k) + ['tab:gray']*len(other_k)
    else:
        ordered_keys = keys_sorted
        colors = ['tab:blue']*len(ordered_keys)

    positions = np.arange(1, len(ordered_keys)+1)
    fig, ax = plt.subplots(figsize=tuple(args.figsize))

    # create boxplot with patch_artist True to control colors
    bplots = ax.boxplot(data_list, positions=positions, patch_artist=True,
                        showmeans=False, meanline=False, sym='w.', widths=0.6)

    # apply colors and styles
    for patch, color in zip(bplots['boxes'], colors):
        patch.set(facecolor='white', edgecolor=color, linewidth=1.5)
    for whisker, color in zip(bplots['whiskers'][::2], colors*2):
        whisker.set(color=color, linewidth=1.0)
    for cap, color in zip(bplots['caps'][::2], colors*2):
        cap.set(color=color, linewidth=1.0)
    for median in bplots['medians']:
        median.set(color='red', linewidth=1.5)

    # compute mean or median and plot line
    mean_vals = []
    for arr in data_list:
        if args.median_line:
            val = float(np.median(arr)) if len(arr)>0 else np.nan
        else:
            val = float(np.mean(arr)) if len(arr)>0 else np.nan
        mean_vals.append(val)
    ax.plot(positions, mean_vals, marker='o', linestyle='-', color='r', linewidth=2.0, markersize=6)

    # xticks and labels
    ax.set_xticks(positions)
    ax.set_xticklabels(ordered_keys, fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.set_xlabel('Velocity (or group label)', fontsize=14)
    ax.set_ylabel('Delay (ms)', fontsize=14)
    ax.grid(False)

    plt.tight_layout()
    # save figure
    outpath = args.out
    outdir = os.path.dirname(outpath)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    plt.savefig(outpath, dpi=args.dpi)
    if not args.quiet:
        print(f"Saved figure to {outpath} (dpi={args.dpi})")
    plt.show()

def main():
    args = parse_args()

    # collect input files
    if args.inputs:
        input_files = args.inputs
    else:
        input_files = find_files_from_folder(args.input_folder, args.pattern)
        if not input_files:
            print("No input files found. Exiting.", file=sys.stderr)
            sys.exit(1)

    if not args.quiet:
        print("Input files:", input_files)

    per_vel_data = prepare_data(input_files, args)
    if not per_vel_data:
        print("No delay data extracted. Check column names and inputs.", file=sys.stderr)
        sys.exit(2)

    if not args.quiet:
        print("Prepared velocity groups:", list(per_vel_data.keys()))

    make_boxplot(per_vel_data, args)

if __name__ == '__main__':
    main()
