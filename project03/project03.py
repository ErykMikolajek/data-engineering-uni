# %%
import pandas as pd
import numpy as np

df1 = pd.read_json('proj3_data1.json')
df2 = pd.read_json('proj3_data2.json')
df3 = pd.read_json('proj3_data3.json')

df = df1.append(df2, ignore_index=True)
df = df.append(df3, ignore_index=True)
df


# %%
df.to_json('ex01_all_data.json', orient='records', indent=4)

# %%
missing_values = {}
for col in df.columns:
    num_missing = df[col].isna().sum()
    if num_missing > 0:
        missing_values[col] = num_missing

# %%
df_missing_values = pd.DataFrame.from_dict(missing_values, orient='index')
df_missing_values.to_csv('ex02_no_nulls.csv', header=False)

# %%
import json
with open('proj3_params.json', 'r') as file:
    params = json.load(file)
params

# %%
def add_description(row):
    description = ''
    for name in params['concat_columns']:
        description += row[name] + ' '
    description = description[:-1]
    return description

df['description'] = df.apply(add_description, axis=1)
df

# %%
df.to_json('ex03_descriptions.json', orient='records', indent=4)

# %%
df_more_data = pd.read_json('proj3_more_data.json')

# %%
df = df.join(df_more_data.set_index(params['join_column']), on=params['join_column'], how='left')
df

# %%
df.to_json('ex04_joined.json', orient='records', indent=4)

# %%
for i, row in df.iterrows():
    filename = 'ex05_' + row['description'].lower().replace(' ', '_') + '.json'
    row_to_file = row.drop('description')
    row_to_file.to_json(filename, orient='index', indent=4)

# %%
for i, row in df.iterrows():
    filename = 'ex05_int_' + row['description'].lower().replace(' ', '_') + '.json'
    row_to_file = row.drop('description')
    for col_name in params['int_columns']:
        if row_to_file[col_name] == row_to_file[col_name]:
            row_to_file[col_name] = int(row_to_file[col_name])
    row_to_file.to_json(filename, orient='index', indent=4)

# %%
agg_dict = {}
for col_name, func in params['aggregations']:
    field_name = func + '_' + col_name
    agg_dict[field_name] = df[col_name].aggregate(func)

# %%
with open("ex06_aggregations.json", "w") as agg_file:
    json.dump(agg_dict, agg_file, indent=4)

# %%
grouped_df = df.groupby(params['grouping_column']).filter(lambda x: len(x) > 1)
grouped_df = grouped_df.groupby(params['grouping_column']).aggregate('mean')
grouped_df

# %%
grouped_df.to_csv('ex07_groups.csv')

# %%
pivoted_df = df.pivot_table(index=params['pivot_index'], columns=params['pivot_columns'], 
                            values=params['pivot_values'], aggfunc='max')
pivoted_df

# %%
import pickle
with open('ex08_pivot.pkl', 'wb') as pivoted_pickle:
    pickle.dump(pivoted_df, pivoted_pickle)

# %%
melted_df = df.melt(id_vars=params['id_vars'])
melted_df

# %%
melted_df.to_csv('ex08_melt.csv', index=False)

# %%
statistics_df = pd.read_csv('proj3_statistics.csv')
statistics_df

# %%
melted_df = statistics_df.melt(id_vars=['Country'])
melted_df[['Brand', 'Year']] = melted_df['variable'].str.split('_', expand=True)
melted_df = melted_df.drop(columns=['variable'])
pivoted_df = melted_df.pivot_table(index=['Country', 'Year'], columns='Brand', values='value')
pivoted_df


# %%
with open('ex08_stats.pkl.', 'wb') as cars_years_pickle:
    pickle.dump(pivoted_df, cars_years_pickle)


# %%



