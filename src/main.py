from datetime import datetime


def get_data_input() -> str:
    date = input()
    try:
        return datetime.fromisoformat(date).strftime("%d/%M/%Y")
    except ValueError:
        print("Invalid date format.")


if __name__ == "__main__":
    start_date = get_data_input()
    print(f"Looking for events starting from {start_date}...")
