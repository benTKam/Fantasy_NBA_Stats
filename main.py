import pandas as pd

# Read the Excel sheet into a pandas DataFrame
data = pd.read_excel('NBA-2022-2023.xlsx')

# Filter the data to include rows where the position is 'C', 'C-F', or 'F-C'
center_data = data[data['POSITION'].isin(['C', 'C-F'])].copy()

# # Filter the data to include rows where the position is 'G'
# guard_data = data[data['POSITION'] == 'G'].copy()
#
# # Filter the data to include rows where the position is 'F', 'G-F', or 'F-G'
# forward_data = data[data['POSITION'].isin(['F', 'G-F', 'F-G'])].copy()



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

# # Calculate the weighted score for guards
# guard_data['SCORE'] = (
#     guard_data['3P'] * weights['3P'] +
#     guard_data['FG'] * weights['2P'] +
#     guard_data['FT'] * weights['FT'] +
#     guard_data['DR'] * weights['REB'] +
#     guard_data['OR'] * weights['REB'] +
#     guard_data['A'] * weights['AST'] +
#     guard_data['BL'] * weights['BLK'] +
#     guard_data['ST'] * weights['STL'] +
#     guard_data['TO'] * weights['TO']
# )
#
# # Calculate the weighted score for forwards
# forward_data['SCORE'] = (
#     forward_data['3P'] * weights['3P'] +
#     forward_data['FG'] * weights['2P'] +
#     forward_data['FT'] * weights['FT'] +
#     forward_data['DR'] * weights['REB'] +
#     forward_data['OR'] * weights['REB'] +
#     forward_data['A'] * weights['AST'] +
#     forward_data['BL'] * weights['BLK'] +
#     forward_data['ST'] * weights['STL'] +
#     forward_data['TO'] * weights['TO']
# )
# Group the data by the opponent team and whether the player is a starter
center_opponent_stats = center_data.groupby(['OPPONENT \nTEAM', 'STARTER\n(Y/N)'])['SCORE'].mean()

# Calculate the average weighted score per game for centers against starters
center_starters_avg_score = center_opponent_stats.loc[pd.IndexSlice[:, 'Y']].mean()

# Calculate the average weighted score per game for centers against bench players
center_bench_avg_score = center_opponent_stats.loc[pd.IndexSlice[:, 'N']].mean()

# Calculate the position multiplier for centers against starters
center_starters_multiplier = center_starters_avg_score / center_data['SCORE'].mean()

# Calculate the position multiplier for centers against bench players
center_bench_multiplier = center_bench_avg_score / center_data['SCORE'].mean()

# Sort the teams based on their average weighted scores for centers against starters in descending order
sorted_center_starters = center_opponent_stats.loc[pd.IndexSlice[:, 'Y']].sort_values(ascending=False)
team_scores = pd.DataFrame(columns=['Team', 'Starting Score', 'Bench Score'])

# Iterate over the center_opponent_stats DataFrame and populate the team_scores DataFrame
for team, avg_score_start, avg_score_bench in zip(
    center_opponent_stats.index.get_level_values('OPPONENT \nTEAM').unique(),
    center_opponent_stats.loc[pd.IndexSlice[:, 'Y']],
    center_opponent_stats.loc[pd.IndexSlice[:, 'N']]
):
    row = {'Team': team, 'Starting Score': avg_score_start, 'Bench Score': avg_score_bench}
    team_scores = pd.concat([team_scores, pd.DataFrame([row])], ignore_index=True)

# Export the team_scores DataFrame to an Excel file
team_scores.to_excel('TeamScores.xlsx', index=False)
# league_avg_weighted_score_center = center_data['SCORE'].mean()
# # Group the data by the opponent team and calculate the average weighted score per game for centers
# center_opponent_stats = center_data.groupby('OPPONENT \nTEAM')['SCORE'].mean()
#
# center_position_multiplier = center_opponent_stats / league_avg_weighted_score_center

# # Group the data by the opponent team and calculate the average weighted score per game for guards
# guard_opponent_stats = guard_data.groupby('OPPONENT \nTEAM')['SCORE'].mean()
#
# # Group the data by the opponent team and calculate the average weighted score per game for forwards
# forward_opponent_stats = forward_data.groupby('OPPONENT \nTEAM')['SCORE'].mean()

# Rank the teams based on their average weighted scores for centers
# center_team_ranking = center_opponent_stats.rank(ascending=False)

# # Rank the teams based on their average weighted scores for guards
# guard_team_ranking = guard_opponent_stats.rank(ascending=False)
#
# # Rank the teams based on their average weighted scores for forwards
# forward_team_ranking = forward_opponent_stats.rank(ascending=False)

# # Sort the teams based on their average weighted scores for centers in descending order
# sorted_center_teams = center_opponent_stats.sort_values(ascending=False)
#
# # Sort the teams based on their average weighted scores for guards in descending order
# sorted_guard_teams = guard_opponent_stats.sort_values(ascending=False)

# Sort the teams based on their average weighted scores for forwards in descending order
# sorted_forward_teams = forward_opponent_stats.sort_values(ascending=False)


# print(f"League Average Against centers: {league_avg_weighted_score_center:.2f}")
# # Display the team ranking for centers
# print("Rank\tTeam\t\t\tAverage Weighted Score (Centers)")
# for team, avg_score in sorted_center_teams.items():
#     multiplier = center_position_multiplier[team]
#     print(f"{center_team_ranking[team]}\t{team}\t\t{avg_score:.2f}\t\t{multiplier:.2f}")
#
# print()  # Add a line break between the two rankings

# # Display the team ranking for guards
# print("Rank\tTeam\t\t\tAverage Weighted Score (Guards)")
# for team, avg_score in sorted_guard_teams.items():
#     print(f"{guard_team_ranking[team]}\t{team}\t\t{avg_score:.2f}")
#
# print()  # Add a line break between the two rankings
#
# # Display the team ranking for forwards
# print("Rank\tTeam\t\t\tAverage Weighted Score (Forwards)")
# for team, avg_score in sorted_forward_teams.items():
#     print(f"{forward_team_ranking[team]}\t{team}\t\t{avg_score:.2f}")
