import json
import asyncio
from functools import partial
from pywebio.output import *
import pywebio.input as inp
from pywebio.session import run_js


class TaskHandler:

    def __init__(self):
        self.__coins = ["BTC", "ETH", "DOT", "LTC", "XRP"]


    @staticmethod
    def read_task_file():
        with open("tasks.json", encoding="utf-8") as file:
            return json.load(file)


    @staticmethod
    def add_task_to_file(data: dict):
        last_changes = TaskHandler.read_task_file()
        last_changes[data["name"]] = data["price to alert"]
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(last_changes, file, indent=4)


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


    @staticmethod
    def get_task_list():
        result = []     # для хранения заданий
        tasks = TaskHandler.read_task_file()
        for name, price in tasks.items():
            result.append([
                name,
                price,
                put_button(f"delete {name}", onclick=partial(TaskHandler.delete_task_in_file, name))
            ])

        # a button to add all the table wih data on the screen
        put_table(
            result,
            header=["name", "price to alert", "delete?"]
        )
        # a button "Back" calls JavaScript
        put_button("Back", onclick=lambda: run_js("location.reload()"))


    @staticmethod
    def add_task_validate(data):
        if data is None or data == "":
            return "price", "You need to fill a field"


    async def add_task_in_list(self):
        coin_ticker = await inp.select("Select a coin", self.__coins, multiple=False)
        price = await inp.input("Enter awaiting price", validate=TaskHandler.add_task_validate)

        if all([coin_ticker, price]):
            toast("A task created successfully")
            await asyncio.sleep(2)
            run_js("location.reload()")
            TaskHandler.add_task_to_file({
                "name": coin_ticker.lower(),
                "price to alert": price.replace(',', '.').lower()
            })