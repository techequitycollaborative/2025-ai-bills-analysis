#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lobbying.py
Date: Nov 3, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load lobbying data
data = pd.read_csv('./data/lobbying_data.csv')

# Check columns
print(data.columns)

# Get 2025-2026 data only
data_2526 = data[data['SESSION'] == '2025-2026']
data_2526 = data_2526[['COMPANY','QUARTER','GENERAL LOBBYING']] # grab a few columns

# Summarize total lobbying expenses by company for 2025-2026
data_2526['GENERAL LOBBYING'] = pd.to_numeric(data_2526['GENERAL LOBBYING'], errors='coerce') # Convert 'GENERAL LOBBYING' to numeric, coercing errors to NaN
lobbying_summary_2526 = data_2526.groupby('COMPANY')['GENERAL LOBBYING'].sum().reset_index() # Group by compay and sum amounts
lobbying_summary_2526 = lobbying_summary_2526.rename(columns={'GENERAL LOBBYING': 'AMOUNT'}) # Rename general lobbying columnt to 'AMOUNT'
lobbying_summary_2526 = lobbying_summary_2526.sort_values(by='AMOUNT', ascending=False) # Sort by amount descending
print(lobbying_summary_2526)

# Plots

# Overall 2025-2026 lobbying amounts by company
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=lobbying_summary_2526, x='AMOUNT', y='COMPANY', palette='viridis') 
plt.title('2025-2026 Lobbying Amounts by Company')
plt.xlabel('Total Lobbying Amount ($)')
plt.ylabel('Company / Organization')

# Add value labels to each bar
for i, bar in enumerate(ax.patches):
    value = bar.get_width()
    ax.text(value, bar.get_y() + bar.get_height()/2, 
            f'${value:,.0f}', 
            va='center', ha='left', fontsize=10, color='black')

plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig('./plots/lobbying_amounts_by_company_2025_2026.png')
plt.show()




