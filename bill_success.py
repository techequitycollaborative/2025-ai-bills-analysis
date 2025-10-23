#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bill_success.py
Date: Oct 23, 2025
"""

from db.get_bills import get_bills
import pandas as pd
import numpy as np

# Load AI bills data
bills = get_bills()

# Check columns
print(bills.columns)

# Check unique bill status
unique_status = bills['status'].unique()
print(unique_status)

# Assign success categories based on bill status
def assign_success(df):
    """
    Creates a new 'success' column in the DataFrame that categorizes 
    bills based on whether they failed, were signed, or were vetoed.
    
    Parameters:
    -----------
    df: DataFrame with bill data
    
    Returns:
    --------
    new_df: The DataFrame with a new 'success' column added
    """
    # Define conditions and corresponding values
    conditions = [
        df['status'].str.contains('veto', case=False, na=False),
        (df['status'].str.contains('approved by governor', case=False, na=False) |
        df['status'].str.contains('chaptered by secretary of state', case=False, na=False))
        ] # Failed = all other statuses
   
    # Define category labels
    choices = ['Vetoed', 'Signed']
    
    # Assign labels (default is 'Failed')
    df['success'] = np.select(conditions, choices, default='Failed')
    
    return df

bills = assign_success(bills)
print(bills[['status', 'success']].head(10))
