import sys
from typing import Literal
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = "https://www.alesc.sc.gov.br/"


def get_event_data(field: Literal["titulo-longo", "local-do-evento", "data-agenda-2", "resp-reserva"], event: Tag) -> str:
    t = event.find("div", class_=f"views-field-field-{field}")

    match(field):
        case "titulo-longo":
            return t.find("strong").text
        case "local-do-evento":
            return t.text
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
            if t:
                organizer, phone_number, email = t.text.split("\n")
                return {
                    "organizer": organizer,
                    "phone_number": phone_number,
                    "email": email
                }


def read_panel_events(panel: Tag) -> dict:
    events = panel.find(
        "ul", class_="list-unstyled"
    ).find_all("li")

    fields = ["titulo-longo",
              "local-do-evento",
              "data-agenda-2",
              "resp-reserva"
              ]

    return [{
        field: get_event_data(field, event)
        for field in fields
    } for event in events]


def scrape_page(page: BeautifulSoup):
    content = (page
               .find("div", class_="row")
               .find("div", class_="view-content"))

    return [read_panel_events(panel)
            for panel in content.find_all("div", class_="panel panel-default")]


def get_url(start_date: str, page: int = None):
    page_param = f"page={page}"
    return f"{BASE_URL}?data_in[value][date]={start_date}&data_fim[value][date]=&titulo=&local=All{page_param if page is not None else ''}"


def download_url(url: str) -> BeautifulSoup:
    res = requests.get(url)
    if (res.status_code == 200):
        return BeautifulSoup(res.text, "html.parser")


def crawler(start_date: str):
    print("Downloading first page...")
    first_page = download_url(
        BASE_URL + f"agenda?data_in[value][date]={start_date}&data_fim[value][date]=&titulo=&local=All")

    pagination = first_page.find("ul", class_="pagination")
    pages = [first_page]
    if pagination:
        print("Pagination found. Downloading next pages...")

        while (li := pages[-1].find("li", class_="next")) is not None:
            resource = li.a.get("href")
            url = BASE_URL + resource
            print(f"Downloading {url}\033[K", end="\r")
            page = download_url(url)
            pages.append(page)

        print(f"\n{len(pages)} pages found.")

    print("Scraping pages...")
    return [scrape_page(page) for page in pages]
