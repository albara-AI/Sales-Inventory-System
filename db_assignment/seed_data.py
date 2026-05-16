from database import SessionLocal, engine
import models
from schemas import MovementType
import datetime

def seed_data():
    db = SessionLocal()
    
    # Check if we have data
    if db.query(models.Customer).first():
        print("Data already exists. Skipping.")
        db.close()
        return

    print("Seeding data...")

    # 1. Create Default Customer
    customer = models.Customer(
        name="John Doe",
        phone="555-0123",
        country="USA"
    )
    db.add(customer)
    
    # 2. Create Warehouses
    w1 = models.Warehouse(name="Main Warehouse", location="New York")
    w2 = models.Warehouse(name="West Warehouse", location="California")
    db.add(w1)
    db.add(w2)
    db.commit() # Get IDs

    # 3. Create Products
    p1 = models.Product(name="Laptop", sku="LAP-001", unit_price=999.99, description="High perf laptop")
    p2 = models.Product(name="Mouse", sku="MOU-001", unit_price=29.99, description="Wireless mouse")
    p3 = models.Product(name="Monitor", sku="MON-001", unit_price=199.99, description="24 inch monitor")
    db.add(p1)
    db.add(p2)
    db.add(p3)
    db.commit()

    # 4. Add Initial Stock (via Movement manually or logic)
    # We should also create StockLevel entries
    # Laptop in Main: 50
    sl1 = models.StockLevel(product_id=p1.product_id, warehouse_id=w1.warehouse_id, quantity=50)
    # Mouse in West: 100
    sl2 = models.StockLevel(product_id=p2.product_id, warehouse_id=w2.warehouse_id, quantity=100)
    # Monitor in Main: 20
    sl3 = models.StockLevel(product_id=p3.product_id, warehouse_id=w1.warehouse_id, quantity=20)
    
    db.add(sl1)
    db.add(sl2)
    db.add(sl3)
    
    # Record movements
    m1 = models.StockMovement(product_id=p1.product_id, warehouse_id=w1.warehouse_id, quantity=50, movement_type=MovementType.in_)
    m2 = models.StockMovement(product_id=p2.product_id, warehouse_id=w2.warehouse_id, quantity=100, movement_type=MovementType.in_)
    m3 = models.StockMovement(product_id=p3.product_id, warehouse_id=w1.warehouse_id, quantity=20, movement_type=MovementType.in_)
    
    db.add(m1)
    db.add(m2)
    db.add(m3)

    db.commit()
    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed_data()
