from pydantic import BaseModel, Field, AnyUrl, EmailStr, field_validator, computed_field, model_validator
from uuid import UUID
from typing import Annotated, Literal, Optional, List
from datetime import datetime

# -----------------------
# Dimension
# -----------------------
class DimensionCM(BaseModel):
    length: float = Field(gt=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)

class Seller(BaseModel):
    seller_id: UUID
    name: str = Field(min_length=3, max_length=80)
    email: EmailStr
    website: AnyUrl

    @field_validator("email", mode="after")
    @classmethod
    def validate_email_domain(cls, value: EmailStr):
        allowed = {
            "samsungindia.in", "lenovostore.in", "hpworld.in", "applestoreindia.in",
            "dellexclusive.in", "sonycenter.in", "oneplusstore.in", "asusexclusive.in"
        }
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed:
            raise ValueError(f"Seller email domain not allowed: {domain}")
        return value

# -----------------------
# Product Full Model
# -----------------------
class Product(BaseModel):
    id: UUID
    sku: str = Field(min_length=6, max_length=36)
    name: str = Field(min_length=3, max_length=80)
    description: str = Field(min_length=2, max_length=50)
    category: str
    brand: str
    price: float = Field(gt=0)
    discount_percent: int = Field(ge=0, le=90, default=0)
    stock: float = Field(gt=0)
    is_active: bool = True
    rating: int = Field(ge=0, le=5)
    currency: Literal["INR"] = "INR"
    tags: Optional[List[str]] = Field(default_factory=list)
    image_urls: List[AnyUrl] = Field(min_items=1)
    dimensions_cm: DimensionCM
    seller: Seller
    created_at: datetime

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)

# -----------------------
# Product Update Model
# -----------------------
class DimensionCMUpdate(BaseModel):
    length: Optional[float]
    width: Optional[float]
    height: Optional[float]

class SellerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    website: Optional[AnyUrl]

    @field_validator("email", mode="after")
    @classmethod
    def validate_email_domain(cls, value: EmailStr):
        allowed = {
            "mistore.in","realmeofficial.in","samsungindia.in","lenovostore.in",
            "hpworld.in","applestore.in","dellexclusive.in","sonycenter.in",
            "oneplusstore.in","asusexclusive.in"
        }
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed:
            raise ValueError(f"Seller email domain not allowed: {domain}")
        return value

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    brand: Optional[str]
    price: Optional[float]
    discount_percent: Optional[int]
    stck: Optional[float]
    is_active: Optional[bool]
    rating: Optional[int]
    currency: Optional[Literal["INR"]]
    tags: Optional[List[str]]
    image_urls: Optional[List[AnyUrl]]
    dimensions_cm: Optional[DimensionCMUpdate]
    seller: Optional[SellerUpdate]
