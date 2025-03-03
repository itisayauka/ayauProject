from sqlalchemy import Integer, Text, TIMESTAMP, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_class import Base


class Review(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Связь с дорамой
    dorama_id: Mapped[int] = mapped_column(ForeignKey("dorama.id"), nullable=False)
    
    # Связь с пользователем (кто оставил отзыв)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    
    # Оценка (например, от 1 до 10)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Текст отзыва
    content: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Дата публикации отзыва
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    # Связи с другими сущностями
    dorama = relationship("Dorama", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
