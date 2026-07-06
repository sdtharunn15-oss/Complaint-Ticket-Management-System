from fastapi import FastAPI

from database import Base, engine
import models

from routers.auth import router as auth_router
from routers.customers import router as customer_router
from routers.tickets import router as ticket_router
from routers.agents import router as agent_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Complaint & Ticket Management System"
)

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(ticket_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "message": "Complaint & Ticket Management API is running"
    }