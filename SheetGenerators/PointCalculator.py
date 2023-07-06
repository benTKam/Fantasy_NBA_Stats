import pandas as pd

# Load team file
team_file_path = 'CenterVsLeague.xlsx'
team_data = pd.read_excel(team_file_path)

# Remove the line break character from the column header


# Load player file
player_file_path = 'CentersPerGameTotals.xlsx'
player_data = pd.read_excel(player_file_path)

# Specify the player's name
player_name = 'Joel Embiid'

# Retrieve the player's average stats
player_stats = player_data[player_data['PLAYER '] == player_name].iloc[:, 1:11]

# Create an empty DataFrame to store the predicted stats for each team
predicted_stats_all_teams = pd.DataFrame(columns=['PLAYER ', 'TEAM'] + list(player_stats.columns) + ['SCORE'])

# Iterate over each team in the team file
for opponent_team in team_data['OPPONENT \nTEAM']:
    # Retrieve the multipliers for the opponent team
    opponent_multipliers = team_data[team_data['OPPONENT \nTEAM'] == opponent_team].iloc[:, 1:11]

    # Multiply player's average stats by opponent multipliers
    predicted_stats = player_stats.multiply(opponent_multipliers.values)

    # Calculate the player's score based on the predicted stats
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
    predicted_stats['SCORE'] = (predicted_stats['3P'] * weights['3P'] +
                                predicted_stats['FG'] * weights['FG'] +
                                predicted_stats['FT'] * weights['FT'] +
                                predicted_stats['DR'] * weights['DR'] +
                                predicted_stats['OR'] * weights['OR'] +
                                predicted_stats['A'] * weights['A'] +
                                predicted_stats['BL'] * weights['BL'] +
                                predicted_stats['ST'] * weights['ST'] +
                                predicted_stats['TO'] * weights['TO'])

    # Add the player's name and opponent team name to the predicted stats DataFrame
    predicted_stats['PLAYER '] = player_name
    predicted_stats['OPPONENT \nTEAM'] = opponent_team

    # Append the predicted stats for the current team to the overall DataFrame
    predicted_stats_all_teams = predicted_stats_all_teams._append(predicted_stats, ignore_index=True)

# Reorder the columns
predicted_stats_all_teams = predicted_stats_all_teams[['PLAYER ', 'OPPONENT \nTEAM'] + list(player_stats.columns) + ['SCORE']]

# Output the predicted stats to an Excel file
output_file_path = 'Joel_Embiid_Predicted_Stats.xlsx'
predicted_stats_all_teams.to_excel(output_file_path, index=False)

print(f"Predicted stats for {player_name} against each team saved to {output_file_path}.")
