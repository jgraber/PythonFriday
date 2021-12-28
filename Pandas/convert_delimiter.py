import pandas as pd

# reads file with ; as delimiter
df = pd.read_csv('input.csv', delimiter=';')
# writes file with , as delimiter (, is default value)
df.to_csv('output_converted.csv', index=False)