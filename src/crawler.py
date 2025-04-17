from typing import Literal
import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from Event import Event
from Contact import Contact

BASE_URL = "https://www.alesc.sc.gov.br/"


def get_event_data(field: Literal["titulo-longo", "local-do-evento", "data-agenda-2", "resp-reserva"], event: Tag) -> str:
    # Find event field with data
    t = event.find("div", class_=f"views-field-field-{field}")

    # Get and format data based on field
    match(field):
        case "titulo-longo":
            return t.find("strong").text.strip()
        case "local-do-evento":
            return t.text.strip()
        case "data-agenda-2":
            time_range = t.find("span", class_="date-display-range")
            if time_range:
                return {
                    "start": time_range.find("span", class_="date-display-start").get('content'),
                    "end": time_range.find("span", class_="date-display-end").get('content')
                }

            time = t.find("span", class_="date-display-single")
            return {
                "start": time.get("content"),
                "end": None
            }
        case "resp-reserva":
            def remove_escape_sequences(s: str): return re.sub(
                "\\xa0|\\t|\\r|", "", s
            ).strip() or None

            def format_phone_number(s: str):
                s = re.sub("\D", "", s).strip()

                match(len(s)):
                    case 11:
                        return f"({s[:2]}) {s[2:-4]}-{s[7:]}"
                    case 10:
                        return f"({s[:2]}) {s[2:-4]}-{s[6:]}"
                    case 9:
                        return f"{s[2:-4]}-{s[6:]}"
                    case 8:
                        return f"{s[:4]}-{s[4:]}"
                    case _:
                        return s

            organizer, phone_number, email = list(
                map(remove_escape_sequences, t.text.split("\n"))) if t is not None else [None]*3

            if phone_number is not None:
                phone_number = format_phone_number(phone_number)

            return {
                "organizer": organizer,
                "phone_number": phone_number,
                "email": email
            }


def read_panel_events(panel: Tag) -> list[Event]:
    # Get all events of a panel
    events = panel.find(
        "ul", class_="list-unstyled"
    ).find_all("li")

    fields = ["titulo-longo",
              "local-do-evento",
              "data-agenda-2",
              "resp-reserva"
              ]

    # Read data of each event
    events = [{
        field: get_event_data(field, event)
        for field in fields
    } for event in events]

    return [Event(title=event["titulo-longo"],
                  start_date=event["data-agenda-2"]["start"],
                  end_date=event["data-agenda-2"]["end"],
                  local=event["local-do-evento"],
                  organizer=event["resp-reserva"]["organizer"],
                  contact=Contact(phone_number=event["resp-reserva"]["phone_number"],
                                  email=event["resp-reserva"]["email"]))
            for event in events]


def scrape_page(page: BeautifulSoup):
    # Get event content in page
    content = (page
               .find("div", class_="row")
               .find("div", class_="view-content"))

    # Read every event from every panel in the page
    return [read_panel_events(panel)
            for panel in content.find_all("div", class_="panel panel-default")]


def get_url(start_date: str, page: int = None):
    page_param = f"page={page}"
    return f"{BASE_URL}?data_in[value][date]={start_date}&data_fim[value][date]=&titulo=&local=All{page_param if page is not None else ''}"


def download_url(url: str) -> BeautifulSoup:
    # Request and parse HTML page
    res = requests.get(url)
    if (res.status_code == 200):
        return BeautifulSoup(res.text, "html.parser")


def crawler(start_date: str):
    print("Requesting first page...")
    first_page = download_url(
        BASE_URL + f"agenda?data_in[value][date]={start_date}&data_fim[value][date]=&titulo=&local=All")

    pagination = first_page.find("ul", class_="pagination")
    pages = [first_page]
    if pagination:
        print("Pagination found. Requesting next pages...")

        def get_page_number_from_href(
            t: str): return int(t.split("&")[-1].split("=")[-1]) + 1

        last_page_href = (first_page
                          .find("li", class_="pager-last")
                          .a.get("href"))
        last_page_number = get_page_number_from_href(last_page_href)

        # Request pages while the "next" button exists (otherwise, it's the last page)
        while (li := pages[-1].find("li", class_="next")) is not None:
            resource = li.a.get("href")
            url = BASE_URL + resource
            page_number = get_page_number_from_href(resource)
            print(
                f"Requesting page {page_number} of {last_page_number}\033[K", end="\r")
            page = download_url(url)
            pages.append(page)

    print("\nScraping pages...")
    return [scrape_page(page) for page in pages]
