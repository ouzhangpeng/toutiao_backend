"""
共享的 SQLAlchemy Base 类
所有模型都应该继承自这个 Base
"""

from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class CreateUpdateBase(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="修改时间"
    )


class CreateBase(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="创建时间"
    )
