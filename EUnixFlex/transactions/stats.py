import pandas as pd
import numpy as np

def compute_statis(dfr):
    # Ensure correct data types
    dfr['Matched_qty'] = pd.to_numeric(dfr['Matched_qty'], errors='coerce')
    dfr['Clearing_rate'] = pd.to_numeric(dfr['Clearing_rate'], errors='coerce')
    dfr['Bid_rate'] = pd.to_numeric(dfr['Bid_rate'], errors='coerce')
    dfr['Offer_rate'] = pd.to_numeric(dfr['Offer_rate'], errors='coerce')
    dfr['Bid_qty'] = pd.to_numeric(dfr['Bid_qty'], errors='coerce')
    dfr['Offer_qty'] = pd.to_numeric(dfr['Offer_qty'], errors='coerce')

    stats = {}

    # Market-Level Statistics
    stats['market'] = {
        'Total Matched Quantity': dfr['Matched_qty'].sum(),
        'Average Clearing Price': dfr['Clearing_rate'].mean(),
        'Weighted Average Clearing Price': (
            (dfr['Clearing_rate'] * dfr['Matched_qty']).sum() / dfr['Matched_qty'].sum()
        ),
        'Average Market Spread (Bid - Offer)': (dfr['Bid_rate'] - dfr['Offer_rate']).mean(),
        'Clearing Price Volatility (Std Dev)': dfr['Clearing_rate'].std()
    }

    # 📈 Buyer Statistics
    buyers = dfr[dfr['Trans_type'] == 'Buying']
    stats['buyers'] = {
        'Average Bid Price': buyers['Bid_rate'].mean(),
        'Median Bid Rate': buyers['Bid_rate'].median(),
        'Min Bid Rate': buyers['Bid_rate'].min(),
        'Max Bid Rate': buyers['Bid_rate'].max(),
        'Total bid volume': buyers['Bid_qty'].sum()
    }

    # 📉 Seller Statistics
    sellers = dfr[dfr['Trans_type'] == 'Selling']
    stats['sellers'] = {
        'Average Offer Price': sellers['Offer_rate'].mean(),
        'Median Offer Rate': sellers['Offer_rate'].median(),
        'Min Offer Rate': sellers['Offer_rate'].min(),
        'Max Offer Rate': sellers['Offer_rate'].max(),
        'Total Offer volume': sellers['Offer_qty'].sum()
    }

    # 📊 Matching Efficiency and Distribution
    stats['matching'] = {
        'Number of Unique Transactions': dfr['Trans_id'].nunique(),
        'Number of Unique Buyers': dfr['Buyer'].nunique(),
        'Number of Unique Sellers': dfr['Seller'].nunique(),
        'Clearing Efficiency Ratio': dfr['Matched_qty'].sum() / dfr['Offer_qty'].sum(),
        'Average Matches per Transaction ID': dfr.groupby('Trans_id').size().mean(),
        'Match Imbalance Index': abs(dfr['Bid_qty'].sum() - dfr['Offer_qty'].sum()) / max(dfr['Bid_qty'].sum(), dfr['Offer_qty'].sum())
    }

    return stats
