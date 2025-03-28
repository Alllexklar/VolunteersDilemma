import os
import pandas as pd

def load_latest_csv():
    temp_folders = [d for d in os.listdir('.') if d.startswith('__temp_bots') and os.path.isdir(d)]
    temp_folders.sort(key=os.path.getctime, reverse=True)
    if not temp_folders:
        return None
    newest_folder = temp_folders[0]
    csv_path = os.path.join(newest_folder, 'dilemma1.csv')
    print(f"Loading CSV from: {newest_folder}")
    return pd.read_csv(csv_path)

def validate_bot_data():
    df = load_latest_csv()
    if df is None:
        print("No temp folder found.")
        return
    print("Latest CSV file loaded.")

    columns_of_interest = [
        "participant.id_in_session",
        "participant._is_bot",
        "player.pet_choice",
        "player.group_assignment",
        "player.my_group_id"
    ]

    # Filter the DataFrame
    try:
        df = df[columns_of_interest]
    except KeyError as e:
        print(f"Column not found: {e}")
        return
    
    # Simple validation example: Check for missing data
    if df.isnull().any().any():
        print("Some rows have missing values in the key columns.")
    else:
        print("All key columns have valid data.")

    # Remove any duplicate row that has participant._is_bot = 0
    duplicates = df[df.duplicated(subset=["participant.id_in_session"], keep=False)]
    nonbot_duplicates = duplicates[duplicates["participant._is_bot"] == 0]
    df = df[~df.index.isin(nonbot_duplicates.index)]

    groups = df.groupby('player.group_assignment')

    # Instead of groups.filter(...), just count groups by name.
    num_dog_minority = sum(1 for group_name, _ in groups if group_name.startswith('dog_minority'))
    num_cat_minority = sum(1 for group_name, _ in groups if group_name.startswith('cat_minority'))
    num_control = sum(1 for group_name, _ in groups if group_name.startswith('control'))

    print("")
    print(f"Total number of players: {df.shape[0]}")
    print(f"Total number of groups: {len(groups)}")
    print(f"Number dog minority groups: {num_dog_minority}")
    print(f"Number cat minority groups: {num_cat_minority}")
    print(f"Number control groups: {num_control}")
    print("")

    success = True

    for group_name, group_df in groups:
        # check group sizes
        if group_df.shape[0] != 3 and not group_name.startswith('control'):
            print(f"Group {group_name} does not have 3 players.")
            success = False
        
        # check if my_group_id is unique within this group
        if group_df['player.my_group_id'].nunique() != 1:
            print(f"Group {group_name} has inconsistent my_group_id values.")
            success = False

        # check dog_minority groups
        if group_name.startswith('dog_minority'):
            counts = group_df['player.pet_choice'].value_counts()
            if not (counts.get('dog', 0) == 1 and counts.get('cat', 0) == 2):
                print(f"{group_name}: Not 1 dog / 2 cats.")
                success = False                
        # check cat_minority groups
        elif group_name.startswith('cat_minority'):
            counts = group_df['player.pet_choice'].value_counts()
            if not (counts.get('cat', 0) == 1 and counts.get('dog', 0) == 2):
                print(f"{group_name}: Not 1 cat / 2 dogs.")
                success = False

        
    print("")
    if success:
        print("All checks passed.")
    else:
        print("Some checks failed. Please review the output above.")


if __name__ == "__main__":
    validate_bot_data()