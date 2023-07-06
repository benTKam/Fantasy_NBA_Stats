import pandas as pd

# Load actual scores file
actual_scores_file = 'PlayerStats/PlayerAverageScores.xlsx'
actual_scores_data = pd.read_excel(actual_scores_file)

# Load predicted stats file
predicted_stats_file = 'Joel_Embiid_Predicted_Stats.xlsx'
predicted_stats_data = pd.read_excel(predicted_stats_file)

# Specify the player's name
player_name = 'Joel Embiid'

# Filter actual scores for the player
actual_scores_player = actual_scores_data[actual_scores_data['PLAYER '] == player_name]

# Filter predicted stats for the player
predicted_stats_player = predicted_stats_data[predicted_stats_data['PLAYER '] == player_name]

# Merge actual scores and predicted stats for the player
comparison_data = pd.merge(actual_scores_player, predicted_stats_player, on='OPPONENT \nTEAM', suffixes=('_ACTUAL', '_PREDICTED'))

# Select relevant columns for comparison
comparison_data = comparison_data[['OPPONENT \nTEAM', 'AVERAGE SCORE', 'SCORE']]


# Output the comparison to a file
output_file_path = 'ScoreComparison.xlsx'
comparison_data.to_excel(output_file_path, index=False)

print(f"Score comparison for {player_name} saved to {output_file_path}.")
