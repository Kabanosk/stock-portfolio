You can use this code for tracking your stock portfolio. To do that you must:
  1. Make your gcp project to connect to firebase database.
  2. Install libraries: firebase-admin, yfinance, matplotlib
  3. Use script options for buying selling and getting data from portfolio:
      - **--buy** <stock_name> <no_shares> for adding shares of the stock to database
      - **--sell** <stock_name> <no_shares> for removing shares of the stock to database
      - **--get** <stock_name/"all"/"value"> for getting how many shares of the stock(stock_name) / how many shares of each stock(all) do you have or value of your portfolio (value)
      - **--plot** for geting pie plot of your portfolio
