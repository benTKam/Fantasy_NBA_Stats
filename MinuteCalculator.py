
import pandas as pd

# Read data from the Excel file
file_path = "NBA-2022-2023.xlsx"
#sheet_name = "NBA_Data"
df = pd.read_excel(file_path)
df = df[df["MIN"] >= 30]
# Define a function to extract the primary position
def extract_primary_position(position):
    positions = position.split("-")
    return positions[0] if len(positions) > 1 else position

# Apply the function to create a new column 'PRIMARY_POSITION'
df['PRIMARY_POSITION'] = df['POSITION'].apply(extract_primary_position)

# Map non-main positions to 'O' (Other)
main_positions = ['C', 'G', 'F']
df['PRIMARY_POSITION'] = df['PRIMARY_POSITION'].apply(lambda x: x if x in main_positions else 'O')

# Calculate the league averages for each category for each position
league_avg = df.groupby('PRIMARY_POSITION')[['3P', 'FG', 'FT', 'REB', 'A', 'BL', 'ST']].mean().reset_index()

# Group by "OPPONENT TEAM" and "PRIMARY_POSITION" to calculate the opponent's performance
opponent_performance = df.groupby(['OPPONENT TEAM', 'PRIMARY_POSITION'])[['3P', 'FG', 'FT', 'REB', 'A', 'BL', 'ST']].mean().reset_index()

# Merge the opponent's performance with league averages
merged_df = pd.merge(opponent_performance, league_avg, on='PRIMARY_POSITION', suffixes=('_opponent', '_league'))

# Calculate multipliers for each category based on opponent performance and league averages
categories = ['3P', 'FG', 'FT', 'REB', 'A', 'BL', 'ST']
for category in categories:
    merged_df[f'{category}_multiplier'] = merged_df[f'{category}_opponent'] / merged_df[f'{category}_league']

pivoted_df = merged_df.pivot(index=['OPPONENT TEAM', 'PRIMARY_POSITION'], columns='PRIMARY_POSITION', values=['3P', 'FG', 'FT', 'REB', 'A', 'BL', 'ST'] + [f'{category}_multiplier' for category in categories])

# Reset the index to have a clean DataFrame
pivoted_df.reset_index(inplace=True)

# Export the results to an Excel spreadsheet
output_file = "fantasy_multipliers.xlsx"
pivoted_df.to_excel(output_file, index=False, header=True)

print(f"Results exported to {output_file}")




