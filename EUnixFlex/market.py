from .auctions.orders import OrderManager
from EUnixFlex.mechanisms import *


MECHANISM = {

    'flex': FlexibilityClearing,
}




class Market():
 
    def __init__(self):
        """TODO: to be defined."""
        self.bm = OrderManager()
        
        

    def accept_order(self, *args):
       
        """Adds
        
        """
        order_id = self.bm.add_order(*args)
        return order_id



    def get_oders(self):
        """get the bids and offers

        

        
        """
        df = self.bm.get_df()
        return df



    def run(self, algo, *args, **kwargs):
        """Runs 

        
        """
        df = self.bm.get_df()
        mec = MECHANISM[algo](df, *args, **kwargs)
        transactions, extra = mec.run()
        self.transactions = transactions
        self.extra = extra
        return transactions, extra

    