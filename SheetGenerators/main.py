import pandas as pd

# Read the Excel sheet into a pandas DataFrame
data = pd.read_excel('PlayerStats/NBA-2022-2023.xlsx')

# Filter the data to include rows where the position is 'C', 'C-F', or 'F-C'
center_data = data[data['POSITION'].isin(['C', 'C-F'])].copy()

# Filter the data to include rows where the position is 'G'
guard_data = data[data['POSITION'].isin(['G', 'G-F'])].copy()

# Filter the data to include rows where the position is 'F', 'F-C', or 'F-G'
forward_data = data[data['POSITION'].isin(['F', 'F-C', 'F-G'])].copy()

# Define weights for each statistical category
weights = {
    '3P': 3,
    'FG': 2,
    'FT': 1,
    'REB': 1.2,
    'A': 1.5,
    'BLK': 3,
    'STL': 3,
    'TO': -1
}

# Calculate the weighted score for centers
center_data['SCORE'] = (
    center_data['3P'] * weights['3P'] +
    center_data['FG'] * weights['FG'] +
    center_data['FT'] * weights['FT'] +
    center_data['DR'] * weights['REB'] +
    center_data['OR'] * weights['REB'] +
    center_data['A'] * weights['A'] +
    center_data['BL'] * weights['BLK'] +
    center_data['ST'] * weights['STL'] +
    center_data['TO'] * weights['TO']
)
center_data = center_data[center_data['MIN'] >= 25]
# Group the data by the opponent team and calculate the mean score for each position
center_opponent_stats = center_data.groupby('OPPONENT \nTEAM')['SCORE'].mean()

# Calculate the average points, offensive rebounds, defensive rebounds, blocks, assists, turnovers, and steals given up to a center for each team
team_stats = center_data.groupby('OPPONENT \nTEAM')[['3P', 'FG', 'FT', 'OR', 'DR', 'BL', 'A', 'TO', 'ST']].mean()

# Calculate the league average for each statistical category
league_avg_stats = center_data[['3P', 'FG', 'FT', 'OR', 'DR', 'BL', 'A', 'TO', 'ST']].mean()

# Calculate the division of each team's stats by the league average
team_stats_divided = team_stats.divide(league_avg_stats)

# Merge the team_stats_divided DataFrame with the center_opponent_stats DataFrame
team_scores = pd.merge(team_stats_divided, center_opponent_stats, left_index=True, right_index=True)

# Calculate the average score for each team against the league average score
team_scores['Center Score vs. League Avg'] = team_scores['SCORE'] / center_opponent_stats.mean()

# Export the team_scores DataFrame to an Excel file
team_scores.to_excel('CenterVsLeague.xlsx', index=True)