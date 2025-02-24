import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

class Item(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    author: str = Field(...)
    datetime_created: datetime = Field(...)
    isbn: str = Field(...)
    name: str = Field(...)
    price: float = Field(...)
    url: str = Field(...)

    #class Config:
    #    allow_population_by_field_name = True
    #    schema_extra = {
    #        "example": {
    #            "isbn": "0593234278",
    #            "price": 18.75,
    #            "name": "The Mediterranean Dish: 120 Bold and Healthy Recipes You'll Make on Repeat: A Mediterranean Cookbook",
    #            "author": "Suzy Karadsheh",
    #            "url": "https://www.amazon.com/Mediterranean-Dish-Healthy-Recipes-Cookbook/dp/0593234278/",
    #            "datetime": {
    #                "$date": "2025-02-18T15:32:24.535Z"
    #            }
    #        }
    #    }

class ItemUpdate(BaseModel):
    author: Optional[str]
    datetime_created: Optional[date]
    isbn: Optional[str]
    name: Optional[str]
    price: Optional[float]
    url: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "isbn": "0593234278",
                "price": 18.75,
                "name": "The Mediterranean Dish: 120 Bold and Healthy Recipes You'll Make on Repeat: A Mediterranean Cookbook",
                "author": "Suzy Karadsheh",
                "url": "https://www.amazon.com/Mediterranean-Dish-Healthy-Recipes-Cookbook/dp/0593234278/",
                "datetime": {
                    "$date": "2025-02-18T15:32:24.535Z"
                }
            }
        }