from pydantic import BaseModel


class Contact(BaseModel):
    phone_number: str | None
    email: str | None
