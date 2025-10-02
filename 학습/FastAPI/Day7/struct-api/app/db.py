from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite 파일 DB. 메모리 DB 원하면 sqlite:///:memory:
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 전용 옵션
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


# FastAPI 의존성에서 사용할 세션 팩토리
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
