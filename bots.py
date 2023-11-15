import os
import json
import threading
import time

this_dir = os.path.dirname(os.path.realpath(__file__))

dat_file_path = os.path.join(this_dir, "inventory.dat")

with open(dat_file_path, 'r') as file:
    data = json.load(file)


def bot_clerk(items: list):
    cart = []
    lock = threading.Lock()

    robot_fetcher_lists = [[] for _ in range(3)]

    for n, item in enumerate(items):
        robot_fetcher_lists[n % 3].append(item)

    threads = []
    for n, fetcher_list in enumerate(robot_fetcher_lists, start=1):
        thread = threading.Thread(target=bot_fetcher, args=(fetcher_list, cart, lock))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return cart


def bot_fetcher(items: list, cart: list, lock: threading.Lock):
    for item in items:
        item_number, item_description, seconds = item, data[item][0], data[item][1]

        time.sleep(seconds)

        with lock:
            cart.append([item_number, item_description])


# print(bot_clerk([]))
# print(bot_clerk(['104']))
# print(bot_clerk(['106', '109', '102']))
# print(bot_clerk(['103', '108', '102', '110', '106']))
# print(bot_clerk(['106', '102', '108', '109', '103', '101', '110', '104', '107', '105']))
