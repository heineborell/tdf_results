import pickle

from rich import print as rprint

with open("6112161792_1922_1909.pkl", "rb") as fp:  # Pickling
    dictmain = pickle.load(fp)

print(dictmain)
rprint("[bold green] testing[/bold green]")
rprint("[red ]this is red[/red ]")
