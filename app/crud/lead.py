from sqlalchemy import select
from app.models.lead import Lead


# adapted from https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
test1 = select(Lead).where(Lead.ssid.in_(["La Fleur - WiFi"]))

