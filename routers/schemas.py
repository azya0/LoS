import datetime
import json
import uuid
from string import ascii_letters, digits
from typing import List, Optional

from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, validator, BaseModel


class BaseModelsPostWithFile(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str


class UserCreate(CreateUpdateDictModel):
    first_name: str
    second_name: str

    email: EmailStr
    username: str
    password: str

    @validator('username')
    def username_validator(cls, v):
        if len(v) < 3:
            raise ValueError(f'username length less then 3')

        banned_chars = set(filter(lambda char: char not in ascii_letters + digits + '_', v))
        if any(banned_chars):
            raise ValueError(f'username can\'t include chars like: {", ".join(banned_chars)}')
        return v

    @validator('password')
    def password_validator(cls, v):
        if len(v) < 5:
            raise ValueError(f'password length less then 5')
        return v


class UserUpdate(schemas.BaseUserUpdate):
    username: str


class UserShortRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class TestSchemeRead(BaseModel):
    file_format: str
    file_path: str

    class Config:
        orm_mode = True


class VkNewsRead(BaseModel):
    title: Optional[str]
    content: Optional[str]
    image_url: Optional[str]

    link: str

    class Config:
        orm_mode = True


class VkNewsReadList(BaseModel):
    count: int
    items: Optional[List[VkNewsRead]]

    class Config:
        orm_mode = True


class CommentShortRead(BaseModel):
    author: UserShortRead

    context: str

    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class NewsRatingRead(BaseModel):
    user_id: int
    news_id: int
    positive: bool

    class Config:
        orm_mode = True


class NewsRead(BaseModel):
    id: int

    title: str
    context: str

    rating_value: Optional[int]

    author: UserShortRead
    comments: List[CommentShortRead]

    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class NewsPatchScheme(BaseModel):
    title: Optional[str]
    context: Optional[str]


class NewsPostScheme(BaseModel):
    title: str
    context: str


class CodeCharacterRead(BaseModel):
    first_name: str
    second_name: str

    description: str

    class Config:
        orm_mode = True


class CodeFileRead(BaseModel):
    id: int

    file_format: str

    class Config:
        orm_mode = True


class CodeCharacterPatch(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]

    description: Optional[str]


class CodeFractionGet(BaseModelsPostWithFile):
    name: str

    description: str


class CodeFractionRead(BaseModel):
    id: int
    name: str

    description: str

    code_file: Optional[CodeFileRead]

    class Config:
        orm_mode = True


class CodeFractionPatch(BaseModelsPostWithFile):
    name: Optional[str]

    description: Optional[str]


class CodeLocationGet(CodeFractionGet): ...
class CodeLocationRead(CodeFractionRead): ...
class CodeLocationPatch(CodeFractionPatch): ...
class CodeItemGet(CodeFractionGet): ...
class CodeItemRead(CodeFractionRead): ...
class CodeItemPatch(CodeFractionPatch): ...
class CodeDifferentGet(CodeFractionGet): ...
class CodeDifferentRead(CodeFractionRead): ...
class CodeDifferentPatch(CodeFractionPatch): ...
