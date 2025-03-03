from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_class import Base


class Watchlist(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Связь с пользователем
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Связь с дорамой
    dorama_id: Mapped[int] = mapped_column(ForeignKey("dorama.id"), nullable=False)

    # Статус (например, "смотрю", "запланировано", "завершено")
    status: Mapped[str] = mapped_column(String, nullable=False, default="запланировано")

    # Дата добавления в список
    added_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Связи
    user = relationship("User", back_populates="watchlist")
    dorama = relationship("Dorama", back_populates="watchlist")
