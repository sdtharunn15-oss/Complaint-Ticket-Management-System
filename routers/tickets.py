from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models import Ticket, Customer
from schemas import TicketCreate, TicketUpdate, TicketResponse
from security import get_current_user

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# -----------------------
# Create Ticket
# -----------------------
@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role not in ["Admin", "Customer"]:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    customer = db.query(Customer).filter(
        Customer.id == ticket.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Customer can create only their own tickets
    if (
        current_user.role == "Customer"
        and customer.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can create tickets only for yourself"
        )

    if ticket.priority not in ["High", "Medium", "Low"]:
        raise HTTPException(
            status_code=400,
            detail="Priority must be High, Medium or Low"
        )

    new_ticket = Ticket(
        customer_id=ticket.customer_id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        category=ticket.category,
        status="Open"
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# -----------------------
# Get All Tickets
# -----------------------
@router.get("/", response_model=list[TicketResponse])
def get_all_tickets(
    title: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    query = db.query(Ticket)

    if current_user.role == "Customer":

        customer = db.query(Customer).filter(
            Customer.user_id == current_user.id
        ).first()

        if customer:
            query = query.filter(
                Ticket.customer_id == customer.id
            )

    elif current_user.role == "Support Agent":

        query = query.filter(
            Ticket.assigned_agent == current_user.id
        )

    if title:
        query = query.filter(
            Ticket.title.ilike(f"%{title}%")
        )

    if priority:
        query = query.filter(
            Ticket.priority == priority
        )

    if status:
        query = query.filter(
            Ticket.status == status
        )

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()


# -----------------------
# Get Ticket
# -----------------------
@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    customer = db.query(Customer).filter(
        Customer.id == ticket.customer_id
    ).first()

    if (
        current_user.role == "Customer"
        and customer.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    if (
        current_user.role == "Support Agent"
        and ticket.assigned_agent != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return ticket


# -----------------------
# Update Ticket
# -----------------------
@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if ticket.status == "Closed":
        raise HTTPException(
            status_code=400,
            detail="Closed tickets cannot be updated"
        )

    if (
        current_user.role == "Support Agent"
        and ticket.assigned_agent != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only assigned agent can update this ticket"
        )

    if ticket_data.priority:
        if ticket_data.priority not in ["High", "Medium", "Low"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid priority"
            )

    if ticket_data.status:
        if ticket_data.status not in [
            "Open",
            "In Progress",
            "Resolved",
            "Closed"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Invalid status"
            )

    update_data = ticket_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return ticket


# -----------------------
# Delete Ticket
# -----------------------
@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete tickets"
        )

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }