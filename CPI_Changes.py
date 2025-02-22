import pandas as pd

# Load the merged CPI data
df = pd.read_csv("merged_cpi_data.csv")

# Convert CPI column to numeric.
df["CPI"] = pd.to_numeric(df["CPI"], errors="coerce")

# Sort data by jurisdiction, item, and month
df.sort_values(by=["Jurisdiction", "Item", "Month"], inplace=True)

# Calculate Month-to-Month CPI Change
df["Prev_CPI"] = df.groupby(["Jurisdiction", "Item"])["CPI"].shift(1)
df["Month-to-Month Change"] = ((df["CPI"] - df["Prev_CPI"]) / df["Prev_CPI"]) * 100

# Filter for selected categories
df_filtered = df[df["Item"].isin(["Food", "Shelter", "All-items excluding food and energy"])]

# Calculate average Month-to-Month CPI change per province
avg_monthly_change = df_filtered.groupby("Jurisdiction")["Month-to-Month Change"].mean().reset_index()
avg_monthly_change["Month-to-Month Change"] = avg_monthly_change["Month-to-Month Change"].round(1)

# Find the province with the highest average CPI change
highest_cpi_province = avg_monthly_change.loc[avg_monthly_change["Month-to-Month Change"].idxmax()]

# Compute Annual Change in CPI for Services
df_services = df[df["Item"] == "Services"]
df_services_jan = df_services[df_services["Month"] == "24-Jan"].set_index("Jurisdiction")["CPI"]
df_services_dec = df_services[df_services["Month"] == "24-Dec"].set_index("Jurisdiction")["CPI"]

# Calculate percentage change in CPI for services from January to December
annual_change = ((df_services_dec - df_services_jan) / df_services_jan) * 100
annual_change = annual_change.reset_index()
annual_change.columns = ["Jurisdiction", "Annual Change in CPI for Services"]
annual_change["Annual Change in CPI for Services"] = annual_change["Annual Change in CPI for Services"].round(1)

# Find the region with the highest services inflation
highest_services_region = annual_change.loc[annual_change["Annual Change in CPI for Services"].idxmax()]

# Save results to CSV files
avg_monthly_change.to_csv("avg_monthly_change.csv", index=False)
annual_change.to_csv("annual_services_cpi.csv", index=False)

# Print key results
print("CPI changes")
print("Province with highest average CPI change:")
print(highest_cpi_province)

print("Region with highest services inflation:")
print(highest_services_region)

