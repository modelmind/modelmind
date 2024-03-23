from typing import List, TypedDict

from pydantic import HttpUrl


class Author(TypedDict, total=False):
    name: str
    url: HttpUrl
    icon_url: HttpUrl


class Thumbnail(TypedDict):
    url: HttpUrl


class Image(TypedDict):
    url: HttpUrl


class Footer(TypedDict):
    text: str
    icon_url: HttpUrl


class Field(TypedDict, total=False):
    name: str
    value: str
    inline: bool


class Embed(TypedDict, total=False):
    author: Author
    title: str
    url: HttpUrl
    description: str
    color: int
    fields: List[Field]
    thumbnail: Thumbnail
    image: Image
    footer: Footer


class WebhookBody(TypedDict, total=False):
    username: str
    avatar_url: HttpUrl
    content: str
    embeds: List[Embed]
