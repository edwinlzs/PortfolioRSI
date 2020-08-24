# function to generate standardized dataframe containing desired data points

import pandas as pd
import datetime as dt

def generate_return_df(ticker_df,period_dates):
    
    # return_df will have the standardized dates for rows and 3 columns for Close, Volume & Market Value
    
    return_df = pd.DataFrame(index=period_dates,columns=['Close', 'Volume', 'Market Value'])
    return_df = return_df.rename_axis('Date')
    
    count = 0
    for date in return_df.index:

        try:
            ticker_timestamp = dt.datetime.date(ticker_df.index[count]) # converts Timestamp to datetime.date type
        except:
            continue

        return_timestamp = date
        
        # if date of return_df matches date of ticker_df - data point corresponds correctly

        if return_timestamp == ticker_timestamp:
            return_df.loc[date, 'Close'] = ticker_df.iloc[count]['Close']
            return_df.loc[date, 'Volume'] = ticker_df.iloc[count]['Volume']
            return_df.loc[date, 'Market Value'] = ticker_df.iloc[count]['Market Value']  
            count += 1

        # if date of return_df does not match date of ticker_df - indicates non-trading holiday
            
        elif return_timestamp < ticker_timestamp:
            return_df.loc[date, 'Close'] = ticker_df.iloc[count-1]['Close']
            return_df.loc[date, 'Volume'] = ticker_df.iloc[count-1]['Volume']
            return_df.loc[date, 'Market Value'] = ticker_df.iloc[count-1]['Market Value']
            
        elif return_timestamp > ticker_timestamp:
            count += 1
            return_df.loc[date, 'Close'] = ticker_df.iloc[count]['Close']
            return_df.loc[date, 'Volume'] = ticker_df.iloc[count]['Volume']
            return_df.loc[date, 'Market Value'] = ticker_df.iloc[count]['Market Value']
            count += 1
            
            
    return return_df