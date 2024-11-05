import pandas as pd
from datetime import date

d = {'Date': [date(2024, 10, 29), date(2024, 10, 30), date(2024, 10, 31)], 
     'JetPack': [347, 362, 251],
     'Statify': [499, 480, 346],
     'WP Statistics': [493, 476, 343],}
df = pd.DataFrame(data=d)
print(df)

# Only when Index is set to a column we need
# df = df.reset_index()

df_melted = df.melt(id_vars="Date",
        var_name="Tool", 
        value_name="Visitors")
print(df_melted)
