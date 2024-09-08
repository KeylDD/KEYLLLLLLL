import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium

# Step 1: Load the dataset
file_path = "case-assignment-data.xlsx"  # Update this with your actual file path
data = pd.read_excel(file_path)

# Step 2: Data overview
print("First few rows of the dataset:")
print(data.head())

print("\nDataset information:")
print(data.info())

print("\nMissing values:")
print(data.isnull().sum())

# Step 3: Handle missing values
# Fill numerical columns with 0
numeric_columns = data.select_dtypes(include=['number']).columns
data[numeric_columns] = data[numeric_columns].fillna(0)

# Fill non-numerical columns with mode
non_numeric_columns = data.select_dtypes(exclude=['number']).columns
for column in non_numeric_columns:
    data[column] = data[column].fillna(data[column].mode()[0])  # Avoid inplace=True to avoid FutureWarning

# Step 4: Visualizations
# 4.1 Distribution of Installed Capacity in MW
plt.figure(figsize=(10,6))
sns.histplot(data['installed_capacity_MW'], kde=True)
plt.title('Distribution of Installed Capacity (MW)')
plt.show()

# 4.2 Correlation heatmap
# Ensure all columns are numeric before calculating correlation
numeric_data = data.select_dtypes(include=['number'])
plt.figure(figsize=(10,8))
sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# 4.3 Scatter plot: Dam Height vs Average Annual Generation
plt.figure(figsize=(10,6))
sns.scatterplot(x='dam_height_m', y='avg_annual_generation_GWh', data=data)
plt.title('Dam Height vs Average Annual Generation')
plt.show()

# 4.4 Bar plot for the number of power plants by country
plt.figure(figsize=(10,6))
sns.countplot(x='country_code', data=data)
plt.title('Number of Power Plants by Country')
plt.xticks(rotation=90)
plt.show()

# Step 5: Geographical visualization using Folium
# Create a map centered around Europe
m = folium.Map(location=[50.0, 10.0], zoom_start=4)

# Add markers for each power plant
for i, row in data.iterrows():
    folium.Marker([row['lat'], row['lon']],
                  popup=row['name']).add_to(m)

# Save the map as an HTML file
m.save('power_plants_map.html')

print("Geographical map saved as 'power_plants_map.html'. You can open this file to view the interactive map.")
