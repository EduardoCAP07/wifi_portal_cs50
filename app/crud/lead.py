from sqlalchemy import select
from app.models.lead import Lead


# adapted from https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
#TODO: Replace the hardcoded user_id for the variable of the currrent user id when login feature is implemented
select_all_query = select(
    Lead.created_at,
    Lead.name,
    Lead.ssid,
    Lead.phone
).where(Lead.user_id == 1)

