import gzip
import pickle

with gzip.open(f"segment6151368704_2013_tdf.pkl.gz", "rb") as fp:  # Pickling
    data = pickle.load(fp)


print([i[0][4] for i in data])
