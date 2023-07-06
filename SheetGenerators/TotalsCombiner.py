import pandas as pd

centers_file_path = '../STATIC SHEETS/CentersPerGameTotals.xlsx'
centers_data = pd.read_excel(centers_file_path)

guards_file_path = '../STATIC SHEETS/GuardsPerGameTotals.xlsx'
guards_data = pd.read_excel(guards_file_path)

forwards_file_path = '../STATIC SHEETS/ForwardsPerGameTotals.xlsx'
forwards_data = pd.read_excel(forwards_file_path)

frames = [centers_data, guards_data, forwards_data]

result = pd.concat(frames)

result.to_excel("AllPlayerTotals.xlsx")
