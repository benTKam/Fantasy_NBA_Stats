import pandas as pd

# Read the Excel sheet into a pandas DataFrame
data = pd.read_excel('NBA-2022-2023.xlsx')

# Filter the data to include rows where the position is 'C', 'C-F', or 'F-C'
center_data = data[data['POSITION'].isin(['C', 'C-F'])].copy()

# Filter the data to include rows where the position is 'G'
guard_data = data[data['POSITION'].isin(['G', 'G-F'])].copy()

# Filter the data to include rows where the position is 'F', 'G-F', or 'F-G'
forward_data = data[data['POSITION'].isin(['F', 'F-C', 'F-G'])].copy()



# Define weights for each statistical category
weights = {
    '3P': 3,
    '2P': 2,
    'FT': 1,
    'REB': 1.2,
    'AST': 1.5,
    'BLK': 3,
    'STL': 3,
    'TO': -1
}

# Calculate the weighted score for centers
center_data['SCORE'] = (
    center_data['3P'] * weights['3P'] +
    center_data['FG'] * weights['2P'] +
    center_data['FT'] * weights['FT'] +
    center_data['DR'] * weights['REB'] +
    center_data['OR'] * weights['REB'] +
    center_data['A'] * weights['AST'] +
    center_data['BL'] * weights['BLK'] +
    center_data['ST'] * weights['STL'] +
    center_data['TO'] * weights['TO']
)

forward_data['SCORE'] = (
    forward_data['3P'] * weights['3P'] +
    forward_data['FG'] * weights['2P'] +
    forward_data['FT'] * weights['FT'] +
    forward_data['DR'] * weights['REB'] +
    forward_data['OR'] * weights['REB'] +
    forward_data['A'] * weights['AST'] +
    forward_data['BL'] * weights['BLK'] +
    forward_data['ST'] * weights['STL'] +
    forward_data['TO'] * weights['TO']
)

guard_data['SCORE'] = (
    guard_data['3P'] * weights['3P'] +
    guard_data['FG'] * weights['2P'] +
    guard_data['FT'] * weights['FT'] +
    guard_data['DR'] * weights['REB'] +
    guard_data['OR'] * weights['REB'] +
    guard_data['A'] * weights['AST'] +
    guard_data['BL'] * weights['BLK'] +
    guard_data['ST'] * weights['STL'] +
    guard_data['TO'] * weights['TO']
)

center_opponent_stats = center_data.groupby(['OPPONENT \nTEAM'])['SCORE'].mean()

# Group the data by the opponent team and whether the player is a starter for guards
guard_opponent_stats = guard_data.groupby(['OPPONENT \nTEAM'])['SCORE'].mean()

# Group the data by the opponent team and whether the player is a starter for forwards
forward_opponent_stats = forward_data.groupby(['OPPONENT \nTEAM'])['SCORE'].mean()

# Create a list of dictionaries to store team scores
team_scores = []

for team in data['OPPONENT \nTEAM'].unique():
    center_score = center_opponent_stats.loc[team]
    guard_score = guard_opponent_stats.loc[team]
    forward_score = forward_opponent_stats.loc[team]
    team_scores.append({'Team': team, 'Center Score': center_score, 'Guard Score': guard_score, 'Forward Score': forward_score})

# Create a DataFrame from the list of dictionaries
team_scores_df = pd.DataFrame(team_scores)
print(team_scores_df)
# Export the team_scores DataFrame to an Excel file
team_scores_df.to_excel('TeamScores.xlsx', index=False)
