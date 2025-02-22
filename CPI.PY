import os
import pandas as pd

# Set the folder where the data files are stored
data_folder = "A2 Data"

# Get all CSV files from the folder
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

all_data = []
for file in csv_files:
    file_path = os.path.join(data_folder, file)  # Get full file path
    province = file.split(".")[0]  # Extract province name from filename
    
    df = pd.read_csv(file_path)  # Read CSV file
    month_columns = [col for col in df.columns if col != "Item"]  # Identify month columns
    
    reshaped_data = []
    for _, row in df.iterrows():
        item = row["Item"]
        for month in month_columns:
            reshaped_data.append([item, month, province, row[month]])  # Convert data to long format
    
    df_reshaped = pd.DataFrame(reshaped_data, columns=["Item", "Month", "Jurisdiction", "CPI"])
    all_data.append(df_reshaped)

# Combine all data into a single DataFrame
df_final = pd.concat(all_data, ignore_index=True)

# Convert CPI values to numeric format
df_final["CPI"] = pd.to_numeric(df_final["CPI"], errors="coerce")

# Save the final data as a CSV file
df_final.to_csv("merged_cpi_data.csv", index=False)




