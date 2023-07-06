import pandas as pd

# Load team file
team_file_path = 'CenterVsLeague.xlsx'
team_data = pd.read_excel(team_file_path)

# Remove the line break character from the column header


# Load player file
player_file_path = 'CentersPerGameTotals.xlsx'
player_data = pd.read_excel(player_file_path)

# Specify the player's name
player_name = 'Al Horford'

# Retrieve the player's average stats
player_stats = player_data[player_data['PLAYER '] == player_name].iloc[:, 1:11]

# Create an empty DataFrame to store the predicted stats for each team
predicted_stats_all_teams = pd.DataFrame(columns=player_stats.columns)

# Iterate over each team in the team file
for opponent_team in team_data['OPPONENT \nTEAM']:
    # Retrieve the multipliers for the opponent team
    opponent_multipliers = team_data[team_data['OPPONENT \nTEAM'] == opponent_team].iloc[:, 1:11]

    # Multiply player's average stats by opponent multipliers
    predicted_stats = player_stats.multiply(opponent_multipliers.values)

    # Append the predicted stats for the current team to the overall DataFrame
    predicted_stats_all_teams = predicted_stats_all_teams._append(predicted_stats, ignore_index=True)

# Output the predicted stats to an Excel file
output_file_path = 'PredictedStats_AlHorford.xlsx'
predicted_stats_all_teams.to_excel(output_file_path, index=False)

print(f"Predicted stats for {player_name} against each team saved to {output_file_path}.")
