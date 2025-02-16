import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("tdf_1.gpx")
# Convert to Pandas Dataframe
df = gpx.to_dataframe(["lat", "lon", "ele"])
df.to_csv("tdf_1.csv")
