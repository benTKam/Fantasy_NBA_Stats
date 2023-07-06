import pandas as pd

data = pd.read_excel('PlayerStats/NBA-2022-2023.xlsx')

# Filter the data to include rows where the position is 'C', 'C-F', or 'F-C'
center_data = data[data['POSITION'].isin(['C', 'C-F', 'F-C'])].copy()

# Select the columns for statistical categories
stat_columns = ['3P', 'FG', 'FT', 'OR', 'DR', 'BL', 'A', 'TO', 'ST']

# Convert the columns to numeric values
center_data[stat_columns] = center_data[stat_columns].apply(pd.to_numeric, errors='coerce')

# Group by player and calculate the sum of statistical categories
total_stats = center_data.groupby('PLAYER ')[stat_columns].sum()

# Calculate the games played for each player based on the number of times they appear in the data
total_stats['Games Played'] = center_data.groupby('PLAYER ')['PLAYER '].count()

# Calculate the per game averages by dividing the total stats by the 'Games Played' column
per_game_averages = total_stats.div(total_stats['Games Played'], axis=0)

# Reset the index of per_game_averages
per_game_averages = per_game_averages.reset_index()

# Define the weights for fantasy scoring
weights = {
    '3P': 3,
    'FG': 2,
    'FT': 1,
    'DR': 1.2,
    'OR': 1.2,
    'A': 1.5,
    'BL': 3,
    'ST': 3,
    'TO': -1
}

# Calculate the weighted score for centers
per_game_averages['SCORE'] = (
    per_game_averages['3P'] * weights['3P'] +
    per_game_averages['FG'] * weights['FG'] +
    per_game_averages['FT'] * weights['FT'] +
    per_game_averages['DR'] * weights['DR'] +
    per_game_averages['OR'] * weights['OR'] +
    per_game_averages['A'] * weights['A'] +
    per_game_averages['BL'] * weights['BL'] +
    per_game_averages['ST'] * weights['ST'] +
    per_game_averages['TO'] * weights['TO']
)

per_game_averages = per_game_averages.round(1)
# Export the per game averages with fantasy scores to an Excel sheet
per_game_averages.to_excel('CentersPerGameTotals.xlsx', index=False)
