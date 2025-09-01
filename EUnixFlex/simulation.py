import time
import EUnixFlex as mp
from EUnixFlex.redisconnection.publish import ProcessSlots as pps
from EUnixFlex.transactions import stats
import pandas as pd


class Simulation():
 
    def __init__(self, data, startSlot = None, steps = 96, mmc = "p2p", grid_fee = 0):
        """TODO: to be defined."""
        self.pub_ins = pps(data,startSlot, steps)
        self.simu_slots=self.pub_ins.get_timeSlot()
        self.mmc = mmc
        self.grid_fee = grid_fee


    def mach_function(self, prev_step):
        
        bid_offer_data = self.pub_ins.read_from_redis(prev_step) #Read market bids and offers data time
        
        if bid_offer_data is None:
            print(f"No Bid or Offer data received for slot {prev_step}")
            return  

        #print(bid_offer_data)
        mar= mp.Market()

        for record in bid_offer_data:
                # Adjust price for offers only
            if record['Type'] is False:  # Offer
                adjusted_rate = record['energy_rate'] + self.grid_fee
            else:  # Bid
                adjusted_rate = record['energy_rate']
            mar.accept_order(
                record["User"],           # User
                record['User_id'],        # User_id 
                record['Unit_area'],      # User_area
                record['Order_id'],       # Order_id
                record['energy_qty'],     # energy_qty
                adjusted_rate,    # energy_rate
                record['bid-offer-time'], # bid-offer-time
                record['delivery-time'],  # delivery-time
                record['Type']            # Type
        )
            
        #orders = mar.get_oders()
        #print(orders)
        transactions, extras = mar.run(self.mmc) #Match bids and offers time
        trans_df = transactions.get_df()
        if trans_df.empty:
            print("The results is empty.")
        else:
            #Update grid fees
            trans_df["User Rate"] = trans_df.apply(lambda row: row["Clearing_rate"] 
            if row["Trans_type"] == "Buying" else row["Clearing_rate"] - self.grid_fee,
            axis=1)
            trans_df["Offer_rate"] = pd.to_numeric(trans_df["Offer_rate"], errors="coerce")
            trans_df["Offer_rate"] = trans_df["Offer_rate"].apply(lambda x: x - self.grid_fee if pd.notnull(x) else x)
            
            trans_stat = stats.compute_statis(trans_df)
            print(trans_stat)#Calculate and publish statistics
            json_data_res = trans_df.to_json(orient='records', indent=4)
            for unit_area, group_df in trans_df.groupby("Unit_area"):
                result_json = group_df.to_json(orient='records')
                key = f"market_result:{unit_area}:{prev_step}"
                self.pub_ins.send_to_redis(key, result_json)
                
            self.pub_ins.send_to_redis("simulation result", json_data_res)
            self.pub_ins.send_to_redis(f"result statistics:{prev_step}", trans_stat)            
            print(f"The result of {prev_step} is stored in the exchange")
        return



    def simulate(self):
        for index, row in self.simu_slots.iterrows():
            slot = (row['Datetime']).isoformat()
            self.pub_ins.publish_slot(slot, index, "Begin") #start new  market slot
            if index ==0:
                prev_slot = slot
                continue

            self.mach_function(prev_slot) #Match previous slot
            self.pub_ins.publish_slot(prev_slot, index, "Results") #Market  slot ends and results published


            prev_slot = slot
            time.sleep(1)
        return prev_slot, index
        
    
    def closeSimulation(self, prev_slot, index):
        self.mach_function(prev_slot)
        self.pub_ins.publish_slot(prev_slot, index, "Results") #Publication of last results announcement
        time.sleep(1)
        self.pub_ins.publish_slot("End", index +1, "end")

        output_results = self.pub_ins.read_from_redis("simulation result")
        self.pub_ins.json_to_csv(output_results, "output.csv")
        print("End of Simulation")
        self.pub_ins.delete_from_redis("registraion")


