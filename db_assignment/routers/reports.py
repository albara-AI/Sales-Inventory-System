from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any
from database import get_db
import models

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. Sales Summary (Total Revenue, Total Orders)
    total_revenue = db.query(func.sum(models.Order.total_amount)).scalar() or 0.0
    total_orders = db.query(func.count(models.Order.order_id)).scalar() or 0
    
    # 2. Product Availability (Total Stock per Product)
    # Group by product and sum quantity
    stock_stats = db.query(
        models.Product.name,
        func.sum(models.StockLevel.quantity).label("total_stock")
    ).join(models.StockLevel).group_by(models.Product.product_id).all()
    
    product_availability = [{"name": s[0], "stock": s[1]} for s in stock_stats]
    
    # 3. Top Customers (By Total Spend)
    top_customers_query = db.query(
        models.Customer.name,
        func.sum(models.Order.total_amount).label("total_spent")
    ).join(models.Order).group_by(models.Customer.customer_id).order_by(desc("total_spent")).limit(5).all()
    
    top_customers = [{"name": c[0], "spent": c[1]} for c in top_customers_query]
    
    return {
        "summary": {
            "total_revenue": total_revenue,
            "total_orders": total_orders
        },
        "product_availability": product_availability,
        "top_customers": top_customers
    }
