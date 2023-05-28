from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    name: str = Field('Bob', min_length=3, max_length=16)
    sure_name: str = Field('Dilan', min_length=3, max_length=16)
    email: EmailStr
    phone_number: str = Field('+3801112233', min_length=9, max_length=16)
    birthday: str = Field('184-03-09')
    additional_data: str


class ContactResponse(BaseModel):
    id: int = 1
    name: str = Field('Bob', min_length=3, max_length=16)
    sure_name: str = Field('Dilan', min_length=3, max_length=16)
    email: EmailStr
    phone_number: str = Field('+38067111233', min_length=9, max_length=16)
    birthday: str = Field('1814-03-09')
    additional_data: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
