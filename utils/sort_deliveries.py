import pandas as pd
import numpy as np
from datetime import datetime

path = "/data/"
result_path = "/data_result/"
df = pd.read_csv(path + "delivery_events.csv")
df['scheduled_datetime'] = pd.to_datetime(df['scheduled_datetime'])
df['actual_datetime'] = pd.to_datetime(df['actual_datetime'])
df['on_time_flag'] = df['on_time_flag'].astype('boolean')
df_2025 = df[
    (df['scheduled_datetime'] >= '2024-01-01') &
    (df['scheduled_datetime'] < '2024-04-19')
]
df_2025["scheduled_datetime"] = df_2025["scheduled_datetime"] + pd.DateOffset(years=2)
df_2025["actual_datetime"] = df_2025["actual_datetime"] + pd.DateOffset(years=2)
df_2025.loc[df_2025['actual_datetime'] > datetime.now(), 'detention_minutes'] = np.nan
df_2025.loc[df_2025['actual_datetime'] > datetime.now(), 'on_time_flag'] = pd.NA
df_2025.loc[df_2025['actual_datetime'] > datetime.now(), 'actual_datetime'] = pd.NaT

print(df_2025)

# duplicate_rows = df_2025[df_2025['load_id'].duplicated()]
# print(duplicate_rows)

df_2025.to_csv(result_path+'delivery_events_result.csv')