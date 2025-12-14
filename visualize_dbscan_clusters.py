import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# ✅ Load your feature shapefile (already includes area, neighbors_count, etc.)
gdf = gpd.read_file("seoul_dong_boundaries_with_pop.gpkg")

# ✅ Select numeric columns for clustering
X = gdf.select_dtypes(include=["number"])

# ✅ Scale and cluster
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

db = DBSCAN(eps=0.45121, min_samples=4)
labels = db.fit_predict(X_scaled)
gdf["cluster"] = labels  # Add cluster labels directly to GeoDataFrame

# ✅ Plot clusters
fig, ax = plt.subplots(figsize=(12, 10))
gdf.plot(column="cluster", cmap="tab20", legend=True, linewidth=0.5, edgecolor="gray", ax=ax)
plt.title("🌎 DBSCAN Clusters — Seoul Dong Boundaries", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.show()

# ✅ Optionally save the clustered shapefile
gdf.to_file("seoul_dong_clusters.shp")
print("✅ Clustering complete and saved to seoul_dong_clusters.shp")
