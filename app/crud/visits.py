from sqlalchemy import select, and_, or_ , func, JSON, insert
from app.models.lead import Lead
from app.models.visit import Visit
from datetime import datetime, timedelta

#TODO: Replace the hardcoded user_id for the variable of the currrent user id when login feature is implemented
def lead_visits_query(lead_id: int, user_id: int):
    stmt = (select(
        Visit.created_at,
        Visit.ssid
    ).join(Lead)
    .where(
        Lead.id == lead_id,
        Lead.user_id == user_id
    )
)
    return stmt

def count_total_visits(user_id: int):
    stmt = select(func.count(Visit.id)).join(Lead).where(Lead.user_id == user_id)
    return stmt

today = datetime.now().date()

def count_visits_today(user_id: int):
    stmt = select(func.count(Visit.id)).join(Lead).where(
        and_(
            Lead.user_id == user_id,
            Visit.created_at.like("%" + f"{today}" + "%")
        )
    )
    return stmt

# AI helped me with timedelta
start_week = (today - timedelta(days=today.weekday()))
end_week = (start_week + timedelta(days=7))

def count_visits_week(user_id: int):
    stmt = select(func.count(Visit.id)).join(Lead).where(
        and_(
            Lead.user_id == user_id,
            Visit.created_at >= start_week,
            Visit.created_at < end_week
        )
    )
    return stmt
