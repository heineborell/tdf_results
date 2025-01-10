import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import LineString

# Sample DataFrame
df = pd.read_csv("tdf_1.csv")

# Extract coordinates from DataFrame
coordinates = list(zip(df["lon"], df["lat"]))  # GeoPandas expects (lon, lat)

# Convert coordinates to a LineString
route = LineString(coordinates)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[route])

# Reproject GeoDataFrame to match the background map's CRS (Web Mercator: EPSG:3857)
gdf = gdf.to_crs(epsg=3857)

# Plot the route with a background map
fig, ax = plt.subplots(figsize=(10, 8))
gdf.plot(ax=ax, color="blue", linewidth=2)
ctx.add_basemap(
    ax, source=ctx.providers.CartoDB.Voyager, crs=gdf.crs
)  # Add background map
ax.set_title("Route with Background Map")
plt.show()
