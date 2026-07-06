from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Ticket, User
from schemas import TicketResponse
from security import get_current_user

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


@router.post("/tickets/{ticket_id}/assign/{agent_id}")
def assign_ticket(
    ticket_id: int,
    agent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can assign tickets"
        )

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    agent = db.query(User).filter(
        User.id == agent_id,
        User.role == "Support Agent"
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Support Agent not found"
        )

    ticket.assigned_agent = agent.id

    db.commit()

    return {
        "message": "Ticket assigned successfully"
    }


@router.get("/{agent_id}/tickets", response_model=list[TicketResponse])
def get_agent_tickets(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if (
        current_user.role != "Admin"
        and current_user.id != agent_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    tickets = db.query(Ticket).filter(
        Ticket.assigned_agent == agent_id
    ).all()

    return tickets