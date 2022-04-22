import sys
from datetime import date

import firebase_admin
import matplotlib.pyplot as plt
import yfinance as yf
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def buy(stock, shares):
    stocks = db.collection('portfolio').document('stocks').get().to_dict()
    no_shares = stocks[stock] + shares if stock in stocks else shares
    db.collection('portfolio').document('stocks').update({stock: no_shares})

def sell(stock, shares, ):
    stocks = db.collection('portfolio').document('stocks').get().to_dict()
    no_shares = stocks[stock] - shares
    if no_shares < 0:
        return Exception("You haven't so many shares on your portfolio")
    db.collection('portfolio').document('stocks').update({stock: no_shares})

def portfolio_value():
    stocks = db.collection('portfolio').document('stocks').get().to_dict()
    portfolio_value = 0
    for stock in stocks:
        portfolio_value += yf.Ticker(stock).history(period=date.today().strftime("%Y-%m-%d")).Close.values[0] * stocks[stock]
    return round(portfolio_value, 2)
    
def get(arg):
    stocks = db.collection('portfolio').document('stocks').get().to_dict()
    if arg == 'all':
        print(stocks)
    elif arg == 'value':
        print(portfolio_value())
    else: 
        print({arg: stocks[arg]})

def get_each_value():
    stocks = db.collection('portfolio').document('stocks').get().to_dict()
    stocks_val = {}
    for stock, shares in stocks.items():
        if shares != 0:
            stocks_val[stock] = shares * yf.Ticker(stock).history(period=date.today().strftime("%Y-%m-%d")).Close.values[0]
    return stocks_val

argv = sys.argv
for i in range(len(argv)):
    if argv[i] == '--buy':
        buy(argv[i+1], float(argv[i+2]))
        i += 2
    if argv[i] == '--sell':
        sell(argv[i+1], float(argv[i+2]))
        i += 2
    if argv[i] == '--get':
        get(argv[i+1])
        i += 1
    if argv[i] == '--plot':
        stock_with_values = get_each_value()
        plt.pie(stock_with_values.values(), labels=stock_with_values.keys())
        plt.axis('equal')
        plt.show()
