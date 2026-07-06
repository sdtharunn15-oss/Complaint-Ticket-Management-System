from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
import re


# -----------------------
# User Schemas
# -----------------------

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# -----------------------
# Customer Schemas
# -----------------------

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        return value


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# -----------------------
# Ticket Schemas
# -----------------------

class TicketBase(BaseModel):
    customer_id: int
    title: str
    description: str
    priority: str
    category: str


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    category: str | None = None
    status: str | None = None


class TicketResponse(TicketBase):
    id: int
    status: str
    assigned_agent: int | None = None

    model_config = ConfigDict(from_attributes=True)


    