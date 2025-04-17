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

    def to_dict(self):
        if (self.start_date is not None
                and isinstance(self.start_date, datetime)):
            self.start_date = self.start_date.isoformat(timespec="seconds")

        if (self.end_date is not None
                and isinstance(self.end_date, datetime)):
            self.end_date = self.end_date.isoformat(timespec="seconds")

        return self.model_dump(warnings=False)
