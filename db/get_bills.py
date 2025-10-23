#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_bills.py
Date: Oct 23, 2025
"""

from db.config import config
from db.query import get_table

def get_bills():
    """ Load AI bills from PostgreSQL database into pandas DataFrame """
    # Get database configuration
    db_config = config('postgres')

    # Load AI bills from database
    df = get_table(db_config, 'ai_bills_2025', schema='bill_analytics')
        
    if df is not None:
        print(df.head())
        print(f'\nShape: {df.shape}')

    return df

