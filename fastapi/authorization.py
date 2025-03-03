from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
import jwt
import datetime

# Настройки базы данных
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# Хеширование пароля
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройки JWT-токена
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# Инициализация FastAPI
app = FastAPI()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Регистрация пользователя (для теста)
@app.post("/register/")
def register(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

# Авторизация пользователя
@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Генерация JWT-токена (код)
    token_data = {
        "sub": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}
