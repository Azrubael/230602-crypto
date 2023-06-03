import json
import asyncio
from functools import partial
from pywebio.output import *
import pywebio.input as inp
from pywebio.session import run_js


class TaskHandler:

    def __init__(self):
        self.__coins = ["BTC", "ETH", "DOT", "LTC", "XRP"]
        self.__position = ["LONG", "SHORT"]


    @staticmethod
    def read_task_file():
        with open("tasks.json", encoding="utf-8") as file:
            return json.load(file)


    @staticmethod
    def add_task_to_file(data: dict):
        last_changes = TaskHandler.read_task_file()
        last_changes[data["name"]] = [data["alert price"], data["position"]]
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(last_changes, file, indent=4)
        print(last_changes)


    @staticmethod
    def delete_task_in_file(coin_name, update=True):
        last_changes = TaskHandler.read_task_file()
        try:
            del last_changes[coin_name]
            with open("tasks.json", "w", encoding="utf-8") as file:
                json.dump(last_changes, file, indent=4)

        except KeyError:
            print("Key is absent in the task list")
        if update:
            run_js("location.reload()")
        print(last_changes)


    @staticmethod
    def get_task_list():
        result = []             # for tasks
        tasks = TaskHandler.read_task_file()
        for name, pos_data in tasks.items():
            result.append([
                name,
                pos_data[0],
                pos_data[1],
                put_button(f"delete {name}", onclick=partial(TaskHandler.delete_task_in_file, name))
            ])
        put_table(              # all the table with data on the screen
            result,
            header=["name", "alert price", "position", "delete?"]
        )
        # a button "Back" calls JavaScript
        put_button("Back", onclick=lambda: run_js("location.reload()"))


    @staticmethod
    def add_price_validate(data):
        if data is None or data == "":
            return "price", "You need to fill a field"


    @staticmethod
    def add_position_validate(position, ticker):
        last_changes = TaskHandler.read_task_file()
        if ticker in last_changes.keys() and\
            last_changes[ticker][1] == position:
            return True
        return False


    async def add_task_in_list(self):
        ticker = await inp.select("Select a coin", self.__coins, multiple=False)
        price = await inp.input("Enter awaiting price", validate=TaskHandler.add_price_validate)
        position = await inp.select("Select position", self.__position, multiple=False)
        position_exists = TaskHandler.add_position_validate(position.upper(), ticker.upper())
        if all([ticker, price, position]) and position_exists:
            await asyncio.sleep(1)
            run_js("location.reload()")
            TaskHandler.add_task_to_file({
                "name": ticker.upper(),
                "alert price": price.replace(',', '.'),
                "position": position.upper()
            })
            toast("A task created successfully")
        elif all([ticker, price, position]) and not position_exists:
            toast(f"A task cannot create because a position {ticker.upper()}USD {position.upper()} already exists")
            await asyncio.sleep(1)
            TaskHandler.get_task_list()