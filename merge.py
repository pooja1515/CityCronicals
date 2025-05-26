import os
import pandas as pd


DATA_FOLDER = "data"


dataframes = []


for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".csv"):
        file_path = os.path.join(DATA_FOLDER, filename)
        try:
            df = pd.read_csv(file_path)
            dataframes.append(df)
            print(f"Loaded: {filename} ({len(df)} rows)")
        except Exception as e:
            print(f"Error reading {filename}: {e}")


combined_df = pd.concat(dataframes, ignore_index=True)


combined_df.drop_duplicates(inplace=True)
print(f"\nCombined DataFrame shape (after deduplication): {combined_df.shape}")


combined_df.to_csv("combined_cleaned_data.csv", index=False)
print("\nSaved combined data to 'combined_cleaned_data.csv'")
