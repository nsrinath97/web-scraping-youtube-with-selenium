import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
yt_trending_df = pd.read_csv('youtube trending videos.csv', sep='|', parse_dates=['Time'])
print(yt_trending_df)


