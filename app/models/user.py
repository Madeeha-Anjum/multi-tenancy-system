import sqlalchemy as sa

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    email = sa.Column(sa.String, unique=True, index=True)
    degree = sa.Column(sa.String, index=True)
