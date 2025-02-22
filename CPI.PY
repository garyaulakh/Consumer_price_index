import os
import pandas as pd

data_folder = "A2 Data"

if not os.path.exists(data_folder):
    exit()

csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

all_data = []
for file in csv_files:
    file_path = os.path.join(data_folder, file)
    province = file.split(".")[0]
    
    df = pd.read_csv(file_path)
    month_columns = [col for col in df.columns if col != "Item"]
    
    reshaped_data = []
    for _, row in df.iterrows():
        item = row["Item"]
        for month in month_columns:
            reshaped_data.append([item, month, province, row[month]])
    
    df_reshaped = pd.DataFrame(reshaped_data, columns=["Item", "Month", "Jurisdiction", "CPI"])
    all_data.append(df_reshaped)

df_final = pd.concat(all_data, ignore_index=True)
df_final["CPI"] = pd.to_numeric(df_final["CPI"], errors="coerce")
df_final.to_csv("merged_cpi_data.csv", index=False)

print("File created: merged_cpi_data.csv")



