import pandas as pd
import numpy as np

data = ['total', 'remote', 'work_from_home', 'by_state', 'by_industry']
j = 0

for i in data:
    df = pd.read_csv('data/' + data[j] + '.csv', parse_dates=['date'])
    # Filter July rows
    df_july = df[df['date'].dt.strftime('%Y-%m') == '2021-07']
    if i == 'by_state' or i == 'by_industry':
        if i == 'by_state':
            col = 'state'
        else:
            col = 'industry'
        # Calculate mean by state/industry
        means = df_july.groupby(col).mean()
        means.rename(columns={'jobs': 'mean_jobs'}, inplace=True)
        df_means = pd.merge(df, means, how='left', left_on=col,
                            right_index=True)
        df_index = df_means['jobs'] / df_means['mean_jobs'] * 100
    else:
        # Calculate mean jobs
        mean_count = np.mean(df_july['jobs'])
        df_index = df['jobs'] / mean_count * 100
    df['jobs'] = df_index
    df['jobs'] = df['jobs'].round(1)
    df.to_csv('data/index/' + data[j] + '.csv', index=False)
    j += 1