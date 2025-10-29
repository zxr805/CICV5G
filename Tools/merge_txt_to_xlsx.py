"""
merge_txt_to_xlsx.py

Scan a folder for all .txt files (matching a glob pattern), concatenate them
(skipping the header rows of subsequent files), and write a combined text file
and an Excel (.xlsx) workbook.

This script is robust to the common layout where each .txt has the same header
line (column names) on the first row. If your files do not have headers, use
--no-header to treat all files as raw columns.

Usage examples:
  # Basic: process all .txt files in the current folder, write all.txt and all.xlsx
  python merge_txt_to_xlsx.py --input-folder . --pattern "*.txt" --output-txt all.txt --output-xlsx all.xlsx

  # If files include a header row and you want to skip that header in subsequent files (default)
  python merge_txt_to_xlsx.py --input-folder data --output-txt combined.txt --output-xlsx combined.xlsx

Arguments:
  --input-folder   Folder to search for input files (required)
  --pattern        Glob pattern for input files (default "*.txt")
  --output-txt     Output combined text file (default: all.txt)
  --output-xlsx    Output Excel file (default: all.xlsx)
  --skip-rows      Number of header rows to skip in subsequent files (default: 1)
  --no-header      Treat input files as not having a header row (all files are data rows)
  --sep            Column separator for reading txt files. Use 'ws' for whitespace (default).
  --encoding       File encoding (default 'utf-8')
  --engine-xlsx    Excel writer engine (default 'xlsxwriter')
"""

import argparse
import glob
import os
import sys

try:
    import pandas as pd
except Exception as e:
    print("Error: pandas is required. Install with `pip install pandas`.", file=sys.stderr)
    raise

def parse_args():
    p = argparse.ArgumentParser(description="Merge txt files in folder and export to TXT/Excel")
    p.add_argument("--input-folder", required=True, help="Folder containing input text files")
    p.add_argument("--pattern", default="*.txt", help="Glob pattern for input files (default '*.txt')")
    p.add_argument("--output-txt", default="all.txt", help="Combined output text file path")
    p.add_argument("--output-xlsx", default="all.xlsx", help="Output Excel (.xlsx) file path")
    p.add_argument("--skip-rows", type=int, default=1, help="Number of header rows to skip in subsequent files (default 1)")
    p.add_argument("--no-header", action="store_true", help="Treat files as not having a header row")
    p.add_argument("--sep", default="ws", choices=["ws", ",", "\\t", " "], help="Separator: 'ws' = whitespace (default), ',', '\\t', or ' '")
    p.add_argument("--encoding", default="utf-8", help="File encoding (default utf-8)")
    p.add_argument("--engine-xlsx", default="xlsxwriter", help="Excel writer engine for pandas (default xlsxwriter)")
    return p.parse_args()

def find_files(folder, pattern):
    pattern_path = os.path.join(folder, pattern)
    files = sorted(glob.glob(pattern_path))
    return files

def read_first_file(filepath, sep, encoding, header_present):
    if sep == "ws":
        df = pd.read_csv(filepath, delim_whitespace=True, header=0 if header_present else None, encoding=encoding, engine='python')
    else:
        sep_actual = {"\\t":"\t"}.get(sep, sep)
        df = pd.read_csv(filepath, sep=sep_actual, header=0 if header_present else None, encoding=encoding)
    return df

def read_file_as_df(filepath, sep, encoding, names=None, skiprows=0):
    if sep == "ws":
        df = pd.read_csv(filepath, delim_whitespace=True, header=None if names is not None else 0, names=names, skiprows=skiprows, encoding=encoding, engine='python')
    else:
        sep_actual = {"\\t":"\t"}.get(sep, sep)
        df = pd.read_csv(filepath, sep=sep_actual, header=None if names is not None else 0, names=names, skiprows=skiprows, encoding=encoding)
    return df

def main():
    args = parse_args()
    files = find_files(args.input_folder, args.pattern)
    if not files:
        print(f"No files found in {args.input_folder} matching {args.pattern}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(files)} files. First file: {files[0]}")

    # read first file to get header (if present) and initial dataframe
    header_present = not args.no_header
    try:
        df0 = read_first_file(files[0], args.sep, args.encoding, header_present)
    except Exception as e:
        print(f"Failed to read first file {files[0]}: {e}", file=sys.stderr)
        sys.exit(2)

    df_list = [df0]
    # for subsequent files, skip header rows and parse using the first file's columns (if header present)
    if header_present:
        col_names = list(df0.columns)
        skiprows = args.skip_rows
        for f in files[1:]:
            try:
                dfi = read_file_as_df(f, args.sep, args.encoding, names=col_names, skiprows=skiprows)
                df_list.append(dfi)
            except Exception as e:
                print(f"Warning: failed to parse {f} as table, will try line-based concatenation. Error: {e}", file=sys.stderr)
                # fallback: read raw lines, split, and try to create dataframe
                raw_rows = []
                with open(f, 'r', encoding=args.encoding, errors='ignore') as fh:
                    for _ in range(skiprows):
                        next(fh, None)
                    for line in fh:
                        parts = line.strip().split()
                        if parts:
                            raw_rows.append(parts)
                if raw_rows:
                    # pad rows to match column count
                    max_cols = len(col_names)
                    norm_rows = [row[:max_cols] + [None]*(max_cols-len(row)) if len(row) < max_cols else row[:max_cols] for row in raw_rows]
                    dfi = pd.DataFrame(norm_rows, columns=col_names)
                    df_list.append(dfi)
    else:
        # no header: read all files with header=None and concatenate, columns will be numbered
        for f in files[1:]:
            try:
                dfi = read_file_as_df(f, args.sep, args.encoding, names=None, skiprows=args.skip_rows)
                # if header absent, ensure same number of columns by padding/truncating
                if dfi.shape[1] != df0.shape[1]:
                    # try re-reading with delim_whitespace and engine python to be robust
                    dfi = read_file_as_df(f, args.sep, args.encoding, names=None, skiprows=args.skip_rows)
                df_list.append(dfi)
            except Exception as e:
                print(f"Warning: failed to parse {f}: {e}", file=sys.stderr)
                continue

    # concat dataframes (ignore index to reindex rows)
    try:
        combined = pd.concat(df_list, ignore_index=True)
    except Exception as e:
        print(f"Failed to concatenate dataframes: {e}", file=sys.stderr)
        sys.exit(3)

    # write combined text file (tab-separated) and Excel
    out_txt = args.output_txt
    out_xlsx = args.output_xlsx

    # ensure output dir exists
    out_dir = os.path.dirname(os.path.abspath(out_txt)) or "."
    os.makedirs(out_dir, exist_ok=True)

    try:
        combined.to_csv(out_txt, sep='\t', index=False, na_rep='')
        print(f"Wrote combined text to {out_txt} (tab-separated).")
    except Exception as e:
        print(f"Warning: failed to write combined text file {out_txt}: {e}", file=sys.stderr)

    try:
        # choose engine based on extension or arg
        engine = args.engine_xlsx
        # ensure directory exists for xlsx
        os.makedirs(os.path.dirname(os.path.abspath(out_xlsx)) or ".", exist_ok=True)
        combined.to_excel(out_xlsx, index=False, engine=engine)
        print(f"Wrote Excel file to {out_xlsx}.")
    except Exception as e:
        print(f"Failed to write Excel file {out_xlsx}: {e}", file=sys.stderr)

    print(f"Combined dataframe shape: {combined.shape}")
    # show head
    print("Preview (first 5 rows):")
    print(combined.head())

if __name__ == "__main__":
    main()
