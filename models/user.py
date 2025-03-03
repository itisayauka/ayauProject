from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_class import Base

if TYPE_CHECKING:
    from .dorama import Dorama
    from .review import Review


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Имя пользователя
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Email пользователя
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Хэш пароля (никогда не храним пароль в открытом виде)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Активен ли аккаунт
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Является ли пользователь администратором
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Дата регистрации пользователя
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    # Связь с дорамами (какие дорамы добавил пользователь)
    doramas: Mapped[list["Dorama"]] = relationship("Dorama", back_populates="author")

    # Связь с отзывами (какие отзывы оставил пользователь)
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
