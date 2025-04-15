import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

class Item(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    datetime_created: datetime = Field(...)
    product_id: str = Field(...)
    name: str = Field(...)
    price: float = Field(...)
    url: str = Field(...)
    currency: str = Field(...)
    type: str = Field(...)
    seller: str = Field(...)
    original_price: float = Field(...)
    email: str = Field(...)

    #class Config:
    #    allow_population_by_field_name = True
    #    schema_extra = {
    #        "example": {
    #            "product_id": "0593234278",
    #            "price": 18.75,
    #            "name": "The Mediterranean Dish: 120 Bold and Healthy Recipes You'll Make on Repeat: A Mediterranean Cookbook",
    #            "author": "Suzy Karadsheh",
    #            "url": "https://www.amazon.com/Mediterranean-Dish-Healthy-Recipes-Cookbook/dp/0593234278/",
    #            "datetime": {
    #                "$date": "2025-02-18T15:32:24.535Z"
    #            }
    #        }
    #    }

class Clothing(Item):
    brand: str = Field(...)

class Book(Item):
    author: str = Field(...)
    format: str = Field(...)

class VideoGame(Item):
    format: str = Field(...)

class ItemUpdate(BaseModel):
    author: Optional[str]
    datetime_created: Optional[date]
    product_id: Optional[str]
    name: Optional[str]
    price: Optional[float]
    url: Optional[str]
    format: Optional[str]
    currency: str = Field(...)
    brand: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "product_id": "0593234278",
                "price": 18.75,
                "name": "The Mediterranean Dish: 120 Bold and Healthy Recipes You'll Make on Repeat: A Mediterranean Cookbook",
                "author": "Suzy Karadsheh",
                "url": "https://www.amazon.com/Mediterranean-Dish-Healthy-Recipes-Cookbook/dp/0593234278/",
                "datetime": {
                    "$date": "2025-02-18T15:32:24.535Z"
                },
                "format": "Hardcover",
                "currency": "$"
            }
        }

class AlertEmailItem:
    def __init__(self, product_name, product_url, sale_price, original_price, currency, email):
        self.product_name = product_name
        self.product_url = product_url
        self.sale_price = sale_price
        self.original_price = original_price
        self.currency = currency
        self.email = email

class Log(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    datetime_created: datetime = Field(...)
    product_id: str = Field(...)
    url: str = Field(...)
    subject: str = Field(...)
    exception_type: str = Field(...)
    error_message: str = Field(...)