from pydantic import HttpUrl,BaseModel


class URLBase(BaseModel):
     long_url:str


class Urlryic(BaseModel):
    long_url:str
    