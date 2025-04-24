import pandas as pd

df = pd.read_csv('goodreads_library_export.csv', delimiter=',', encoding='utf-8')

for col in df.columns.tolist():
    print(f'- {col}')

df = df.rename(columns={'My Rating': 'Rating'})
df = df.rename(columns={'My Review': 'Review'})

with_reviews = df.query('`Read Count` > 0 & `Rating` > 0 & `Review`.notna()')
reviews = with_reviews[['ISBN13', 'Title','Review','Rating']]

print(reviews)

reviews.to_csv('goodreads_cleaned.csv', index=False,  encoding='utf-8')