from datetime import datetime

from pydantic import BaseModel


class Contact(BaseModel):
    phone_number: int | None
    email: str | None


class Event(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime | None
    local: str
    organizer: str | None
    contact: Contact
