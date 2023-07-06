import pandas as pd

data = pd.read_excel('NBA-2022-2023.xlsx')

# Filter the data to include rows where the position is 'C', 'C-F', or 'F-C'
center_data = data[data['POSITION'].isin(['C', 'C-F'])].copy()

# Select the column headers
column_headers = center_data.columns.tolist()

# Print the column headers
print(column_headers)
