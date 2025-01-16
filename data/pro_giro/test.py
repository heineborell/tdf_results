import pickle

with open("main_2014_2014.pkl", "rb") as fp:  # Pickling
    dictmain = pickle.load(fp)

print(dictmain)
