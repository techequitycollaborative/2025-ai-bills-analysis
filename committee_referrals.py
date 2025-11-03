#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
committee_referrals.py
Date: Nov 3, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load AI bills data
bills = pd.read_csv('./data/bill_data_with_success_status.csv')

# Check for Judiciary (JUD) and Privacy (P. & C.P.) committee referrals 
def check_committee_referrals(df):
    """
    Creates a new 'committee_referral' column in the DataFrame that categorizes 
    bills based on whether they were referred to the Senate Judiciary (JUD) committee,
    Assembly Privacy (P&CP) committee, both, or niether.
    
    Parameters:
    -----------
    df: DataFrame with bill data
    
    Returns:
    --------
    new_df: The DataFrame with a new 'committee_referral' column added
    """
    # Define conditions and corresponding values
    conditions = [
        (df['bill_history'].str.contains('JUD', case=True, na=False) & 
         df['bill_history'].str.contains('P. & C.P.', case=True, na=False)),
        (df['bill_history'].str.contains('JUD', case=True, na=False) & 
         ~df['bill_history'].str.contains('P. & C.P.', case=True, na=False)),
        df['bill_history'].str.contains('P. & C.P.', case=True, na=False)
    ]
    
    # Define category labels
    choices = ['Both', 'Senate Judiciary', 'Assembly Privacy']
    
    # Assign labels (default is 'Neither')
    df['committee_referral'] = np.select(conditions, choices, default='Neither')
    
    return df

bills = check_committee_referrals(bills)

# Grab just a few columns to review output
referrals = bills[['bill_number','bill_history','committee_referral', 'success']]

# Get summary breakdown of committee referral categories
referral_summary = referrals['committee_referral'].value_counts().reset_index()
referral_summary.columns = ['Committee Referral', 'Count']
referral_summary['Percentage'] = (referral_summary['Count'] / referral_summary['Count'].sum()) * 100
print(referral_summary)

# Save data with committee referrals
bills.to_csv('./data/bills_with_committee_referrals.csv', index=False) # All data
referral_summary.to_csv('./data/committee_referral_summary.csv', index=False) # Summary data

# Plot
plt.figure(figsize=(8,6))
plt.pie(referral_summary['Count'], labels=referral_summary['Committee Referral'], autopct='%1.1f%%', colors=sns.color_palette('Set2', 4))
plt.title('Committee Referrals')
plt.savefig('./plots/committee_referrals.png')
plt.show()



