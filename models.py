from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="user", uselist=False)
    assigned_tickets = relationship("Ticket", back_populates="agent")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="customer")
    tickets = relationship("Ticket", back_populates="customer")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    priority = Column(String, nullable=False)
    category = Column(String, nullable=False)

    status = Column(String, default="Open")

    assigned_agent = Column(Integer, ForeignKey("users.id"), nullable=True)

    customer = relationship("Customer", back_populates="tickets")
    agent = relationship("User", back_populates="assigned_tickets")