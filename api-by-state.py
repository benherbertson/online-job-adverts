# Load packages
import requests
import pandas as pd
import numpy as np
import os.path
from datetime import date

# Returns number of jobs by state/territory
resp = requests.get(
    "https://api.adzuna.com/v1/api/jobs/au/geodata?app_id=61b4311d&app_key=a32a52eca3a52dd359685294182ee67d&content-type=application/json"
)

# Create new dictionary with total number of jobs by state/territory
d = {}
j = np.arange(8)  # total number of states and territories to retrieve

for i in j:
    d[resp.json()['locations'][i]['location']['display_name']] = resp.json()['locations'][i]['count']

# Convert to DataFrame
df = pd.DataFrame(list(d.items()), columns=['state', 'jobs'])

# Strip ', Australia' from names of states and territories
df['state'] = df['state'].str.replace(', Australia', '')

# Add date and make date column datetime type
today = date.today()
df['date'] = today
df['date'] = pd.to_datetime(df['date'])

# Reorder columns
df = df.reindex(columns=['date', 'jobs', 'state'])

# Here we check whether a file containing previously scraped data exists
# If previous file already exists, then read it in and amend with new data
# If not, create a new file
output = 'data/by_state.csv'

if os.path.isfile(output):
    # Read in existing data
    df_hist = pd.read_csv(output, parse_dates=['date'])

    # Add latest jobs data
    df_updated = pd.concat([df_hist, df])

    # Write updated file
    df_updated.to_csv(output, index=False)
else:
    # Write new file
    df.to_csv(output, index=False)