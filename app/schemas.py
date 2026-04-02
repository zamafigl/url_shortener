from datetime import datetime
from pydantic import BaseModel, field_validator


class ShortenRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def normalize_url(cls, value: str) -> str:
        value = value.strip()

        if len(value) > 2048:
            raise ValueError("URL is too long")

        if not value.startswith(("http://", "https://")):
            value = f"https://{value}"

        if "." not in value:
            raise ValueError("Invalid URL")

        return value


class ShortenResponse(BaseModel):
    original_url: str
    short_code: str
    short_url: str


class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime

    class Config:
        from_attributes = True