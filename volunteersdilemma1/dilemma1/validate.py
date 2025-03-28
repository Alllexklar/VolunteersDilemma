import os
import pandas as pd

def load_latest_csv():
    temp_folders = [d for d in os.listdir('.') if d.startswith('__temp_bots') and os.path.isdir(d)]
    temp_folders.sort(key=os.path.getctime, reverse=True)
    if not temp_folders:
        return None
    newest_folder = temp_folders[0]
    csv_path = os.path.join(newest_folder, 'dilemma1.csv')
    return pd.read_csv(csv_path)

def validate_bot_data():
    df = load_latest_csv()
    if df is None:
        print("No temp folder found.")
        return
    print("Latest CSV file loaded.")