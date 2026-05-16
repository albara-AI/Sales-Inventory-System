from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    ordered = "ordered"
    delivered = "delivered"

class MovementType(str, Enum):
    in_ = "in"
    out = "out"

# Product Schemas
class ProductBase(BaseModel):
    name: str
    sku: str
    unit_price: float
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Warehouse Schemas
class WarehouseBase(BaseModel):
    name: str
    location: str
    description: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseResponse(WarehouseBase):
    warehouse_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Inventory/Stock Schemas
class StockLevelResponse(BaseModel):
    stock_level_id: int
    product_id: int
    warehouse_id: int
    quantity: int
    product: Optional[ProductResponse] = None # Optional to avoid circular dep if needed
    warehouse: Optional[WarehouseResponse] = None

    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    phone: str
    country: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Order Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemBase]

class OrderItemResponse(OrderItemBase):
    order_item_id: int
    unit_price: float
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    status: OrderStatus
    total_amount: float
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
