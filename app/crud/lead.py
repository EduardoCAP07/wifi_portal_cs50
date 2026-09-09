from sqlalchemy import select, and_, or_ , func, insert
from app.models.lead import Lead
from app.models.visit import Visit

# adapted from https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
#TODO: Replace the hardcoded user_id for the variable of the currrent user id when admin login feature is implemented
def select_all_query(user_id: int):
    stmt = select(
        Lead.email,
        Lead.name,
        Lead.phone,
        Lead.id
    ).where(Lead.user_id == user_id)
    return stmt

#TODO: Replace the hardcoded user_id for the variable of the currrent user id when admin login feature is implemented
def search_query(search_term: str, user_id: int):
    stmt = select(
        Lead.email,
        Lead.name,
        Lead.phone,
        Lead.id
    ).where(
        and_(
            or_(
                Lead.email.like(search_term),
                Lead.name.like(search_term),
                Lead.phone.like(search_term),
            ),
            (Lead.user_id == user_id)
        )
)
    return stmt



def count_total_leads(user_id: int):
    stmt = select(func.count()).where(Lead.user_id == user_id).select_from(Lead)
    return stmt

def get_lead_id(phone: str, user_id: int):
    stmt = select(Lead.id).where(
        and_(
            Lead.phone == phone,
            Lead.user_id == user_id
        )
    )
    return stmt
