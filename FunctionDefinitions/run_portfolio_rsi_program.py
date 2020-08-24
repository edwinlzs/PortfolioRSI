
def run_portfolio_rsi_program(filename, years):
    # import yahoo finance package - will already include data management libraries pandas & numpy
    import yfinance as yf
    
    # import currency conversion tools
    from forex_python.converter import CurrencyRates
    
    # import data management & plotting tools
    import pandas as pd
    import numpy as np
    import datetime as dt
    
    # import excel interaction tools
    from openpyxl import Workbook
    from openpyxl.utils.dataframe import dataframe_to_rows # convert pandas to excel rows
    
    # import custom-made functions
    from FunctionDefinitions.convert_to_sgd import convert_to_sgd
    from FunctionDefinitions.generate_return_df import generate_return_df
    from FunctionDefinitions.retrieve_shares_held import retrieve_shares_held
    from FunctionDefinitions.workdays import workdays
    
    # extract ticker data from excel file
    data = pd.read_excel(filename + ".xlsx")
    ticker_list = data['Ticker']
    
    # setting dates
    end_date = dt.date.today() # set today as end date
    start_date = dt.date(end_date.year-years, end_date.month, end_date.day)
    
    # initialize output dataframe with dates set
    
    period_dates = workdays(start_date, end_date)
    
    output_df = pd.DataFrame(index=period_dates,columns=['Portfolio Value'])
    output_df = output_df.rename_axis('Date')
    output_df = output_df.fillna(0)
    
    # currency adjustment
    
    c = CurrencyRates()
    forex_rates = c.get_rates('SGD')
    forex_rates['GBp'] = forex_rates['GBP']*100 # adjustment for GB pence
    
    # match exchange with relevant currency
    # to be used if tickerData.info does not provide currency info
    # if tickers with new exchanges not inside this array, add in the relevant exchange:currency
    # exchange is based on the end of the ticker symbol (e.g. 000660.KS exchange is KS), currency is based on forex_rates array
    
    exchange_currency = {
        '':'USD', # currently an assumption, not sure if all symbols without a .exchange is from a US exchange
        'AS':'EUR',
        'AX':'AUD',
        'DE':'EUR',
        'HK':'HKD',
        'KS':'KRW',
        'L':'GBp',
        'PA':'EUR',
        'SI':'SGD',
        'SW':'CHF',
        'T':'JPY'
    }
    
    # calculate market values for each ticker
    
    for ticker in ticker_list:
        
        # create yfinance.Ticker object
        
        tickerData = yf.Ticker(ticker)
        
        # locate corresponding shares held
        
        shares_held = retrieve_shares_held(ticker, data)
        
        # retrieve price data
        
        ticker_df = tickerData.history(period='1d', start=start_date, end=end_date)
        
        # preparing output data:
        
        # calculate market value column
        
        ticker_df['Market Value'] = ticker_df['Close'] * shares_held
        
        # generate dataframe with the required values of Close, Volume & Market Value
        
        return_df = generate_return_df(ticker_df, period_dates)
        
        # adjust currency
        
        try:
            currency = tickerData.info["currency"]
        except: # sometimes ticker does not offer tickerData.info
            split_ticker = ticker.split('.')
            
            try:
                ticker_exchange = split_ticker[1] # get the exchange of the ticker
                currency = exchange_currency[ticker_exchange] # locate exchange in array and find corresponding currency
            except: # assume if no exchange appended to end of ticker, then exchange is in US
                currency = 'USD'
    
        if currency != 'SGD':
            return_df = convert_to_sgd(return_df, currency, forex_rates)
            
        output_df['Portfolio Value'] = output_df['Portfolio Value'] + return_df['Market Value']
    
    for date in output_df.index:
        value = output_df.loc[date,"Portfolio Value"]
    
        if pd.isnull(value): # NaN value
            output_df = output_df.drop(date)
            
    # Gain/Loss calculation

    g = lambda x: x if x > 0 else 0
    l = lambda x: -x if x < 0 else 0
    change_df = output_df["Portfolio Value"] - output_df["Portfolio Value"].shift(1)
    output_df["Gain"] = pd.DataFrame(map(g, change_df), index=output_df.index)
    output_df["Loss"] = pd.DataFrame(map(l, change_df), index=output_df.index)        
    
    # Avg Gain/Loss calculation

    avg_gain_list = []
    total_gain = 0
    for i in range(1,15):
        avg_gain_list.append(np.nan) # first 14 days are all 0 since we only get 14 datapoints for Gain/Loss on Day 15
        total_gain += output_df["Gain"].iloc[i]
    
    avg_loss_list = []
    total_loss = 0
    for i in range(1,15):
        avg_loss_list.append(np.nan)
        total_loss += output_df["Loss"].iloc[i]
    
    initial_avg_gain, initial_avg_loss = total_gain/14, total_loss/14
    
    avg_gain_list.append(initial_avg_gain)
    avg_loss_list.append(initial_avg_loss)
    
    df_size = len(output_df)
    
    for i in range(15, df_size):
        last_avg_gain = avg_gain_list[i-1]
        new_gain = output_df["Gain"].iloc[i]
        new_avg_gain = ((last_avg_gain)*13 + new_gain)/14
        avg_gain_list.append(new_avg_gain)
        
        last_avg_loss = avg_loss_list[i-1]
        new_loss = output_df["Loss"].iloc[i]
        new_avg_loss = ((last_avg_loss)*13 + new_loss)/14
        avg_loss_list.append(new_avg_loss)
        
    output_df["Avg Gain"] = pd.DataFrame(avg_gain_list, index=output_df.index)
    output_df["Avg Loss"] = pd.DataFrame(avg_loss_list, index=output_df.index)
    
    # RSI Calculation
    
    output_df["Relative Strength"] = output_df["Avg Gain"]/output_df["Avg Loss"]
    output_df["RSI"] = 100-(100/(1+output_df["Relative Strength"]))
    
    # create & append to workbook
    
    wb = Workbook()
    ws = wb.active
    dest_filename = "PortfolioRSIOutput.xlsx"
    
    for r in dataframe_to_rows(output_df, index=True, header=True):
        ws.append(r)
        
    wb.save(filename = dest_filename)
    
    return