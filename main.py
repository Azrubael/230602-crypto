import os
import threading
import pywebio  # https://pywebio.readthedocs.io/en/latest/
import pywebio.input as inp
from pywebio.output import *

from handlers.menu import TaskHandler


@pywebio.config(theme="dark")
async def main():
    clear()

    task = TaskHandler()
    logo_path = os.path.join("data", "logo.jpg")
    put_image(open(logo_path, "rb").read())

    method = await inp.select(
        "Select the desired option",
        [
            "Add a task",
            "The task list"
        ]
    )

    if "Add a task" == method:
        await task.add_task_in_list()
    elif "The task list" == method:
        task.get_task_list()
        

if __name__ == "__main__":
      pywebio.start_server(main, host="127.0.0.1", port=4444)