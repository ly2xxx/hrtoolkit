#!/usr/bin/env python3
"""Generate sample CSV file from sample data"""

from sample_data import generate_360_review_data

def main():
    """Generate and save sample CSV"""
    df = generate_360_review_data()
    df.to_csv("sample_360_reviews.csv", index=False)
    print(f"Generated sample_360_reviews.csv with {len(df)} records for {df['employee_name'].nunique()} employees")

if __name__ == "__main__":
    main()