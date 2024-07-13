from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv
import os

#get the APIKEYS
load_dotenv()

API_KEY=os.getenv("key")
API_SECRET=os.getenv("Secret")
BASE_URL=os.getenv("Endpoint")

class AlpacaConfig:
    {
    "api_key": API_KEY,
    "api_secret": API_SECRET,
    "PAPER": True
}