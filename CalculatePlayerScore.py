import pandas as pd

# Load NBA 2022-2023 data
nba_data_path = 'NBA-2022-2023.xlsx'
nba_data = pd.read_excel(nba_data_path)

# Specify the player's name
player_name = 'Joel Embiid'

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

# Filter the data for the specified player
player_data = nba_data[nba_data['PLAYER '] == player_name]

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
result = pd.merge(player_data[['PLAYER ', 'OPPONENT \nTEAM']], average_scores, on='OPPONENT \nTEAM').drop_duplicates()

# Output the results to an Excel file
output_file_path = 'PlayerAverageScores.xlsx'
result.to_excel(output_file_path, index=False)

print(f"Player average scores against each team saved to {output_file_path}.")
