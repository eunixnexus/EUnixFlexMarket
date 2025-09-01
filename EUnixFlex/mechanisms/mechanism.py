import pandas as pd

from EUnixFlex.auctions.process import merge_same_price
from EUnixFlex.transactions.processing import split_transactions_merged_players
from EUnixFlex.transactions.transactions import TransactionManager
from collections import OrderedDict



class Mechanism():

    """
    """

    def __init__(self, algo, orders, *args, merge=False, **kwargs):
        """Creates a mechanisms with bids

        """
        self.algo = algo
        self.args = args
        self.kwargs = kwargs
        self.merge = merge
        self.orders = self._sanitize_bids(orders)

    def _sanitize_bids(self, orders):
        """

        """
        if self.merge:
            self.old_orders = orders
            new_orders, maping = merge_same_price(orders)
            
            self.maping = maping
        else:
            new_orders = orders

        return new_orders

    def _run(self):
        """Runs the mechanisms"""
        orders = self.orders
        N = orders.shape[0]

        if (orders.loc[orders['type']].shape[0] not in [0, N]):

            trans, extra = self.algo(self.orders, *self.args, **self.kwargs)
            return trans, extra
        else:

            trans = TransactionManager()
            return trans, OrderedDict()

    def _cleanup(self, trans):
        """

        """

        if self.merge:
            trans = split_transactions_merged_players(
                trans, self.old_bids, self.maping)

        return trans

    def run(self):

        """Runs the mechanisms"""
        trans, extra = self._run()

        trans = self._cleanup(trans)
        return trans, extra
