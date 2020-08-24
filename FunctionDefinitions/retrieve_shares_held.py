# function to retrieve corresponding SharesHeld

def retrieve_shares_held(input_ticker, data):
    
    count = 0
    for ticker in data['Ticker']:
        if ticker == input_ticker:
            return(data['SharesHeld'][count])
        else:
            count += 1