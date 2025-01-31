import gzip
import pickle

with gzip.open(
    f"/Users/deniz/iCloud/Research/Data_Science/Projects/data/strava/tdf_pickles/segment_6145585152_2017_tdf.pkl.gz",
    "rb",
) as fp:  # Pickling
    data = pickle.load(fp)


print([i[0][1][0] for i in data])
# print(data)
