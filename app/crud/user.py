from sqlalchemy import select, and_, or_ , insert
from app.models.user import User

def get_user_email_stmt(email: str) -> str:
    stmt = select(User).where(User.email == email)
    return stmt

def get_user_id_stmt(id: int, version: int) -> str:
    stmt = select(User).where(and_(User.id == id, User.session_version == version))
    return stmt

def get_version_id_stmt(id: int) -> str:
    stmt = select(User.session_version).where(User.id == id)
    return stmt
