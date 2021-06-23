from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from app.api.dependencies import get_db
from app.config import settings


def get_url():
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    db = settings.POSTGRES_DB
    server = settings.POSTGRES_SERVER
    return f"postgresql://{user}:{password}@{server}/{db}"


SQLALCHEMY_DATABASE_URL = get_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


# noinspection PyUnboundLocalVariable
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        try:
            db.close()
        except Exception as e:
            print("failed to close db", repr(e))


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
