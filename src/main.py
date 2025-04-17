import os
from datetime import datetime
from pathlib import Path
from json import dump

from crawler import crawler

# It's expected that this script will be called from the root path
ROOT_PATH = os.getcwd()


def get_data_input() -> str:
    date = input("Insert a date in ISO format: ")
    try:
        return datetime.fromisoformat(date).strftime("%d/%m/%Y")
    except ValueError:
        print("Invalid date format.")


if __name__ == "__main__":
    start_date = get_data_input()
    if start_date is not None:
        print(f"Start date: {start_date}")

        print("Data retrieved.")
        pages = crawler(start_date)

        print("Flattening data...")
        data = [
            event.to_dict()
            for page in pages
            for panel in page
            for event in panel
        ]

        data_dir = Path(ROOT_PATH, 'data')
        data_dir.mkdir(exist_ok=True)

        save_path = data_dir.joinpath(
            f"events_starting_from_{start_date.replace('/', '-')}.json")

        print(f"Storing data at {save_path}...")
        with open(save_path, "w") as fp:
            dump(data, fp, indent=4, ensure_ascii=False)
            print(f"Data stored.")
