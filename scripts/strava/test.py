import getpass

import grand_tours
from grand_tours import jsonisers

if __name__ == "__main__":
    username = getpass.getuser()
    print(jsonisers.stat_jsoniser(username, "tdf", 2018))
