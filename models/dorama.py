from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, TIMESTAMP, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .review import Review
    from .voiceover import Voiceover


class Dorama(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Название дорамы
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Слаг для URL (например, "moj-idealnyj-sekretar")
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Описание дорамы
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Жанр (например, "Романтика, Драма")
    genre: Mapped[str] = mapped_column(String, nullable=True)

    # Рейтинг дорамы (например, 8.5)
    rating: Mapped[float] = mapped_column(Float, nullable=True)

    # Автор (пользователь, который добавил дораму)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship("User", back_populates="doramas")

    # Дата создания
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    # Активна ли дорама (например, для модерации)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Связи
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="dorama")
    voiceovers: Mapped[list["Voiceover"]] = relationship("Voiceover", back_populates="dorama")
