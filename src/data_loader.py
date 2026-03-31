# src/data_loader_simple.py
"""Simple data loader for Rossmann Store Sales dataset"""
import pandas as pd
from pathlib import Path

# Load the three datasets
print("="*50)
print("LOADING ROSSMANN DATA")
print("="*50)

# 1. Load training data
train_path = Path('data/raw/train.csv')
train_df = pd.read_csv(train_path)
print(f"\n✓ Train data loaded: {train_df.shape[0]:,} rows, {train_df.shape[1]} columns")
print(f"  Columns: {list(train_df.columns)}")

# 2. Load test data
test_path = Path('data/raw/test.csv')
test_df = pd.read_csv(test_path)
print(f"\n✓ Test data loaded: {test_df.shape[0]:,} rows, {test_df.shape[1]} columns")
print(f"  Columns: {list(test_df.columns)}")

# 3. Load store data
store_path = Path('data/raw/store.csv')
store_df = pd.read_csv(store_path)
print(f"\n✓ Store data loaded: {store_df.shape[0]:,} rows, {store_df.shape[1]} columns")
print(f"  Columns: {list(store_df.columns)}")

# Quick look at first few rows
print("\n" + "="*50)
print("FIRST 5 ROWS - TRAIN DATA")
print("="*50)
print(train_df.head())

print("\n" + "="*50)
print("FIRST 5 ROWS - STORE DATA")
print("="*50)
print(store_df.head())

# Basic info about missing values
print("\n" + "="*50)
print("MISSING VALUES")
print("="*50)
print("\nTrain data missing values:")
print(train_df.isnull().sum())

print("\nStore data missing values:")
print(store_df.isnull().sum())

# Save the merged dataset (combine train + store info)
print("\n" + "="*50)
print("MERGING TRAIN AND STORE DATA")
print("="*50)

# Merge on 'Store' column
merged_df = train_df.merge(store_df, on='Store', how='left')
print(f"✓ Merged data shape: {merged_df.shape[0]:,} rows, {merged_df.shape[1]} columns")

# Save merged data for later use
merged_path = Path('data/processed/rossmann_merged.csv')
merged_path.parent.mkdir(parents=True, exist_ok=True)
merged_df.to_csv(merged_path, index=False)
print(f"✓ Saved merged data to: {merged_path}")

print("\n✅ DATA LOADING COMPLETE!")