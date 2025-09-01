"""
MIT License

Copyright (c) 2019, Diego Kiedanki
Copyright (c) 2025, Godwin Okwuibe

This file includes modifications made by Godwin Okwuibe in 2025.
"""
import pandas as pd


class TransactionManager:


    name_col = [
        "Trans_id", "Buyer", "Buyer_id", "Unit_area", "Bid_id", "Bid_qty",
        "Bid_rate", "Bid_time", "Seller", "Seller_id", "Offer_id", "Offer_qty",
        "Offer_rate", "Offer_time", "Clearing_rate", "Matched_qty",
        "Delivery_time", "Trans_type"
    ]

    def __init__(self):
        """Initializes an empty transaction manager."""
        self.n_trans = 0
        self.trans = []

    def add_transaction(
        self, Trans_id, Buyer, Buyer_id, Unit_area, Bid_id, Bid_qty,
        Bid_rate, Bid_time, Seller, Seller_id, Offer_id, Offer_qty,
        Offer_rate, Offer_time, Clearing_rate, Matched_qty,
        Delivery_time, Trans_type
    ):
        """
        Adds a transaction to the list.

        Parameters
        ----------
        Trans_id : str
            Unique transaction ID.
        Buyer, Seller : str
            Names or identifiers of buyer and seller.
        Buyer_id, Seller_id : str
            Unique user IDs for buyer and seller.
        Unit_area : str
            Area where the device exist.
        Bid_id, Offer_id : str
            Unique IDs for the matched bid and offer.
        Bid_qty, Offer_qty, Matched_qty : float
            Quantities involved in the bid, offer, and transaction.
        Bid_rate, Offer_rate, Clearing_rate : float
            Prices offered, asked, and finally cleared.
        Bid_time, Offer_time, Delivery_time : str or datetime
            Timestamps related to bidding, offering, and delivery.
        Trans_type : str
            Either "Buying" or "Selling" to indicate buyer or seller record.

        Returns
        -------
        int
            Index of the transaction added.
        """
        new_trans = (
            Trans_id, Buyer, Buyer_id, Unit_area, Bid_id, Bid_qty, Bid_rate,
            Bid_time, Seller, Seller_id, Offer_id, Offer_qty, Offer_rate,
            Offer_time, Clearing_rate, Matched_qty, Delivery_time, Trans_type
        )
        self.trans.append(new_trans)
        self.n_trans += 1
        return self.n_trans - 1

    def get_df(self):

        return pd.DataFrame(self.trans, columns=self.name_col)

    def merge(self, other):

        assert isinstance(other, TransactionManager), "Must merge with another TransactionManager"

        merged = TransactionManager()
        for t in self.trans:
            merged.add_transaction(*t)
        for t in other.trans:
            merged.add_transaction(*t)

        return merged

    def __repr__(self):
        return f"<TransactionManager: {self.n_trans} transactions>"
