import pickle

with open("main_2004_2003.pkl", "rb") as fp:  # Pickling
    dictmain = pickle.load(fp)

print(dictmain)
