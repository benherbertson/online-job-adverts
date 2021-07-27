# Load packages
import requests
import pandas as pd
import os.path
from bs4 import BeautifulSoup as bs
from datetime import date

# Load all web pages
url_base = 'https://www.adzuna.com.au/'

industry_urls = ['hospitality-catering', 'graduate', 'trade-construction',
                 'healthcare-nursing', 'retail', 'travel',
                 'logistics-warehouse', 'teaching']

industry_jobs = []

for industry in industry_urls:
    url = url_base + industry + '-jobs'
    response = requests.get(url)
    soup = bs(response.content, features='html.parser')
    total_jobs_title = soup.find('title')
    total_jobs_str = str(total_jobs_title.string)
    industry_jobs.append(total_jobs_str)

# Save as DataFrame
today = date.today()
df = pd.DataFrame({'date': today, 'jobs': industry_jobs, 'industry': industry_jobs})
df['date'] = pd.to_datetime(df['date'])

# Clean columns
df['jobs'] = df['jobs'].str.replace(
    '[a-zA-Z]|,|&| Jobs in Australia \\| Adzuna', '', regex=True)
df['jobs'] = pd.to_numeric(df['jobs'])
df['industry'] = df['industry'].str.replace(
    '[0-9]|,| Jobs in Australia \\| Adzuna', '', regex=True)
df['industry'] = df['industry'].str.lstrip(' ')

# Here we check whether a file containing previously scraped data exists
# If previous file already exists, then read it in and amend with new data
# If not, create a new file
output = 'data/by_industry.csv'

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