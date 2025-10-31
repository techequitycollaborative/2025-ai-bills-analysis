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
vote_data = merged_df[['bill_number','chamber','status','success','motion_text','vote_location','vote_date','vote_result','vote_threshold','yes_count','no_count','other_count','total_votes','vote_threshold_num','vote_margin']]
print(vote_data.head(10))
print(vote_data['bill_number'].nunique()) # Check that unique bills totals to 71

# Sort data by bill number and vote date
vote_data = vote_data.sort_values(by=['bill_number','vote_date'])

# Are any bills missing vote data? This would imply they never got to a floor vote.
bills_without_vote = vote_data[vote_data['vote_result'].isnull()]
print(len(bills_without_vote)) # 3 bills without floor votes

# Now look at the Third Reading votes specifically
third_reading_votes = vote_data[vote_data['motion_text'].str.contains('Third Reading|3rd reading', case=False, na=False, regex=True)].copy()
print(len(third_reading_votes))

######## CORRECTING DATA ISSUES ########
# Look at sb274, which for some reason has three origin house votes
sb274 = third_reading_votes[third_reading_votes['bill_number'] == 'SB 274'].sort_values(by=['vote_date'])

# Seems to be a duplicate data issue with SB274, so dropping 2 duplicate third reading columns for SB 274
third_reading_votes = third_reading_votes.drop([267, 268])

# Some bills oddly only have an Opposite House vote -- investigate
sb241 = vote_data[vote_data['bill_number'] == 'SB 241'].sort_values(by=['vote_date'])
sb361 = vote_data[vote_data['bill_number'] == 'SB 361'].sort_values(by=['vote_date'])
ab682 = vote_data[vote_data['bill_number'] == 'AB 682'].sort_values(by=['vote_date'])

# Grab the indexes of the floor votes in the house of origin for these three bills; they each had different motion text that did not contain third/3rd reading
keep_these_rows = [272, 34, 71]

# Append those rows to third_reading_votes
additional_votes = vote_data.loc[keep_these_rows]
third_reading_votes = pd.concat([third_reading_votes, additional_votes], ignore_index=True)
print(len(third_reading_votes))

#############################################

# Function to determine if a bill had one floor vote (in house of origin) or two (house of origin + second house)
def assign_vote_type(row):
    if row['chamber'] == row['vote_location']:
        return 'Origin House'
    else:
        return 'Opposite House'
    
third_reading_votes['vote_type'] = third_reading_votes.apply(assign_vote_type, axis=1)

# Get summary of vote types per bill
vote_type_summary = third_reading_votes.groupby('bill_number')['vote_type'].value_counts().unstack(fill_value=0)
print(vote_type_summary.head(10))

# Add a total column
vote_type_summary['Total'] = vote_type_summary[['Opposite House','Origin House']].sum(axis=1)
print(vote_type_summary.head(10))

# Add a column indicating if the bill had votes in both houses
vote_type_summary['Both Houses'] = np.where(
    (vote_type_summary['Total'] == 2),
    True,
    False
)
print(vote_type_summary.head(10))

# Check that no bills have 0 house of origin votes
origin_zero = vote_type_summary[vote_type_summary['Origin House'] == 0]
print(len(origin_zero)) # 0 bills with zero origin house votes

# Get list of bills that had votes in one house only
single_house_bills = vote_type_summary[vote_type_summary['Both Houses'] == False].index.tolist()
print(len(single_house_bills))
print(single_house_bills)

# Get list of bills that had votes in both houses
both_house_bills = vote_type_summary[vote_type_summary['Both Houses'] == True].index.tolist()
print(len(both_house_bills))
print(both_house_bills)

# For bills that have votes in one house only, grab those rows from third_reading_votes
single_house_votes = third_reading_votes[third_reading_votes['bill_number'].isin(single_house_bills)].copy()
print(len(single_house_votes))
print(single_house_votes.head(10))

# For bills that have votes in both houses, grab those rows from third_reading_votes
both_house_votes = third_reading_votes[third_reading_votes['bill_number'].isin(both_house_bills)].copy()
print(len(both_house_votes))
print(both_house_votes.head(10))

# For single house votes, get average assembly and senate vote margins
avg_single_house_margins = single_house_votes.groupby('vote_location')['vote_margin'].mean().reset_index()
print(avg_single_house_margins)

# For both house votes, get average assembly and senate vote margins
avg_both_house_margins = both_house_votes.groupby(['chamber','vote_location'])['vote_margin'].mean().reset_index()
print(avg_both_house_margins)

# Save data to CSV
vote_data.to_csv('./data/all_floor_votes.csv', index=False) # All floor votes
single_house_votes.to_csv('./data/single_floor_votes.csv', index=False) # Bills that only had one floor vote in house of origin
both_house_votes.to_csv('./data/both_floor_votes.csv', index=False) # Bills that had floor vote in both houses

# Plots

# Single vote bills: floor vote margin
plot_data = single_house_votes[['bill_number','vote_location','vote_margin']].sort_values(by=['vote_location','vote_margin'], ascending=True)
print(plot_data.head(10))

plt.figure(figsize=(10,6))
sns.barplot(data=plot_data, x='bill_number', y='vote_margin', hue='vote_location')
plt.xticks(rotation=90)
plt.title('Vote Margin for Single Floor Vote Bills')
plt.xlabel('')
plt.ylabel('Vote Margin')
plt.tight_layout()
plt.savefig('./plots/single_floor_vote_margins.png')
plt.show()

# Both vote bills: floor vote margin

# Look at only passing votes
plot_data = both_house_votes[both_house_votes['vote_result'] == 'pass']

# Sort by bill number, then vote location
plot_data = both_house_votes[['bill_number','vote_location','vote_margin']].sort_values(by=['bill_number','vote_location'], ascending=True)

# Pivot the df so that each bill is one row, with a column for assembly vote margin and a column for senate vote margin
plot_data_pivot = plot_data.pivot(index='bill_number', columns='vote_location', values='vote_margin').reset_index()
print(plot_data_pivot.head(10))

# Multiply senate margins by -1 bc senate margins will be displayed below the x-axis
plot_data_pivot['Senate'] = plot_data_pivot['Senate'] * -1
print(plot_data_pivot.head(10))

# Sort by Assembly vote margin
plot_data_pivot = plot_data_pivot.sort_values(by=['Assembly'], ascending=True)

# Make the plot
plt.figure(figsize=(10,6))
sns.barplot(data=plot_data_pivot, x='bill_number', y='Assembly', color='blue', label='Assembly')
sns.barplot(data=plot_data_pivot, x='bill_number', y='Senate', color='orange', label='Senate')
plt.xticks(rotation=90)
plt.xlabel('')
plt.ylabel('Vote Margin')
plt.title('Vote Margins for Bills with Floor Votes in Both Houses')

# Replace 0 for 'Win' in y axis
yticks = plt.yticks()[0]
yticklabels = [str(int(tick)) if tick != 0 else 'Win' for tick in yticks]
plt.yticks(yticks, yticklabels)

plt.tight_layout()
plt.savefig('./plots/both_floor_vote_margins.png')
plt.show()

# Plot notes
# -- SB 274's Assembly vote margin was zero
# -- SB 295's Assembly vote margin was negative, meaning it did not pass the assembly floor