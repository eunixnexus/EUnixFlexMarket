"""
MIT License

Copyright (c) 2019, Diego Kiedanki
Copyright (c) 2025, Godwin Okwuibe

This file includes modifications made by Godwin Okwuibe in 2025.
"""
import pandas as pd
from EUnixFlex.transactions.transactions import TransactionManager


def split_transactions_merged_players(transactions, bids, mapping, fees=None):
    """

    """
    new_trans = TransactionManager()

    for _, t in transactions.get_df().iterrows():
        bid_id = t.bid
        original_rows = mapping.get(bid_id, [])

        # Proportional share of quantity
        total_quantity = bids.iloc[original_rows]["quantity"].sum()
        proportions = bids.iloc[original_rows]["quantity"] / total_quantity if total_quantity > 0 else 0

        # Optional fee for the merged transaction
        fee_per_user = None
        if len(original_rows) > 1 and fees is not None:
            fee_per_user = fees.pop(t.user, None)

        for row_idx in original_rows:
            user_row = bids.iloc[row_idx]
            t_values = t.copy()

            # Update bid and quantity for disaggregated transaction
            t_values.bid = row_idx
            t_values.quantity *= proportions[row_idx]

            # Update fee per user if applicable
            if fee_per_user is not None:
                user_id = user_row.user
                fees[user_id] = fee_per_user * proportions[row_idx]

            new_trans.add_transaction(*t_values.values)

    return (new_trans, fees) if fees is not None else new_trans
