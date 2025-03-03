from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_class import Base


class Voiceover(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Связь с дорамой
    dorama_id: Mapped[int] = mapped_column(ForeignKey("dorama.id"), nullable=False)
    
    # Тип (озвучка или субтитры)
    type: Mapped[str] = mapped_column(String, nullable=False)  # "озвучка" / "субтитры"
    
    # Студия озвучки
    studio: Mapped[str] = mapped_column(String, nullable=True)

    # Связь с моделью Dorama
    dorama = relationship("Dorama", back_populates="voiceovers")
