from pydantic import BaseModel, Field, HttpUrl
from typing import List

from pydantic import validator, ValidationError

class Product(BaseModel):
    product_title: str = Field(..., min_length=1, max_length=255)
    product_price: float = Field(..., ge=0.0)
    image_url: str

    @validator('product_price')
    def check_price(cls, v):
        if v <= 0:
            raise ValueError('Product price must be positive')
        return v


class ScrapedData(BaseModel):
    products: List[Product]
