# import requests
# import json
# import time

# def get_live_stock_data(symbol):
#     # NSE API URL for real-time stock data
#     api_url = "https://www.nseindia.com/api/quote-data?symbol=" + symbol

#     # Send GET request to fetch stock data
#     response = requests.get(api_url)

#     # Check if request was successful
#     if response.status_code == 200:
#         # Parse JSON response into a Python dictionary
#         data = json.loads(response.text)

#         # Extract relevant stock data
#         current_price = data['data'][0]['lastPrice']
#         day_high = data['data'][0]['dayHigh']
#         day_low = data['data'][0]['dayLow']
#         volume = data['data'][0]['totalTradedVolume']
#         change_percent = data['data'][0]['changePercent']

#         # Print stock data
#         print("Symbol:", symbol)
#         print("Current Price:", current_price)
#         print("Day High:", day_high)
#         print("Day Low:", day_low)
#         print("Volume:", volume)
#         print("Change Percent:", change_percent)
#         print("--------------------")
#     else:
#         # Error handling for unsuccessful requests
#         print("Error fetching stock data for symbol:", symbol)
#         print("Status code:", response.status_code)
#         print("Response:", response.text)

# if __name__ == "__main__":
#     # Specify the stock symbol to track
#     symbol = "NIFTY50"

#     # Fetch and print live stock data for the specified symbol
#     while True:
#         get_live_stock_data(symbol)
#         time.sleep(10)



import requests

class NseIndia:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)

    def get_stock_info(self, symbol):
        url1 = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol.replace(' ', '%20').replace('&', '%26') + "&section=trade_info"
        url2 = 'https://www.nseindia.com/api/quote-equity?symbol=' + symbol.replace(' ', '%20').replace('&', '%26')
        response1 = self.session.get(url1, headers=self.headers).json()
        response2 = self.session.get(url2, headers=self.headers).json()
        
        try:
            tc = response1['marketDeptOrderBook']['tradeInfo']['totalMarketCap']
            fc = response1['marketDeptOrderBook']['tradeInfo']['ffmc']
            lp = response2['priceInfo']['lastPrice']
            ma = response2["industryInfo"]["macro"]
            se = response2["industryInfo"]["sector"]
            ind = response2["industryInfo"]["industry"]
            bas = response2["industryInfo"]["basicIndustry"]
            return tc, fc, lp, ma, se, ind, bas
        except KeyError:
            return None, None, None, None, None, None, None