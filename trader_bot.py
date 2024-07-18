from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv
import os

#get the APIKEYS
load_dotenv()

API_KEY=os.getenv("Key")
API_SECRET=os.getenv("Secret")
BASE_URL=os.getenv("Endpoint")

AlpacaConfig = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}
# Instantiate the Alpaca class
broker=Alpaca(AlpacaConfig)

#set up our own strategy. Lumibot have Momentum if you wanna borrow theirs
class Trader(Strategy):
    def initialize(self, symbol="SPY"):
        self.symbol=symbol
        #the we determine how often we wanna make a trader by sleeptime
        self.sleeptime="24H"
        #then set where to start with the trader in every 24 hours
        self.last_trade = None

    def on_trading_iteration(self):
        if self.last_trade == None:
            new_order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
            )
            self.submit_order(new_order)
            self.last_trade="buy"

#lets set up the trading instance with our strategy variable
strategy=Trader(
    name="mlstrat",
    broker=broker,
    parameters={
        "symbol": "SPY"
    }
)
#set up the backtesting here for our strategy
#step 1: get the start_date
backtesting_start_date=datetime(2023, 12, 15)
#step 2: get the end_date
backtesting_end_date=datetime(2023, 12, 31)
"""
step 3: set up the backtesting with the data source
the data source here is YahooBackTesting class but if
you have your own data, you would typically use panda backtesting

The backtesting_params may include the budget and other stuff too
check here ```https://pypi.org/project/lumibot/1.3.2/```
"""
strategy.backtest(
    YahooDataBacktesting,
    backtesting_start_date,
    backtesting_end_date,
    parameters={
        "symbol": "SPY"
    }
)
