from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

from routers import products, inventory, orders, reports
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(orders.router)
app.include_router(reports.router)

from fastapi import Request
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/user", response_class=HTMLResponse)
def user_dashboard(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

