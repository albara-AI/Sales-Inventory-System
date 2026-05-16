from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=List[schemas.OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Order).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Calculate total and verify stock
    total_amount = 0.0
    
    # Needs logic to pick a warehouse. For simplicity, we might assume a default warehouse or pick the first one with stock.
    # OR, we simplify and just say "stock is global" but schema has warehouses.
    # Requirement 4: "Allow users to process customer orders and automatically update stock levels."
    # Strat: Loop items, find stock in ANY warehouse, decrement.
    
    # Start Transaction implicitly via Session
    
    new_order = models.Order(
        customer_id=order.customer_id,
        status=schemas.OrderStatus.ordered,
        total_amount=0 # Will update
    )
    db.add(new_order)
    db.flush() # Get ID

    for item in order.items:
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        # Check Stock
        # Simple strategy: Aggregate stock across all warehouses
        total_stock = db.query(models.StockLevel).filter(models.StockLevel.product_id == item.product_id).all()
        current_qty = sum([s.quantity for s in total_stock])
        
        if current_qty < item.quantity:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        # Decrement Stock
        # We need to take from specific warehouses.
        remaining_to_take = item.quantity
        for stock_entry in total_stock:
            if remaining_to_take <= 0:
                break
            
            take = min(stock_entry.quantity, remaining_to_take)
            stock_entry.quantity -= take
            remaining_to_take -= take
            
            # Record Movement (OUT)
            movement = models.StockMovement(
                product_id=item.product_id,
                warehouse_id=stock_entry.warehouse_id,
                quantity=take,
                movement_type=schemas.MovementType.out
            )
            db.add(movement)
            
        order_item = models.OrderItem(
            order_id=new_order.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.unit_price
        )
        db.add(order_item)
        total_amount += product.unit_price * item.quantity

    new_order.total_amount = total_amount
    db.commit()
    db.refresh(new_order)
    return new_order
