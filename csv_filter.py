#!/usr/bin/env python3
import argparse
import sys
import pandas as pd
from pathlib import Path

def validate_file(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    if not path.is_file():
        print(f"Error: '{filepath}' is not a file.")
        sys.exit(1)
    if path.suffix.lower() != '.csv':
        print(f"Warning: File '{filepath}' doesn't have .csv extension.")
    return path

def load_csv(filepath):
    try:
        print(f"Loading {filepath}...")
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df):,} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

def filter_data(df, column, value, use_contains=False):
    if column not in df.columns:
        print(f"Error: Column '{column}' not found.")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)
    
    try:
        if use_contains:
            mask = df[column].astype(str).str.contains(str(value), case=False, na=False)
            filter_type = "contains"
        else:
            try:
                if pd.api.types.is_numeric_dtype(df[column]):
                    value = pd.to_numeric(value)
            except (ValueError, TypeError):
                pass 
            
            mask = df[column] == value
            filter_type = "equals"
        
        filtered_df = df[mask]
        print(f"\nFilter applied: {column} {filter_type} '{value}'")
        print(f"Found {len(filtered_df):,} matching rows")
        return filtered_df
        
    except Exception as e:
        print(f"Error filtering data: {e}")
        sys.exit(1)

def save_csv(df, output_path):
    try:
        df.to_csv(output_path, index=False)
        print(f"Saved to: {output_path}")
    except Exception as e:
        print(f"Error saving CSV: {e}")
        sys.exit(1)

def preview_data(df, n=5):
    print(f"\nPreview (first {min(n, len(df))} rows):")
    print("=" * 80)
    print(df.head(n).to_string())
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description='Filter CSV files')
    parser.add_argument('input_file')
    parser.add_argument('--column', '-c', required=True)
    parser.add_argument('--value', '-v', required=True)
    parser.add_argument('--contains', action='store_true')
    parser.add_argument('--output', '-o', default='filtered.csv')
    parser.add_argument('--preview', '-p', action='store_true')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("CSV Filter Tool")
    print("=" * 80)
    
    validate_file(args.input_file)
    df = load_csv(args.input_file)
    filtered_df = filter_data(df, args.column, args.value, args.contains)
    
    if len(filtered_df) == 0:
        print("\nNo matching rows found.")
        sys.exit(0)
    
    if args.preview:
        preview_data(filtered_df)
    else:
        save_csv(filtered_df, args.output)
    
    print("\nDone!")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    main()