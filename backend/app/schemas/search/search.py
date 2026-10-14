#schemas/search
from pydantic import BaseModel


class UserSearchItem(BaseModel):
    id: int
    username: str
    email: str

class CircleSearchItem(BaseModel):
    id: int
    name: str
    description: str | None
    member_count: int | None = None

class PostSearchItem(BaseModel):
    id: int
    title: str
    content: str
    author_name: str

class SearchResponse(BaseModel):
    query: str
    page: int
    page_size: int

    users: list[UserSearchItem]
    circles: list[CircleSearchItem]
    posts: list[PostSearchItem]
