import pickle

import numpy as np
import pandas as pd

with open(
    "../../data/pro_tdf/6107312128_2024_2013.pkl",
    "rb",
) as fp:  # Pickling
    data = pickle.load(fp)

final_dict = {}
df = pd.DataFrame()
for i in range(len(data)):
    if len(data[i][0]) == len(data[i][1]) == len(data[i][2][0]) == len(data[i][2][1]):
        final_dict.update(
            {
                "year": data[i][0],
                "stage": data[i][1],
                "name": data[i][2][0],
                "time": data[i][2][1],
            }
        )
        info_lst = data[i][2][2]
        final_info_lst = []
        for j in info_lst:
            if len(j.split("\n")) == 1:
                single_el = j.split("\n")
                single_el.append("Na")
                final_info_lst.append(single_el)
            else:
                final_info_lst.append(j.split("\n"))

        final_info_lst = np.array(final_info_lst).flatten()

        # construct info table dictionary
        info_dict = dict(zip(final_info_lst[0::2], final_info_lst[1::2]))
        info_dict = {key: [value] * len(data[i][0]) for key, value in info_dict.items()}
        info_df = pd.DataFrame(columns=list(info_dict.keys()))
        df_joined = pd.concat(
            [pd.DataFrame.from_dict(final_dict), pd.DataFrame.from_dict(info_dict)],
            axis=1,
        )

        df = pd.concat([df, df_joined])
    else:
        print(data[i][0][0], data[i][1][0], "---------the index lengths are not same.")

df.to_csv("test.csv")
