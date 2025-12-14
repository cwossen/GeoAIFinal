# load_seoul.py
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the dong-level shapefile
shapefile_path = "seoul_dong_boundaries.shp"
gdf = gpd.read_file(shapefile_path)

# 2. Load population CSV
csv_path = "workplace_population_2025_dong.csv"
try:
    pop_df = pd.read_csv(csv_path, encoding="cp949")
except UnicodeDecodeError:
    pop_df = pd.read_csv(csv_path, encoding="utf-8")

    print(pop_df["동별(1)"].head(20))


print("Shapefile columns:", gdf.columns)
print("Population CSV columns:", pop_df.columns)

# 3. Standardize join key
pop_df = pop_df.rename(columns={"동별(1)": "ADM_NM"})

# 4. 🔥 Filter only rows where 항목 == 총인구 (total population)
pop_total = pop_df[pop_df["항목"] == "총인구"].copy()

# 5. Select one census value (pick your preferred quarter)
# Change to "2025 2/4" if you want 2nd quarter instead
pop_total = pop_total[["ADM_NM", "2025 3/4"]].rename(columns={"2025 3/4": "총인구"})

# 6. Merge with shapefile
merged_gdf = gdf.merge(pop_total, on="ADM_NM", how="left")
print(merged_gdf.head())

# 7. Save merged output (GeoPackage recommended, not shapefile)
merged_path = "seoul_dong_boundaries_with_pop.gpkg"
merged_gdf.to_file(merged_path, driver="GPKG")
print(f"✅ Merged file saved to: {merged_path}")

# 8. Visualize population distribution
if "총인구" in merged_gdf.columns:
    merged_gdf.plot(column="총인구", cmap="viridis", legend=True, figsize=(10, 8))
    plt.title("Seoul — Total Population by Dong (2025 3/4)")
    plt.axis("off")
    plt.show()
else:
    print("⚠️ Population column missing — check merged fields.")
