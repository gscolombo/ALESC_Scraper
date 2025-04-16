from datetime import datetime
from crawler import crawler


def get_data_input() -> str:
    date = input()
    try:
        return datetime.fromisoformat(date).strftime("%d/%m/%Y")
    except ValueError:
        print("Invalid date format.")


if __name__ == "__main__":
    start_date = get_data_input()
    if start_date is not None:
        print(f"Start date: {start_date}")

        panels = crawler(start_date)

        print(panels)
