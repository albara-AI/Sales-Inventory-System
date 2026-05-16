# 🏪 Sales & Inventory Management System

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)](https://mysql.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)](https://sqlalchemy.org)
[![Jinja2](https://img.shields.io/badge/Jinja2-Templates-purple)]()

> **Full-stack web application replacing manual spreadsheets with a centralized,
> automated Sales & Inventory database system.**
> Advanced Database Systems — The Hashemite University, 2025.

**Team:**
| Name 
|------
| **Albara Aljaber**
| Mohammad Ismail Mahmoud Sa'ada 
| Khaled Mohammad Othman Saleh 
| Mohanad Jaber Mohammad Assaf


**Instructor:** Dr. Mahmoud Odeh

---

## 📌 Problem Statement

A retail business running on disconnected spreadsheets faced:
- **Conflicting data** — same info in multiple files, versions diverge
- **Manual stock updates** — slow, error-prone, causes phantom inventory
- **No audit trail** — impossible to trace who changed what
- **Slow reporting** — hours of copy-paste to generate basic summaries

**Solution**: One centralized relational database with an automated web interface that handles all business logic server-side.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│              Browser (HTML/CSS/JS)           │
│   ┌──────────────┐    ┌───────────────────┐ │
│   │ Admin Panel  │    │  User Storefront  │ │
│   └──────┬───────┘    └────────┬──────────┘ │
└──────────┼──────────────────────┼────────────┘
           │   HTTP Requests      │
┌──────────▼──────────────────────▼────────────┐
│              FastAPI Backend                  │
│  ┌─────────┐ ┌──────────┐ ┌───────────────┐  │
│  │inventory│ │ orders   │ │   products    │  │
│  │ router  │ │ router   │ │   router      │  │
│  └────┬────┘ └────┬─────┘ └──────┬────────┘  │
│       └───────────┴──────────────┘            │
│              SQLAlchemy ORM                   │
└──────────────────┬────────────────────────────┘
                   │
┌──────────────────▼────────────────────────────┐
│                MySQL Database                  │
│  customers │ products │ warehouses │ orders    │
│  order_items │ stock_levels │ stock_movements  │
└────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema — 7 Tables

```sql
customers      → customer_id (PK), name, phone, country
products       → product_id (PK), sku (UNIQUE), name, unit_price, description
warehouses     → warehouse_id (PK), name, location
orders         → order_id (PK), customer_id (FK), status ENUM, total_amount
order_items    → order_item_id (PK), order_id (FK), product_id (FK),
                 quantity, unit_price  ← historical price snapshot
stock_levels   → stock_level_id (PK), product_id (FK), warehouse_id (FK),
                 quantity             ← real-time source of truth
stock_movements→ movement_id (PK), product_id (FK), warehouse_id (FK),
                 quantity, movement_type ('in'/'out')  ← immutable audit log
```

### Key Design Decisions
- `order_items.unit_price` stores the price **at time of sale** — historical accuracy even if product price changes later
- `stock_levels` = current state · `stock_movements` = full history (separation of concerns)
- Foreign key constraints prevent orphaned records (e.g., can't delete a customer with active orders)
- `status` ENUM restricts order states to `'ordered'` / `'delivered'`

---

## 📁 Project Structure

```
db_assignment/
├── main.py                 ← FastAPI app entry point
├── database.py             ← SQLAlchemy engine & session
├── models.py               ← ORM models (all 7 tables)
├── schemas.py              ← Pydantic request/response schemas
├── create_database.py      ← Database creation script
├── init_db.py              ← Table initialization
├── seed_data.py            ← Sample data loader
├── verify_backend.py       ← Health check script
├── routers/
│   ├── inventory.py        ← Stock level & movement endpoints
│   ├── orders.py           ← Order creation & management
│   ├── products.py         ← Product CRUD
│   └── reports.py          ← Sales & inventory reports
├── templates/
│   ├── index.html          ← Login page
│   ├── admin.html          ← Admin dashboard
│   └── user.html           ← User storefront
├── static/
│   ├── style.css           ← Custom responsive styles
│   └── script.js           ← Client-side interactivity
├── requirements.txt
└── README.md
```

---

## ✨ Features

### Admin Dashboard
- 📊 **Real-time stats**: Total revenue, total orders, system status
- 📦 **Product management**: Add / edit / delete products with SKU validation
- 🏭 **Warehouse management**: Add locations, view all warehouses
- 🔍 **Stock checker**: Query quantity of any product across warehouses
- 📈 **Stock movement form**: Record IN (restock) / OUT (removal) with full audit trail

### User Storefront
- 🛍️ **Product grid**: Browse available catalog with real-time stock status
- 🛒 **Cart system**: Add items dynamically, cart counter in header
- ✅ **Order placement**: System validates stock before confirming — no overselling
- 📋 **Order history**: View past purchases

### Business Rules (Enforced Server-Side)
- ❌ Cannot place order if stock is insufficient
- 🔄 Stock levels update **automatically** the moment an order is confirmed
- 🔒 Every stock change writes to `stock_movements` (immutable audit log)
- ⚡ Transactions: orders are either 100% complete or fully rolled back (no partial updates)

---

## 🚀 Quick Start

### 1. Clone & install
```bash
git clone https://github.com/[your-username]/sales-inventory-system
cd sales-inventory-system
pip install -r requirements.txt
```

### 2. Configure MySQL
```bash
# Create a MySQL database
mysql -u root -p
CREATE DATABASE sales_inventory;
EXIT;
```

### 3. Set up environment
Create a `.env` file:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=sales_inventory
```

### 4. Initialize & seed the database
```bash
python create_database.py
python init_db.py
python seed_data.py
```

### 5. Run the application
```bash
uvicorn main:app --reload
```

Open `http://localhost:8000` — login as **Admin** or **User**.

### 6. Verify everything works
```bash
python verify_backend.py
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10 | Core backend logic |
| Web Framework | FastAPI | API routing, request handling |
| Database | MySQL 8.0 | Relational data storage |
| ORM | SQLAlchemy | Python ↔ MySQL abstraction |
| Templates | Jinja2 | Server-side HTML rendering |
| Frontend | HTML + CSS + Vanilla JS | Responsive UI, dynamic DOM |
| Validation | Pydantic | Request/response schema validation |

---

## 📊 API Endpoints (Sample)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | List all products |
| `POST` | `/products` | Add new product |
| `POST` | `/orders` | Place new order (validates stock) |
| `GET` | `/inventory/stock` | Check current stock levels |
| `POST` | `/inventory/movement` | Record IN/OUT stock movement |
| `GET` | `/reports/sales` | Sales summary report |
| `GET` | `/docs` | Auto-generated FastAPI docs |

---

## 📬 Contact


**Albaraa Aljaber** — Data Science & AI, The Hashemite University
📧 [albaraaljaberwork@gmail.com]
💼 [https://www.linkedin.com/in/albara-aljaber/]

