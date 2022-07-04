from rich.console import Console
from rich.table import Table

table = Table(title="Star Wars Movies")

table.add_column("Released", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console()
console.print(table, justify="center")

print("\n\n\n\n")


report = Table(show_header=True, header_style="bold")

report.add_column("Address")
report.add_column("City")
report.add_column("Postal Code")

report.add_row("#500-75 O'Connor Street","Ottawa","K4B 1S2")
report.add_row("00, rue Saint-Lazare","Dunkerque","59140")
report.add_row("02, place de Fontenoy","Verrieres Le Buisson","91370")

console.print(report)	