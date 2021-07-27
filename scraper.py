# Load packages
import requests
import pandas as pd
import os.path
from bs4 import BeautifulSoup as bs
from datetime import date

# Load web page content
# Web pages to scrape
webpages = ['https://www.adzuna.com.au/search?w=australia',
            'https://www.adzuna.com.au/work-from-home',
            'https://www.adzuna.com.au/search?remote_only=1']
# For looping through URLs above and writing files
j = 0

for i in webpages:
    r = requests.get(webpages[j])

    # Convert to Beautiful Soup object
    webpage = bs(r.content, features='html.parser')

    # Extract text and convert to str type
    total_jobs_title = webpage.find('title')
    total_jobs_str = str(total_jobs_title.string)

    # Create empty DataFrame then add today's date and job count
    df = pd.DataFrame(columns=['date', 'jobs'], index=['0'])
    today = date.today()
    df['date'] = today
    df['date'] = pd.to_datetime(df['date'])

    # Put scraped data into DataFrame
    df['jobs'] = total_jobs_str

    # Clean column and make numeric
    df['jobs'] = df['jobs'].str.replace(
        '[a-zA-Z]|,|&| Work From Home| Jobs in Australia \\| Adzuna', '',
        regex=True)
    df['jobs'] = pd.to_numeric(df['jobs'])

    # Check whether a file containing previously scraped data exists
    # If previous file already exists, then read it in and amend with new data
    # If not, create a new file
    folder = 'data'
    output = [folder + '/total.csv',
              folder + '/work_from_home.csv',
              folder + '/remote.csv']

    if os.path.isfile(output[j]):
        # Read in existing data
        df_hist = pd.read_csv(output[j], parse_dates=['date'])

        # Add latest jobs data
        df_updated = pd.concat([df_hist, df])

        # Write updated file
        df_updated.to_csv(output[j], index=False)
        # For scraping next URL and writing file
        j += 1
    else:
        # Write new file
        df.to_csv(output[j], index=False)
        j += 1