import pickle

with open("main_2015_2013.pkl", "rb") as fp:  # Pickling
    dictmain = pickle.load(fp)

print(dictmain[:22])
