import pandas as pd


class OrderManager:
    """
    Manages a collection of market orders (bids and offers) in a structured format.

    Attributes
    ----------
    col_names : list of str
        Column names for the DataFrame representing stored orders.
    n_orders : int
        Counter for total number of orders added.
    orders : list of tuple
        List of all orders added to the manager.
    """

    col_names = [
        'User',
        'User_id',
        'Unit_area',
        'Order_id',
        'energy_qty',
        'energy_rate',
        'bid_offer_time',
        'delivery_time',
        'type',  
        'attributes',
        'requirements',
        'power[kW]',
        'area',
        'direction',
    ]

    def __init__(self):
        """Initializes the OrderManager with no orders."""
        self.n_orders = 0
        self.orders = []

    def add_order(
        self,
        User,
        User_id,
        Unit_area,
        Order_id,
        energy_qty,
        energy_rate,
        bid_offer_time,
        delivery_time,
        type,  
        attributes=None,
        requirements=None,
        power=0,
        area=None,
        direction=None
    ):
        """
        Adds a single bid or offer to the order list.

        Parameters
        ----------
        User : str
            Name or ID of the submitting user.
        User_id : str
            Unique identifier for the user.
        Unit_area : str
            Area or location of the user/unit.
        Order_id : str
            Unique order ID.
        energy_qty : float
            Quantity of energy in kWh.
        energy_rate : float
            Bid or offer price in €/kWh.
        bid_offer_time : str or datetime
            Timestamp when the bid/offer is placed.
        delivery_time : str or datetime
            Scheduled time for energy delivery.
        type : bool
            True for bid (buy), False for offer (sell).
        attributes : optional
            Optional metadata or bid tags.
        requirements : optional
            Optional requirements for the transaction.
        power : float, default=0
            Power associated with the order in kW.
        area : optional
            Optional area field.
        direction : optional
            Optional direction indicator (e.g., import/export).

        Returns
        -------
        int
            Index of the added order (zero-based).
        """
        new_order = (
            User, User_id, Unit_area, Order_id, energy_qty, energy_rate,
            bid_offer_time, delivery_time, type, attributes,
            requirements, power, area, direction
        )

        self.orders.append(new_order)
        self.n_orders += 1
        return self.n_orders - 1

    def get_df(self):
        """
        Returns all stored orders as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame of all stored orders.
        """
        return pd.DataFrame(self.orders, columns=self.col_names)
