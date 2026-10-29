
from datetime import date

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Bug(Base):
    __tablename__ = "bugs"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    bug_key: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(100), default="Other", nullable=False
    )
    priority: Mapped[str] = mapped_column(
        String(20), default="Medium", nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default="Open", nullable=False
    )
    assignee: Mapped[str] = mapped_column(
        String(100), default="Unassigned", nullable=False
    )
    initials: Mapped[str] = mapped_column(
        String(10), default="U", nullable=False
    )
    created_at: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
