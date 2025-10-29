#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
floor_votes.py
Date: Oct 28, 2025
"""
from db.get_votes import get_votes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load AI bills data with success status
bills = pd.read_csv('./data/bill_data_with_success_status.csv')
print(bills.columns)

# Load floor votes data from db
votes = get_votes()

# Merge bills with votes on bill_id
merged_df = pd.merge(bills, votes, on='openstates_bill_id', how='left')
print(merged_df.columns)
print(len(merged_df))

# Focus on a few columns
vote_data = merged_df[['bill_number','chamber','success','motion_text','vote_location','vote_date','vote_result','yes_count','no_count','other_count','total_votes','vote_threshold_num','vote_margin']]
print(vote_data.head(10))
print(vote_data['bill_number'].nunique()) # Check that unique bills totals to 71

# Sort data by bill number, vote location, and vote date
vote_data = vote_data.sort_values(by=['bill_number','vote_location','vote_date'])

# Save to CSV
vote_data.to_csv('./data/floor_votes.csv', index=False)

# Look at an individual bill's votes
ab325 = vote_data[vote_data['bill_number'] == 'AB 325'].sort_values(by=['vote_date'])
