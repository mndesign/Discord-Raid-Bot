import datetime
import os

class Startup():
    def __init__(self) -> None:
        print(" _____           _                     ___ _       _         __       _     _     ___       _   ")
        print("/__   \_ __ __ _(_)_ __   ___ _ __    / __\ |_   _| |__     /__\ __ _(_) __| |   / __\ ___ | |_ ")
        print("  / /\/ '__/ _` | | '_ \ / _ \ '__|  / /  | | | | | '_ \   / \/// _` | |/ _` |  /__\/// _ \| __|")
        print(" / /  | | | (_| | | | | |  __/ |    / /___| | |_| | |_) | / _  \ (_| | | (_| | / \/  \ (_) | |_ ")
        print(" \/   |_|  \__,_|_|_| |_|\___|_|    \____/|_|\__,_|_.__/  \/ \_/\__,_|_|\__,_| \_____/\___/ \__|")
        print(f"Version {os.environ["VER"]}.{os.environ["BUILD"]}")
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print("The Bot is Online")
        print("------------------------------------------------------------------------------------------------")
