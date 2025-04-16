from datetime import datetime

from pydantic import BaseModel

from Contact import Contact


class Event(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime | None
    local: str
    organizer: str | None
    contact: Contact
