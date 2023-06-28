import pandas as pd

# Read the Excel sheet into a pandas DataFrame
data = pd.read_excel('NBA_Stats.xlsx')

# Filter the data to include rows where the position is 'C', 'C-F', or 'F-C'
center_data = data[data['POSITION'].isin(['C', 'C-F', 'F-C'])].copy()

# Filter the data to include rows where the position is 'G'
guard_data = data[data['POSITION'] == 'G'].copy()

# Filter the data to include rows where the position is 'F', 'G-F', or 'F-G'
forward_data = data[data['POSITION'].isin(['F', 'G-F', 'F-G'])].copy()



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

# Calculate the weighted score for guards
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

# Calculate the weighted score for forwards
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

# Group the data by the opponent team and calculate the average weighted score per game for centers
center_opponent_stats = center_data.groupby('OPPONENT \nTEAM')['SCORE'].mean()

# Group the data by the opponent team and calculate the average weighted score per game for guards
guard_opponent_stats = guard_data.groupby('OPPONENT \nTEAM')['SCORE'].mean()

# Group the data by the opponent team and calculate the average weighted score per game for forwards
forward_opponent_stats = forward_data.groupby('OPPONENT \nTEAM')['SCORE'].mean()

# Rank the teams based on their average weighted scores for centers
center_team_ranking = center_opponent_stats.rank(ascending=False)

# Rank the teams based on their average weighted scores for guards
guard_team_ranking = guard_opponent_stats.rank(ascending=False)

# Rank the teams based on their average weighted scores for forwards
forward_team_ranking = forward_opponent_stats.rank(ascending=False)

# Sort the teams based on their average weighted scores for centers in descending order
sorted_center_teams = center_opponent_stats.sort_values(ascending=False)

# Sort the teams based on their average weighted scores for guards in descending order
sorted_guard_teams = guard_opponent_stats.sort_values(ascending=False)

# Sort the teams based on their average weighted scores for forwards in descending order
sorted_forward_teams = forward_opponent_stats.sort_values(ascending=False)

# Display the team ranking for centers
print("Rank\tTeam\t\t\tAverage Weighted Score (Centers)")
for team, avg_score in sorted_center_teams.items():
    print(f"{center_team_ranking[team]}\t{team}\t\t{avg_score:.2f}")

print()  # Add a line break between the two rankings

# Display the team ranking for guards
print("Rank\tTeam\t\t\tAverage Weighted Score (Guards)")
for team, avg_score in sorted_guard_teams.items():
    print(f"{guard_team_ranking[team]}\t{team}\t\t{avg_score:.2f}")

print()  # Add a line break between the two rankings

# Display the team ranking for forwards
print("Rank\tTeam\t\t\tAverage Weighted Score (Forwards)")
for team, avg_score in sorted_forward_teams.items():
    print(f"{forward_team_ranking[team]}\t{team}\t\t{avg_score:.2f}")
