import geopandas as gpd

# ✅ Load your Seoul shapefile
gdf = gpd.read_file("seoul_dong_boundaries_with_pop.gpkg")

# ✅ Ensure it has the right coordinate reference system (CRS)
if gdf.crs is None:
    gdf = gdf.set_crs("EPSG:5179")  # Korean Transverse Mercator
else:
    gdf = gdf.to_crs("EPSG:5179")

# ✅ 1. Area and perimeter
gdf["area_m2"] = gdf.geometry.area
gdf["perimeter_m"] = gdf.geometry.length

# ✅ 2. Centroid coordinates
gdf["centroid_x"] = gdf.geometry.centroid.x
gdf["centroid_y"] = gdf.geometry.centroid.y

# ✅ 3. Compute adjacency (number of neighbors)
from libpysal.weights import Queen
w = Queen.from_dataframe(gdf)
gdf["neighbors_count"] = gdf.index.map(lambda i: len(w.neighbors.get(i, [])))

# ✅ 4. Save results
output_path = "C:/PythonProjects/seoul_dong_features.gpkg"
gdf.to_file(output_path)

print("✅ Features built and saved to:", output_path)
print(gdf[["ADM_NM", "area_m2", "neighbors_count"]].head())
