from datetime import date
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, field_validator, Field
from pydantic.generics import GenericModel


T = TypeVar("T")


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    summary: str = Field(..., min_length=1, max_length=511)
    publication_date: str | date = Field(
        ...,
        description="The publication date of the book "
        "in ISO format (YYYY-MM-DD)"
    )

    @field_validator("publication_date", mode="before")
    @classmethod
    def convert_date_to_string(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        return value

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class PaginatedResponse(GenericModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int


class PaginatedAuthors(PaginatedResponse[Author]):
    pass


class PaginatedBooks(PaginatedResponse[Book]):
    pass
