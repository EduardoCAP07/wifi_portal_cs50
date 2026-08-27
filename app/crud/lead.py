from sqlalchemy import select, and_, or_
from app.models.lead import Lead


# adapted from https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
#TODO: Replace the hardcoded user_id for the variable of the currrent user id when admin login feature is implemented
select_all_query = select(
    Lead.email,
    Lead.name,
    Lead.phone
).where(Lead.user_id == 1)

#TODO: Replace the hardcoded user_id for the variable of the currrent user id when admin login feature is implemented
def search_query(search_term: str):
    stmt = select(
        Lead.email,
        Lead.name,
        Lead.phone
    ).where(
        and_(
            or_(
                Lead.email.like(search_term),
                Lead.name.like(search_term),
                Lead.phone.like(search_term),
            ),
            (Lead.user_id == 1)
        )
)
    return stmt

