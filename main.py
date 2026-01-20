
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
import sqlite3, os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_PATH = os.getenv("DB_PATH", "database.db")

def format_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
    except:
        return value

templates.env.filters["format_date"] = format_date

def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
def dashboard(request: Request):
    role = "dispecer"
    user_id = 1
    period = request.query_params.get("period", "day")
    sort = request.query_params.get("sort", "desc")
    now = datetime.now()
    if period == "day":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "month":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT rides.id, rides.date, rides.time, rides.start, rides.end_location, rides.status, rides.approved, rides.car_id, rides.driver_id FROM rides ORDER BY date, time")
    rides = c.fetchall()
    c.execute("SELECT ride_id, user, change, timestamp FROM ride_logs ORDER BY timestamp DESC")
    logs = c.fetchall()
    c.execute(f"SELECT users.name, COUNT(rides.id) AS count FROM users LEFT JOIN rides ON users.id = rides.driver_id WHERE users.role='ridic' AND date>=? GROUP BY users.id ORDER BY count {'DESC' if sort=='desc' else 'ASC'}", (start_date.strftime("%Y-%m-%d"),))
    drivers_load = c.fetchall()
    c.execute(f"SELECT cars.name, COUNT(rides.id) AS count FROM cars LEFT JOIN rides ON cars.id = rides.car_id WHERE rides.date>=? GROUP BY cars.id ORDER BY count {'DESC' if sort=='desc' else 'ASC'}", (start_date.strftime("%Y-%m-%d"),))
    cars_load = c.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "rides": rides, "logs": logs, "drivers_load": drivers_load, "cars_load": cars_load, "role": role, "user_id": user_id, "period": period, "sort": sort})
