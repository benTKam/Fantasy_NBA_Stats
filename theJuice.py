import pandas as pd
import numpy as np

# Read the data from a CSV file
df = pd.read_csv("C:/Users/bkamide/Downloads/FanDuel-NBA-2023 ET-10 ET-24 ET-94790-players-list.csv")  # Specify the path to your CSV file

df = df[(df['FPPG'] > 0) & (df['FPPG'] >= 10)]

# Sort the data by FPPG in descending order
df = df.sort_values(by='FPPG', ascending=False)

# Constraints
positions = {"PG": 2, "SG": 2, "SF": 2, "PF": 2, "C": 1}
max_salary = 60000

# Initialize a memoization table to store the best lineup at each state
memo = {}

# Helper function to calculate the best lineup recursively
def get_best_lineup(players, remaining_positions, remaining_salary, used_players, start_index=0):
    if not remaining_positions or remaining_salary <= 0:
        return [], 0

    state = (tuple(remaining_positions), remaining_salary, tuple(used_players), start_index)

    if state in memo:
        return memo[state]

    best_lineup, best_score = [], 0

    for i, player in enumerate(players):
        if player["Id"] not in used_players:
            pos = player["Position"].split('/')
            for p in pos:
                if remaining_positions.get(p, 0) > 0 and player["Salary"] <= remaining_salary:
                    new_positions = dict(remaining_positions)
                    new_positions[p] -= 1
                    new_salary = remaining_salary - player["Salary"]
                    new_used_players = set(used_players)
                    new_used_players.add(player["Id"])

                    lineup, score = get_best_lineup(players, new_positions, new_salary, new_used_players, start_index=i + 1)

                    if score + player["FPPG"] > best_score:
                        best_score = score + player["FPPG"]
                        best_lineup = [player] + lineup

    memo[state] = (best_lineup, best_score)
    return best_lineup, best_score

# Initial call to the dynamic programming function
initial_positions = positions.copy()
initial_used_players = set()
best_lineup, best_score = get_best_lineup(df.to_dict(orient="records"), initial_positions, max_salary, initial_used_players)

# Reorganize the lineup to have 2 PG, 2 SG, 2 SF, 2 PF, and 1 C in that order
lineup_in_order = []
positions_order = ["PG", "PG", "SG", "SG", "SF", "SF", "PF", "PF", "C"]

for position in positions_order:
    for player in best_lineup:
        if position in player["Position"]:
            lineup_in_order.append(player)
            best_lineup.remove(player)
            break

# Print the lineup in order with player names
for player in lineup_in_order:
    print(f"{player['Position']} {player['FPPG']} {player['Salary']} - {player['First Name']} {player['Last Name']}")
print(f"Total Score: {best_score}")
print(f"Total Salary: {sum(player['Salary'] for player in lineup_in_order)}")