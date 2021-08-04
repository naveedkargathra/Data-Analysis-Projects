import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Finding the Total Cost by Aircraft Type for the entire year and the Aircraft Type with the lowest cost per seat per km

#Import excel sheets for Operations, AC Characteristics, City_pairs
operations = pd.read_excel(io="Data Science Case study Vindiata.xlsx", sheet_name= "Operations", header=3, index_col=1)
AC_char = pd.read_excel(io="Data Science Case study Vindiata.xlsx", sheet_name= "AC characteristics", header=3, index_col=1)
city_pairs = pd.read_excel(io="Data Science Case study Vindiata.xlsx", sheet_name= "City pairs", header=3, index_col=1).reset_index()

# Dropping Null values and renaming columns
operations = operations.dropna(axis=1)
AC_char = AC_char.dropna(axis=1)
city_pairs = city_pairs.dropna(axis=1)

operations.columns = ["Aircraft Type","Jan","Feb","Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

city_pairs.columns = ["Origin", "Destination","Passengers","Distance"]

# Aggregating Operations table for Airline A by Hours Flown for the entire year for each aircraft type.
months = operations.columns[1:]
operations=operations.groupby(["Aircraft Type"]).sum()
operations["Hours Flown"]= operations[months].sum(axis=1)


# Joining the Operations and AC Characteristics Table on Aircraft Type and keeping the relevant columns
lowest_cost = operations.join(AC_char, lsuffix='_caller', rsuffix='_other')
lowest_cost= lowest_cost[["Hours Flown","Costs per flight hour","Number of Seats", "Ave. Speed (km/h)","Range (Km)"]].reset_index()

# Calculating Total Cost for each Aircraft Type 
# Total Cost = Hours Flown * Cost per flight hour
lowest_cost["Total Costs"] = lowest_cost["Hours Flown"] * lowest_cost["Costs per flight hour"] 

low_cost_figure = plt.bar(x=lowest_cost["Aircraft Type"], height=lowest_cost["Total Costs"])
plt.show()
# Calculating the Cost per Hour per Km by Aircraft Type
# Cost per Seat per Km = Total Costs/(Number of Seats * Hours Flown * Average Speed)
lowest_cost["Cost per seat per km"] = round(lowest_cost["Total Costs"]/(lowest_cost["Number of Seats"]*lowest_cost["Hours Flown"]*lowest_cost["Ave. Speed (km/h)"]),4)
lowest_cost = lowest_cost.sort_values("Cost per seat per km", ascending=True)
print(lowest_cost)
print(f"The lowest Cost per seat per km is of Aircraft Type {lowest_cost.index[0]}")


# Finding the most optimal Aircraft Type for each City-Pair by Range, Passenger Demand and Cost

# Modifying the lowest_cost table to keep relevant columns
cost = lowest_cost.drop(['Hours Flown', 'Costs per flight hour', 'Total Costs',"Ave. Speed (km/h)"],axis=1).reset_index()

# Iterating over city pairs table and generating the cost for each aircraft type for each city pair.
# lowest cost = (cost per seat per km * number of seats * distance * number of trips)
# number of trips = passengers/number of seats
for source,destination,passengers,distance in city_pairs.itertuples(index=False):
    cost[source + "-" + destination + ' cost'] = np.where(cost["Range (Km)"] >= distance, (cost["Cost per seat per km"] * cost["Number of Seats"] * distance * np.ceil(passengers/cost["Number of Seats"])).astype(int), "NaN")

# Finding the most optimal aircraft type for each city pair 
AA_BB = cost.sort_values("AA-BB cost", ascending=True).iloc[0,0]
BB_CC = cost.sort_values("BB-CC cost", ascending=True).iloc[0,0]
CC_AA = cost.sort_values("CC-AA cost", ascending=True).iloc[0,0]
AA_DD = cost.sort_values("AA-DD cost", ascending=True).iloc[0,0]

optimal = pd.DataFrame(columns=["Optimal Flight","No. of Trips"])
optimal["Optimal Flight"] =[AA_BB,BB_CC,CC_AA,AA_DD]
optimal["No. of Trips"] = np.ceil(city_pairs["Passengers"]/cost["Number of Seats"])

print(optimal)
print(f"The most optimal flights for city-pairs AA-BB, BB-CC, CC-DD, AA-DD are {AA_BB}, {BB_CC}, {CC_AA}, {AA_DD} respectively ")





