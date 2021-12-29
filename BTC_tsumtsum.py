import binance.client
from binance.client import Client
from datetime import datetime
from binance.enums import *
from binance.exceptions import *
import time
import requests
import json


#API_Keys
api_key = ""
api_secret = ""
line_token = ""
client = binance.client.Client(api_key,api_secret)

price_list = []
total_list = []

#LINEの通知
def LineNotify(text):
    url = "https://notify-api.line.me/api/notify"
    data = {"message": text}
    headers = {"Authorization": "Bearer " + line_token}
    requests.post(url, data=data, headers=headers)

while 1:
    BTC_info = client.get_ticker(symbol="BTCUSDT")
    BTC_price = float(BTC_info["lastPrice"])
    qty = round((11/BTC_price),5)
    price_list.append(BTC_price)
    BTC_prices = sum(price_list)
    total_day = len(price_list)
    avg_price = BTC_prices / total_day
    total_dollar = BTC_price * qty
    total_list.append(total_dollar)
    total_buy = round((sum(total_list)),2)
    order = client.order_market_buy(symbol="BTCUSDT",quantity=qty)
    print("本日の積立完了！本日の取得価格[$]" + str(BTC_price) + "/累計購入額[$]" + str(total_buy) + "/積立日数" + str(total_day) + "日/平均取得価格[$]" + str(avg_price))
    LineNotify("本日の積立完了！　　本日の取得価格[$]" + str(BTC_price) + "　　累計購入額[$]" + str(total_buy) + "　　　　　　積立日数" + str(total_day) + "日　　　　　　　　　平均取得価格[$]" + str(avg_price))
    time.sleep(86400)
