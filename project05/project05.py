# %%
import json

with open('proj5_params.json', 'r') as f:
    params = json.load(f)

params

# %%
import pandas as pd

df = pd.read_csv('proj5_timeseries.csv')
df['date'] = pd.to_datetime(df['Date'])
df.index = df['date']
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace('[^a-z]', '_')
df = df.drop('date', axis=1)
df

# %%
df = df.asfreq(params['original_frequency'])

# %%
import pickle

with open('proj5_ex01.pkl', 'wb') as f:
    pickle.dump(df, f)

# %%
df_target_fq = df.asfreq(params['target_frequency'])
df_target_fq

# %%
with open('proj5_ex02.pkl', 'wb') as f2:
    pickle.dump(df_target_fq, f2)

# %%
interval = str(params['downsample_periods']) + params['downsample_units']
df_downsampled = df.resample(interval).sum(min_count=params['downsample_periods'])
df_downsampled

# %%
with open('proj5_ex03.pkl', 'wb') as f3:
    pickle.dump(df_downsampled, f3)

# %%
interval = str(params['upsample_periods']) + params['upsample_units']
df_upsampled = df.resample(interval).interpolate(method=params['interpolation'], order=params['interpolation_order'])
df_upsampled

# %%
original_timedelta = pd.Timedelta(value=1, unit=params['original_frequency'])
upsampled_timedelta = pd.Timedelta(value=params['upsample_periods'], unit=params['upsample_units'])

df_upsampled *= upsampled_timedelta/original_timedelta
df_upsampled

# %%
with open('proj5_ex04.pkl', 'wb') as f4:
    pickle.dump(df_upsampled, f4)

# %%
sensors_df = pickle.load(open('proj5_sensors.pkl', 'rb'))
sensors_df.head()

# %%
sensors_df = sensors_df.pivot(columns='device_id', values='value')
sensors_df

# %%
interval = str(params['sensors_periods']) + params['sensors_units']
new_index = pd.date_range(sensors_df.index.round(interval).min(), sensors_df.index.round(interval).max(), freq=interval)
# sensors_df = sensors_df.resample(interval).mean()
# sensors_df

# %%
sensors_unified_index = sensors_df.reindex(new_index.union(sensors_df.index)).interpolate()

# %%
sensors_reindexed = sensors_unified_index.reindex(new_index)

# %%
sensors_reindexed.dropna(inplace=True)
sensors_reindexed

# %%
with open('proj5_ex05.pkl', 'wb') as f5:
    pickle.dump(sensors_reindexed, f5)

# %%



