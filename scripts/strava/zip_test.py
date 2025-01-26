import gzip
import pickle

with gzip.open(f"segment_2012_tdf.pkl.gz", "rb") as fp:  # Pickling
    data = pickle.load(fp)


print([i[0][6] for i in data])
