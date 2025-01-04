from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tg_id: int
    tg_url: str
    first_name: str
    last_name: str | None
    tg_username: str | None
    coins: int
    is_active: bool
    is_admin: bool
    subscription: datetime | None
    created_at: datetime
    updated_at: datetime


class UserOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    first_name: str | None = ""
    last_name: str | None = ""
    is_admin: bool
    is_active: bool
    is_verified: bool
    coin: int
    subscription: datetime | None
    created_at: datetime
    updated_at: datetime


class UserCreateInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: str


class EmailVerifyInputSchema(BaseModel):
    token: str


class EmailVerifyOutputSchema(BaseModel):
    status: bool


class UserUpdateData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserUpdateVerifyData(BaseModel):
    is_verified: bool


class UserUpdateInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data: UserUpdateData


class UserDeleteInputSchema(BaseModel):
    id: UUID
