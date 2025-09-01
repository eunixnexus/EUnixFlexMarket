# -*- coding: utf-8 -*-
"""
Implements processing techniques applied to bids before mechanisms can use them.
"""
import numpy as np
import pandas as pd
from collections import OrderedDict


def new_player_id(start_index: int):
    """

    """
    new_player_id.index = start_index

    def assign_id(users):
        if len(users) > 1:
            new_id = new_player_id.index
            new_player_id.index += 1
            return new_id
        return users[0]

    return assign_id


def merge_same_price(df: pd.DataFrame, prec: int = 5):


    # Start assigning virtual user IDs after the highest current ID
    id_gen = new_player_id(df.user.max() + 1)

    original_columns = df.columns.copy()
    df = df.copy().reset_index().rename(columns={'index': 'bid'})

    # Split into buying and selling sides
    buy_df = df[df['buying']]
    sell_df = df[~df['buying']]

    all_sides = [buy_df, sell_df]
    merged_dfs = []
    bid_mapping = OrderedDict()

    # Define how each column should be aggregated
    agg_functions = {
        'bid': list,
        'user': list,
        'quantity': sum,
        'buying': lambda x: x.iloc[0],
        'time': lambda x: x.iloc[0],
        'divisible': lambda x: x.iloc[0]
    }

    for side_df in all_sides:
        # Group by rounded price
        rounded_price = side_df.price.round(prec)
        grouped = side_df.groupby(rounded_price).agg(agg_functions).reset_index()

        # Assign new user IDs (same if only 1 user; new ID if >1)
        grouped['user'] = grouped['user'].apply(id_gen)

        # Keep track of bid origins
        for i, bids in enumerate(grouped['bid']):
            bid_mapping[i] = bids

        merged_dfs.append(grouped)

    # Combine buy and sell sides
    merged_df = pd.concat(merged_dfs).reset_index(drop=True)

    # Reorder columns to match original input
    merged_df = merged_df[original_columns]

    return merged_df, bid_mapping
