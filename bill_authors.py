#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bill_authors.py
Date: Oct 27, 2025
"""

from db.get_bills import get_bills
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load AI bills data
bills = pd.read_csv('./data/bill_data_with_success_status.csv')
print(bills.columns)

# Group bill success status by author
author_success = bills.groupby(['author', 'success']).size().unstack(fill_value=0)
print(author_success.head(10))

# Add a total column
author_success['Total'] = author_success.sum(axis=1)
print(author_success.head(10))

# Authors with at least 1 signed bill, sorted by signed bills
authors_with_1_signed = author_success[author_success['Signed'] > 0].sort_values(by='Signed', ascending=False)
print(authors_with_1_signed)

# Save to CSV
author_success.to_csv('./data/bills_by_author.csv')

# Plot authors with at least 1 signed bill
plt.figure(figsize=(12, 8))
df = authors_with_1_signed.drop(columns=['Total'])
df = df.sort_values(by='Signed', ascending=True) # Sort so that highest number of signed bills is on the top of the plot
df.plot(kind='barh', stacked=True, colormap='Set3', figsize=(12,8))
plt.ylabel('Author')
plt.xlabel('Number of bills')
plt.legend(title='Bill Status')
plt.title('Bill Success by Author')
plt.tight_layout()
plt.savefig('./plots/bills_by_author.png')
plt.show()
