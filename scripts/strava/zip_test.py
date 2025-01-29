import gzip
import pickle

with gzip.open(f"segment_6111440896_2015_tdf.pkl.gz", "rb") as fp:  # Pickling
    data = pickle.load(fp)


print([i[0][0][0] for i in data])
