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

# Apply bill success statuses
bills = assign_success(bills)
print(bills[['status', 'success']].head(15))

# Get breakdown of each success category
signed_bills = bills[bills['success'] == 'Signed']
vetoed_bills = bills[bills['success'] == 'Vetoed']
failed_bills = bills[bills['success'] == 'Failed']

num_signed = len(signed_bills)
num_vetoed = len(vetoed_bills)
num_failed = len(failed_bills)
perc_signed = (num_signed / len(bills)) * 100
perc_vetoed = (num_vetoed / len(bills)) * 100 
perc_failed = (num_failed / len(bills)) * 100

print(f'Signed Bills: {num_signed}, {perc_signed:.2f}%')
print(f'Vetoed Bills: {num_vetoed}, {perc_vetoed:.2f}%')
print(f'Failed Bills: {num_failed}, {perc_failed:.2f}%')
print(f'Total AI Bills: {len(bills)}')

# Get bill success by bill topic
success_by_topic = bills.groupby('assigned_topics')['success'].value_counts()
print(success_by_topic)

success_by_topic_2 = bills.explode('assigned_topics').groupby('assigned_topics')['success'].value_counts
print(success_by_topic_2)
