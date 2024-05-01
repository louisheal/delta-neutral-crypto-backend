import csv
from pathlib import Path


FIELDNAMES = ['Ticker', 'Quantity']


def load_portfolio(portfolio_path: Path) -> dict:
    
    with open(portfolio_path, 'r', newline='') as file:
        csv_reader = csv.DictReader(file, fieldnames=FIELDNAMES)
        portfolio = {}
        for row in csv_reader:
            portfolio[row['Ticker']] = float(row['Quantity'])

    return portfolio

def save_portfolio(portfolio: dict, portfolio_path: Path) -> None:
    
    with open(portfolio_path, 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        for k, v in portfolio.items():
            csv_writer.writerow({'Ticker':k, 'Quantity':v})
