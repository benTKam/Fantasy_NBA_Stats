import pandas as pd

data = pd.read_excel('Joel_Embiid_Predicted_Stats.xlsx')

# Filter the data to include rows where the position is 'C', 'C-F', or 'F-C'


# Select the column headers
column_headers = data.columns.tolist()

# Print the column headers
print(column_headers)
