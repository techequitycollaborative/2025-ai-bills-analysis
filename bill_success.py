#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bill_success.py
Date: Oct 23, 2025
"""

from db.get_bills import get_bills
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
        (df['status'].str.contains('approved by the governor', case=False, na=False) |
        df['status'].str.contains('chaptered by secretary of state', case=False, na=False))
        ] # Failed = all other statuses
   
    # Define category labels
    choices = ['Vetoed', 'Signed']
    
    # Assign labels (default is 'Failed')
    df['success'] = np.select(conditions, choices, default='Failed')
    
    return df

# Apply bill success statuses
bills = assign_success(bills)
print(bills[['assigned_topics','status', 'success']].head(15))

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

success_summary = pd.DataFrame({
    'Status': ['Signed', 'Vetoed', 'Failed', 'Total'],
    'Count': [num_signed, num_vetoed, num_failed, len(bills)],
    'Percentage': [perc_signed, perc_vetoed, perc_failed, 100.0]
})

print(success_summary)

####### BILLS BY TOPIC #######

### THIS CHUNK OF CODE USES THE LEGISLATION TRACKER ASSIGNED TOPICS ###

# Get bill success by bill topic
#success_by_topic = bills.groupby('assigned_topics')['success'].value_counts()
#print(success_by_topic)

# Some bills have multiple topics, so we need to separate them out
#success_by_topic_expanded = bills.assign(
#    assigned_topics=bills['assigned_topics'].str.split('; ')
#).explode('assigned_topics')
#print(success_by_topic_expanded[['assigned_topics','success']].head(10))

# Regroup by topic, now that we split them out
#success_by_topic_summary = success_by_topic_expanded.groupby(['assigned_topics', 'success']).size().unstack(fill_value=0)
#success_by_topic_summary['Total'] = success_by_topic_summary.sum(axis=1) # Add a total column
#success_by_topic_summary = success_by_topic_summary.sort_values('Total', ascending=False) # Sort
#print(success_by_topic_summary)

# Check overall total -- should be more than 71, which is the total number of bills
#print(success_by_topic_summary['Total'].sum())

### THIS NEXT CHUNK OF CODE USES MEGAN'S TOPICS ###

# Merge megan's topics into bills dataframe
megan_topics = pd.read_csv('./data/megan_topics.csv')
bills = bills.merge(megan_topics[['Bill No', 'Megan Topic']], left_on='bill_number', right_on='Bill No', how='left')
print(bills[['bill_number', 'assigned_topics', 'Megan Topic']].head(10))

# Get bill success by Megan's topics
success_by_topic = bills.groupby('Megan Topic')['success'].value_counts()
print(success_by_topic)

# Make summary table
success_by_topic_summary = bills.groupby(['Megan Topic', 'success']).size().reset_index(name='Count')
success_by_topic_summary = success_by_topic_summary.pivot(index='Megan Topic', columns='success', values='Count')
success_by_topic_summary = success_by_topic_summary.fillna(0).astype(int) # Fill NaN values with 0
success_by_topic_summary = success_by_topic_summary.reset_index() # Reset index to make Megan Topic a column again
success_by_topic_summary = success_by_topic_summary.rename(columns={'Megan Topic': 'Topic'}) # Rename columns
success_by_topic_summary['Total'] = success_by_topic_summary[['Failed', 'Signed', 'Vetoed']].sum(axis=1) # Add a total column
print(success_by_topic_summary)
print(success_by_topic_summary['Total'].sum()) # Check overall total -- should be 71

# Save data as csv
bills.to_csv('./data/bill_data_with_success_status.csv', index=False)
#success_by_topic_expanded.to_csv('./data/bill_topic_expanded.csv') # This data creates multiple rows per bill if a bill has multiple topics
success_summary.to_csv('./data/bill_success_summary.csv')
success_by_topic_summary.to_csv('./data/bill_success_by_topic.csv') # With Megan's topics

# Plots

# Bill success overall
plt.figure(figsize=(8,6))
plt.pie(success_summary['Count'].iloc[:-1], labels=success_summary['Status'].iloc[:-1], autopct='%1.1f%%', colors=sns.color_palette('Set2', 3))
plt.title('AI Bills Success Overview')
plt.savefig('./plots/bill_success_overview.png')
plt.show()

# Bill success by topic
plt.figure(figsize=(12,8))
df = success_by_topic_summary.drop(columns=['Total'])
df = df.set_index('Topic') # Set 'Topic' as the index for plotting
df.plot(kind='bar', stacked=True, colormap='Set3', figsize=(12,8))
plt.xlabel('Bill Topic')
plt.legend(title='Bill Status')
plt.title('Bill Success by Topic')
plt.tight_layout()
plt.savefig('./plots/bills_by_topic.png')
plt.show()
