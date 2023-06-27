# %%
import sqlite3
import pandas as pd

con = sqlite3.connect("proj6_readings.sqlite")
cur = con.cursor()
result = cur.execute("SELECT count(*) from readings;").fetchall()
df = pd.DataFrame(result)
df

# %%
df = pd.read_sql("SELECT count(*) from readings;", con)
df

# %%
df_ex_1 = pd.read_sql("SELECT count(DISTINCT detector_id) from readings;", con)

import pickle
with open("proj6_ex01_detector_no.pkl", "wb") as ex1:
    pickle.dump(df_ex_1, ex1)

# %%
df_ex_2 = pd.read_sql("SELECT detector_id, count(count), min(starttime), max(starttime) from readings group by detector_id;", con)

with open("proj6_ex02_detector_stat.pkl", "wb") as ex2:
    pickle.dump(df_ex_2, ex2)

# %%
df_ex_3 = pd.read_sql("SELECT detector_id, count, LAG(count) OVER (ORDER BY starttime) AS prev_count from readings where detector_id=146 LIMIT 500;", con)

with open("proj6_ex03_detector_146_lag.pkl", "wb") as ex3:
    pickle.dump(df_ex_3, ex3)

# %%
df_ex_4 = pd.read_sql("SELECT detector_id, count, SUM(count) OVER (ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING) AS window_sum from readings where detector_id=146 LIMIT 500;", con)

with open("proj6_ex04_detector_146_sum.pkl", "wb") as ex4:
    pickle.dump(df_ex_4, ex4)


