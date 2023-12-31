import pandas as pd

nba_data_path = 'NBA-2022-2023.xlsx'
nba_data = pd.read_excel(nba_data_path)

# Define the weights for each statistical category
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

# Filter the data for centers who played at least 30 minutes
center_data = nba_data[nba_data['POSITION'].isin(['C', 'C-F'])].copy()
center_data = center_data[center_data['MIN'] >= 30]

# Get the list of unique center players
center_players = center_data['PLAYER '].unique()

# Create an empty DataFrame to store the combined results for all centers
combined_data_all_centers = pd.DataFrame()

# Iterate over each center player
for player_name in center_players:
    # Filter the data for the current center player
    player_data = center_data[center_data['PLAYER '] == player_name]

    # Calculate the score for each team
    player_data['SCORE'] = (player_data['3P'] * weights['3P'] +
                            player_data['FG'] * weights['FG'] +
                            player_data['FT'] * weights['FT'] +
                            player_data['DR'] * weights['DR'] +
                            player_data['OR'] * weights['OR'] +
                            player_data['A'] * weights['A'] +
                            player_data['BL'] * weights['BL'] +
                            player_data['ST'] * weights['ST'] +
                            player_data['TO'] * weights['TO'])

    # Calculate the average score against each team
    average_scores = player_data.groupby('OPPONENT \nTEAM')['SCORE'].mean().reset_index()

    # Rename the column
    average_scores.rename(columns={'SCORE': 'AVERAGE SCORE'}, inplace=True)

    # Select the relevant columns for the final output
    player_average_score_against_team = pd.merge(player_data[['PLAYER ', 'OPPONENT \nTEAM']], average_scores, on='OPPONENT \nTEAM').drop_duplicates()

    # Load team file
    team_file_path = 'TeamStats/CenterVsLeague.xlsx'
    team_data = pd.read_excel(team_file_path)

    # Load player file
    player_file_path = 'STATIC SHEETS/CentersPerGameTotals.xlsx'
    player_data = pd.read_excel(player_file_path)

    # Filter player data for the current center player
    player_stats = player_data[player_data['PLAYER '] == player_name].iloc[:, 1:11]

    # Create an empty DataFrame to store the predicted stats for each team
    predicted_stats_all_teams = pd.DataFrame(columns=['PLAYER ', 'TEAM'] + list(player_stats.columns) + ['SCORE'])

    # Iterate over each team in the team file
    for opponent_team in team_data['OPPONENT \nTEAM']:
        # Retrieve the multipliers for the opponent team
        opponent_multipliers = team_data[team_data['OPPONENT \nTEAM'] == opponent_team].iloc[:, 1:11]

        # Multiply player's average stats by opponent multipliers
        predicted_stats = player_stats.multiply(opponent_multipliers.values)

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

    combined_data = pd.merge(predicted_stats_all_teams, player_average_score_against_team, on=['PLAYER ', 'OPPONENT \nTEAM'], how='inner')

    # Calculate the percentage by dividing the actual score by the predicted score
    combined_data['PERCENTAGE'] = (combined_data['AVERAGE SCORE'] / combined_data['SCORE']) * 100

    combined_data['ABSOLUTE_DIFFERENCE'] = abs(combined_data['AVERAGE SCORE'] - combined_data['SCORE'])
    combined_data['ABSOLUTE_PERCENTAGE_DIFFERENCE'] = combined_data['ABSOLUTE_DIFFERENCE'] / combined_data['AVERAGE SCORE']

    # Calculate the mean absolute percentage error (MAPE)
    mape = combined_data['ABSOLUTE_PERCENTAGE_DIFFERENCE'].mean()

    num = combined_data['SCORE'] * mape

    combined_data['FLOOR'] = combined_data['SCORE'] - num
    combined_data['CEILING'] = combined_data['SCORE'] + num
    combined_data['MAPE'] = mape * 100

    # Select the relevant columns for the final output
    combined_data = combined_data[['PLAYER ', 'OPPONENT \nTEAM', 'AVERAGE SCORE', 'FLOOR', 'SCORE', 'CEILING', 'PERCENTAGE', 'MAPE']]

    # Append the combined data for the current center player to the overall DataFrame
    combined_data_all_centers = combined_data_all_centers._append(combined_data, ignore_index=True)


# Export the combined data for all center players to an Excel file
output_file_path = 'CenterStats.xlsx'
combined_data_all_centers.to_excel(output_file_path, index=False)
