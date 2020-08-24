# function to convert dataframe values into SGD

def convert_to_sgd(df, currency, forex_rates):
    
    sgd_to_currency = forex_rates[currency]
    df['Close'] = df['Close']/sgd_to_currency
    df['Market Value'] = df['Market Value']/sgd_to_currency
    
    return df