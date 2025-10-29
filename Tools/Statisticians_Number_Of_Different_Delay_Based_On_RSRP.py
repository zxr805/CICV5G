"""
Copyright (c) 2025 Tongji University

This file is part of 5G V2N2V Dataset.

rsrp_delay_analysis.py
Automated analysis of RSRP vs delay statistics across multiple text input files.

Usage examples:
  # analyze specific files and write Excel
  python rsrp_delay_analysis.py --inputs v2v_info01.txt v2v_info02.txt v2v_info03.txt --output rsrp_delay.xlsx

  # analyze all txt files in a folder and write CSV
  python rsrp_delay_analysis.py --input-folder data/ --pattern "*.txt" --output rsrp_delay.csv --out-format csv

  # change column indices (zero-based), e.g., delay in col 2, rsrp in col 9 (default)
  python rsrp_delay_analysis.py --inputs file1.txt --delay-col 2 --rsrp-col 9

Notes:
- Default behavior skips the first line of each file (assumed header). Use --skip-rows 0 to disable.
- The script is robust to malformed lines and will skip rows that cannot be parsed.
- Requires: xlsxwriter (only if writing xlsx). Install via `pip install xlsxwriter`.
"""

import argparse
import glob
import os
import sys
from collections import OrderedDict

def parse_args():
    p = argparse.ArgumentParser(description="RSRP vs Delay summary across text files.")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--inputs", nargs="+", help="List of input text files to process.")
    group.add_argument("--input-folder", help="Folder containing input files to process (use with --pattern).")
    p.add_argument("--pattern", default="*.txt", help="Glob pattern when using --input-folder (default '*.txt').")
    p.add_argument("--output", default="rsrp_delay.xlsx", help="Output file path (xlsx or csv).")
    p.add_argument("--out-format", choices=["xlsx", "csv"], help="Force output format (derived from --output if omitted).")
    p.add_argument("--delay-col", type=int, default=2, help="Zero-based column index for delay (default 2).")
    p.add_argument("--rsrp-col", type=int, default=9, help="Zero-based column index for RSRP (default 9).")
    p.add_argument("--skip-rows", type=int, default=1, help="Number of header lines to skip per file (default 1).")
    p.add_argument("--quiet", action="store_true", help="Suppress progress messages.")
    return p.parse_args()

def collect_files(args):
    files = []
    if args.inputs:
        for f in args.inputs:
            if os.path.isfile(f):
                files.append(f)
            else:
                print(f"Warning: input file not found: {f}", file=sys.stderr)
    else:
        # folder + pattern
        pattern = os.path.join(args.input_folder, args.pattern)
        files = sorted(glob.glob(pattern))
        if not files:
            print(f"No files matched pattern: {pattern}", file=sys.stderr)
    return files

def bucket_rsrp(rsrp_value):
    # returns key string for given rsrp numeric value
    if rsrp_value > -75:
        return "-75"
    elif rsrp_value > -85:
        return "-85"
    elif rsrp_value > -90:
        return "-90"
    elif rsrp_value > -95:
        return "-95"
    else:
        return "<-95"

def process_files(files, delay_col, rsrp_col, skip_rows=1, quiet=False):
    # Ordered keys to preserve output order
    rsrp_ranges = OrderedDict([("-75",[0,0,0]),("-85",[0,0,0]),("-90",[0,0,0]),("-95",[0,0,0]),("<-95",[0,0,0])])
    total_count = 0
    processed_files = 0

    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                # skip header lines
                for _ in range(skip_rows):
                    next(fh, None)
                for line in fh:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    # Ensure enough columns
                    if len(parts) <= max(delay_col, rsrp_col):
                        continue
                    try:
                        delay = float(parts[delay_col])
                        rsrp = float(parts[rsrp_col])
                    except Exception:
                        # Unable to parse numeric values; skip row
                        continue

                    total_count += 1
                    key = bucket_rsrp(rsrp)
                    # increment total rsrp count
                    rsrp_ranges[key][2] += 1
                    # categorize delay
                    if delay > 100:
                        rsrp_ranges[key][0] += 1
                    elif 50 <= delay <= 100:
                        rsrp_ranges[key][1] += 1
            processed_files += 1
            if not quiet:
                print(f"Processed {fpath}")
        except Exception as e:
            print(f"Error reading {fpath}: {e}", file=sys.stderr)

    return rsrp_ranges, total_count, processed_files

def write_output_xlsx(outfile, rsrp_ranges, total_count):
    import xlsxwriter
    workbook = xlsxwriter.Workbook(outfile)
    worksheet = workbook.add_worksheet("rsrp_delay_summary")
    headers = ['rsrp_bucket','delay>100_count','50<=delay<=100_count','total_rsrp_count','percent_delay>100','percent_50<=delay<=100','total_count']
    for col, h in enumerate(headers):
        worksheet.write(0, col, h)
    row = 1
    for key, value in rsrp_ranges.items():
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, value[0])
        worksheet.write(row, 2, value[1])
        worksheet.write(row, 3, value[2])
        pct1 = (value[0]/total_count*100) if total_count>0 else 0.0
        pct2 = (value[1]/total_count*100) if total_count>0 else 0.0
        worksheet.write(row, 4, pct1)
        worksheet.write(row, 5, pct2)
        worksheet.write(row, 6, total_count)
        row += 1
    workbook.close()

def write_output_csv(outfile, rsrp_ranges, total_count):
    import csv
    with open(outfile, "w", newline="", encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['rsrp_bucket','delay>100_count','50<=delay<=100_count','total_rsrp_count','percent_delay>100','percent_50<=delay<=100','total_count'])
        for key, value in rsrp_ranges.items():
            pct1 = (value[0]/total_count*100) if total_count>0 else 0.0
            pct2 = (value[1]/total_count*100) if total_count>0 else 0.0
            writer.writerow([key, value[0], value[1], value[2], pct1, pct2, total_count])

def print_summary(rsrp_ranges, total_count, processed_files):
    print("\nSummary:")
    print(f"Files processed: {processed_files}, Total records analysed: {total_count}\n")
    for key, value in rsrp_ranges.items():
        pct1 = (value[0]/total_count*100) if total_count>0 else 0.0
        pct2 = (value[1]/total_count*100) if total_count>0 else 0.0
        print(f"RSRP bucket {key}: delay>100: {value[0]}, 50<=delay<=100: {value[1]}, total: {value[2]}, pct_delay>100: {pct1:.3f}%, pct_50-100: {pct2:.3f}%")

def main():
    args = parse_args()
    # determine output format
    if args.out_format:
        outfmt = args.out_format
    else:
        _, ext = os.path.splitext(args.output)
        outfmt = "xlsx" if ext.lower() in [".xlsx",".xls"] else "csv"

    files = collect_files(args)
    if not files:
        print("No input files found. Exiting.", file=sys.stderr)
        sys.exit(2)

    rsrp_ranges, total_count, processed_files = process_files(files, args.delay_col, args.rsrp_col, args.skip_rows, args.quiet)

    # ensure output directory exists
    outdir = os.path.dirname(os.path.abspath(args.output))
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    if outfmt == "xlsx":
        try:
            write_output_xlsx(args.output, rsrp_ranges, total_count)
            if not args.quiet:
                print(f"Wrote Excel output to {args.output}")
        except Exception as e:
            print(f"Failed to write XLSX output: {e}", file=sys.stderr)
            # fallback to csv
            csv_out = os.path.splitext(args.output)[0] + ".csv"
            write_output_csv(csv_out, rsrp_ranges, total_count)
            print(f"Wrote CSV fallback to {csv_out}")
    else:
        write_output_csv(args.output, rsrp_ranges, total_count)
        if not args.quiet:
            print(f"Wrote CSV output to {args.output}")

    if not args.quiet:
        print_summary(rsrp_ranges, total_count, processed_files)

if __name__ == "__main__":
    main()
