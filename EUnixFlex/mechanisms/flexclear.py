

import pandas as pd
import uuid
from EUnixFlex.transactions.transactions import TransactionManager
from EUnixFlex.mechanisms import Mechanism


def flexibility_clearing(orders, flex_type="positive", demand_qty=0):
    """
    Market clearing for flexibility demand from TSO/DSO.

    Parameters
    ----------
    orders : pd.DataFrame
        DataFrame with columns:
        - type (True=bid, False=offer)
        - energy_rate
        - energy_qty
        - User, User_id, Unit_area, Order_id, bid_offer_time, delivery_time
    flex_type : str
        "positive" (TSO wants upward flexibility → use bids)
        "negative" (TSO wants downward flexibility → use offers)
    demand_qty : float
        Amount of flexibility required by TSO/DSO

    Returns
    -------
    trans : TransactionManager
        All matched transactions
    extra : dict
        Metadata: clearing price, clearing quantity, side used
    """

    trans = TransactionManager()

    if flex_type == "positive":
        side = orders[orders.type].sort_values("energy_rate", ascending=False)
    else:  # negative flexibility
        side = orders[~orders.type].sort_values("energy_rate", ascending=True)

    qty_accumulated = 0
    clearing_price = None

    for _, row in side.iterrows():
        if qty_accumulated >= demand_qty:
            break
        matched_qty = min(row.energy_qty, demand_qty - qty_accumulated)
        clearing_price = row.energy_rate
        trans.add_transaction(*create_flex_transaction(row, clearing_price, matched_qty))
        qty_accumulated += matched_qty

    return trans, {
        "flex_type": flex_type,
        "clearing_price": clearing_price,
        "clearing_quantity": qty_accumulated,
    }


def create_flex_transaction(row, price, matched_qty):
    """Helper to generate transaction tuple for flexibility clearing."""
    tx_id = str(uuid.uuid4())
    if row.type:  # Buyer (TSO/DSO request)
        return (
            tx_id, row.User, row.User_id, row.Unit_area, row.Order_id,
            row.energy_qty, row.energy_rate, row.bid_offer_time,
            "", "", "", "", "", "", price, matched_qty,
            row.delivery_time, "FlexBuyer"
        )
    else:  # Seller (flexibility provider)
        return (
            tx_id, "", "", row.Unit_area, "", "", "", "",
            row.User, row.User_id, row.Order_id, row.energy_qty,
            row.energy_rate, row.bid_offer_time, price, matched_qty,
            row.delivery_time, "FlexSeller"
        )


class FlexibilityClearing(Mechanism):
    """Interface for the new flexibility clearing mechanism."""

    def __init__(self, orders, *args, flex_type="positive", demand_qty=0, **kwargs):
        super().__init__(flexibility_clearing, orders, flex_type=flex_type, demand_qty=demand_qty, *args, **kwargs)
