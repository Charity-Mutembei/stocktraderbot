from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from alpaca_trade_api import REST
from utils import estimate_sentiment


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

broker=Alpaca(AlpacaConfig)

class MLTrader(Strategy):
    def initialize(self, symbol="SPY", cash_at_risk=.5):
        self.symbol=symbol
        #the we determine how often we wanna make a trader by sleeptime
        self.sleeptime="24H"
        #then set where to start with the trader in every 24 hours
        self.last_trade = None
        self.cash_at_risk=cash_at_risk
        self.api=REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
    

    #position sizing and limiting
    def position_size(self):
        #making sure that we have good use of money when trading
        cash_left_in_account = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash_left_in_account*self.cash_at_risk/last_price, 0)
        return cash_left_in_account, last_price, quantity
    

    #get dates function
    def get_dates(self):
        today=self.get_datetime()
        three_days_ago = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_ago.strftime('%Y-%m-%d')
    

    #getting the news
    def get_news_sentiment(self):
       today, three_days_ago = self.get_dates()
       news=self.api.get_news(symbol="SPY", start=three_days_ago, end=today)
       news = [ev.__dict__["_raw"]["headline"] for ev in news]

       probability, sentiment = estimate_sentiment(news)

       return probability, sentiment

    def on_trading_iteration(self):
        #get the returns in position_size function
        cash_left_in_account, last_price, quantity = self.position_size()

        if cash_left_in_account > last_price:
            probability =self.get_news_sentiment()
            sentiment = self.get_news_sentiment()
            # print(probability, sentiment)
            if probability [0] > .999 and sentiment == "positive":
                if self.last_trade == "sell":
                    self.sell_all()

                new_order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.20,
                    stop_loss_price=last_price*0.95,
                )
                self.submit_order(new_order)
                self.last_trade="buy"
            if probability [0] > .999 and sentiment == "negative":
                if self.last_trade == "buy":
                    self.sell_all()

                new_order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell ",
                    type="bracket",
                    take_profit_price=last_price*.8,
                    stop_loss_price=last_price*1.05,
                )
                self.submit_order(new_order)
                self.last_trade="sell"


#lets set up the trading instance with our strategy variable
strategy=MLTrader(
    name="mlstrat",
    broker=broker,
    parameters={
        "symbol": "SPY",
        "cash_at_risk": .5
    }
)

# set up the backtesting here for our strategy
#step 1: get the start_date
backtesting_start_date=datetime(2023, 1, 1)
backtesting_end_date=datetime.today()
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
        "symbol": "SPY",
        "cash_at_risk": .5
    }
)
