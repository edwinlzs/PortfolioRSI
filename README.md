Current version is fixed at calculating 14-day RSI

required libraries
1) pip install yfinance --upgrade --no-cache-dir
3) pip install forex-python
4) pip install workdays
5) pip install openpyxl

Prepare ticker input Excel file to be read (example "InputPortfolio.xlsx" has been prepared)
Make sure the data in the Ticker columns are formatted according to how Yahoo Finance formats them

The correct ticker to use is based on the symbols state on the yahoo finance website for the stock
for example, here is the website for Singtel https://sg.finance.yahoo.com/quote/Z74.SI/

The correct ticker corresponding to Singtel is "Z74.SI" as stated in the URL

Run the program and enter name of input file as well as years of data

Program generates "PortfolioRSIOutput.xlsx" which contains the resulting RSI calculations
