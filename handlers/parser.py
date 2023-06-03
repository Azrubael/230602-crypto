import time
import requests
from bs4 import BeautifulSoup
from handlers.telegram import send_notify
from handlers.menu import TaskHandler


def converter(line):
    """Converting the string received from the exchange aggregator"""
    result = line.find("div", class_="valuta--light").text\
        .replace("$", "").replace(",", "").replace(" ", "")\
        .replace("\n", "").replace("\xa0", "")
    return float(result)


def get_crypto_rank(coins):
    """Processing request for quotations"""
    result = {}
    html_resp = requests.get("https://coinranking.com").text
    block = BeautifulSoup(html_resp, "lxml") #sudo apt-get install python3-lxml
    rows = block.find_all("tr", class_="table__row--full-width")

    for row in rows:
        ticker = row.find("span", class_="profile__subtitle-name")
        if ticker:
            ticker = ticker.text.strip().upper()

            if ticker in coins:
                price = row.find("td", class_="table__cell--responsive")
                if price:
                    converted_price = converter(price)
                result[ticker.upper()] = converted_price
    return result


def check_coins_balance():
    """Send message to the telegram bot if the price matches the condition"""
    while True:
        coins = TaskHandler.read_task_file()
        coin_dict = get_crypto_rank(coins.keys())
        for name, pos_data in coins.items():
            if name in coin_dict:
                if coin_dict[name] <= float(pos_data[0]) and\
                    pos_data[1] == "LONG":
                    send_notify(f"{name.upper()}USD - you can BUY\ncurrent price: {coin_dict[name]}")
                    TaskHandler.delete_task_in_file(name, update=False)
                elif coin_dict[name] > float(pos_data[0]) and\
                    pos_data[1] == "SHORT":
                    send_notify(f"{name.upper()}USD - you can SELL\ncurrent price: {coin_dict[name]}\ntarget price{pos_data[1]}")
                    TaskHandler.delete_task_in_file(name, update=False)

        time.sleep(20)