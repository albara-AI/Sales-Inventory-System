from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas

router = APIRouter(prefix="/inventory", tags=["inventory"])

# Warehouse Operations
@router.get("/warehouses", response_model=List[schemas.WarehouseResponse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Warehouse).offset(skip).limit(limit).all()

@router.post("/warehouses", response_model=schemas.WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = models.Warehouse(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

# Stock Operations
@router.get("/stock/{product_id}", response_model=List[schemas.StockLevelResponse])
def get_product_stock(product_id: int, db: Session = Depends(get_db)):
    return db.query(models.StockLevel).filter(models.StockLevel.product_id == product_id).all()

@router.post("/stock", status_code=status.HTTP_201_CREATED)
def add_stock_movement(
    product_id: int, 
    warehouse_id: int, 
    quantity: int, 
    movement_type: schemas.MovementType, 
    db: Session = Depends(get_db)
):
    # 1. Record Movement
    movement = models.StockMovement(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity,
        movement_type=movement_type
    )
    db.add(movement)

    # 2. Update Stock Level
    stock_level = db.query(models.StockLevel).filter(
        models.StockLevel.product_id == product_id,
        models.StockLevel.warehouse_id == warehouse_id
    ).first()

    if not stock_level:
        if movement_type == schemas.MovementType.out:
            raise HTTPException(status_code=400, detail="Cannot remove stock from empty inventory location")
        # Create new stock level entry
        stock_level = models.StockLevel(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=0
        )
        db.add(stock_level)
    
    if movement_type == schemas.MovementType.in_:
        stock_level.quantity += quantity
    elif movement_type == schemas.MovementType.out:
        if stock_level.quantity < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        stock_level.quantity -= quantity

    db.commit()
    return {"message": "Stock updated successfully"}
