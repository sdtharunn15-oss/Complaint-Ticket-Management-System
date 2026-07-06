from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Customer, Ticket
from schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    TicketResponse,
)
from security import get_current_user

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# -----------------------
# Create Customer
# -----------------------
@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in ["Admin", "Customer"]:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if current_user.role == "Customer":
        already_exists = db.query(Customer).filter(
            Customer.user_id == current_user.id
        ).first()

        if already_exists:
            raise HTTPException(
                status_code=400,
                detail="Customer profile already exists"
            )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        user_id=current_user.id
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# -----------------------
# Get All Customers
# -----------------------
@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can view all customers"
        )

    return db.query(Customer).all()


# -----------------------
# Get Customer By ID
# -----------------------
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if (
        current_user.role != "Admin"
        and customer.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return customer


# -----------------------
# Update Customer
# -----------------------
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if (
        current_user.role != "Admin"
        and customer.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    email_exists = db.query(Customer).filter(
        Customer.email == customer_data.email,
        Customer.id != customer_id
    ).first()

    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    customer.name = customer_data.name
    customer.email = customer_data.email
    customer.phone = customer_data.phone
    customer.address = customer_data.address

    db.commit()
    db.refresh(customer)

    return customer


# -----------------------
# Delete Customer
# -----------------------
@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete customers"
        )

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }


# -----------------------
# Customer Tickets
# -----------------------
@router.get("/{customer_id}/tickets", response_model=list[TicketResponse])
def get_customer_tickets(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if (
        current_user.role != "Admin"
        and customer.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    tickets = db.query(Ticket).filter(
        Ticket.customer_id == customer_id
    ).all()

    return tickets