from datetime import datetime

from pydantic import BaseModel


class Contact(BaseModel):
    phone_number: int
    email: str


class Event(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime
    local: str
    organizer: str
    contact: dict[str, Contact]
