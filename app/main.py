from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI", "version": settings.APP_VERSION}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
