import pandas as pd
from datetime import date

d = {'Date': [date(2024, 10, 29), date(2024, 10, 30), date(2024, 10, 31)], 
     'JetPack (Visitors)': [347, 362, 251],
     'Statify': [499, 480, 346],
     'WP Statistics (Visitors)': [493, 476, 343],}
df = pd.DataFrame(data=d)
print(df)

df = df.rename({'Jetpack (Visitors)': 'Jetpack', 
                'WP Statistics (Visitors)': 'WP Statistics'}, 
                axis=1)
print(df)
