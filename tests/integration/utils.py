import csv
from pathlib import Path

from src.portfolios.csv_portfolio import FIELDNAMES, TICKER, QUANTITY


def save_csv_portfolio(portfolio: dict, path: Path):
        
         with open(path, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            for k, v in portfolio.items():
                csv_writer.writerow({TICKER:k,QUANTITY:v})
