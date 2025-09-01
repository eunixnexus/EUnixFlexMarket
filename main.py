import os
import pandas as pd


from EUnixFlex.simulation import Simulation as sm

marktSlots = "timeslot" 
curr_dir = os.path.dirname(__file__)


data = pd.read_csv(os.path.join(curr_dir, "data/"+str(marktSlots)+'.csv'), delimiter=',')



Nslot = 94
startSlot = "2014-12-01T00:00"
grid_fee = 3 #grid fee in cent/kWh - will be updated
simu = sm(data,startSlot, Nslot, "flex", grid_fee) #mechanism can be "uniform", "p2p"

prev_slot, index = simu.simulate()
simu.closeSimulation(prev_slot, index)



