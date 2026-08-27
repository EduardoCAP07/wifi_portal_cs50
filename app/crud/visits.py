from sqlalchemy import select
from app.models.lead import Lead
from app.models.visit import Visit


#TODO: Replace the hardcoded user_id for the variable of the current user id when login is implemented
def lead_visits_query(lead_id: int):
    return (
        select(
            Visit.created_at,
            Visit.ssid
        )
        .join(Lead)
        .where(
            Lead.id == lead_id,
            Lead.user_id == 1
        )
    )
