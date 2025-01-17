import pickle

from rich import print as rprint

with open("pickels/6208991232_2002_2002.pkl", "rb") as fp:  # Pickling
    dictmain = pickle.load(fp)

print(dictmain)
rprint("[bold green] testing[/bold green]")
rprint("[red ]this is red[/red ]")
