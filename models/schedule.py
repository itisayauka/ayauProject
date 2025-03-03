from sqlalchemy import Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_class import Base


class Schedule(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Связь с дорамой
    dorama_id: Mapped[int] = mapped_column(ForeignKey("dorama.id"), nullable=False)
    
    # Номер серии
    episode_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Дата выхода серии
    release_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    # Связь с моделью Dorama
    dorama = relationship("Dorama", back_populates="schedules")
