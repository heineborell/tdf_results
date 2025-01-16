import pickle

from rich import print as rprint

with open("6165049344_2012_2011.pkl", "rb") as fp:  # Pickling
    dictmain = pickle.load(fp)

print(dictmain)
rprint("[bold green] testing[/bold green]")
rprint("[red ]this is red[/red ]")
