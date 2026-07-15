from fastapi import FastAPI
from app.routers import checks
from app.database import engine, Base

# Создаём приложение
app = FastAPI(
    title="Credit Document Checker API",
    description="API для проверки документов по кредитным программам",
    version="1.0.0"
)

# Создаём таблицы в базе данных (если их нет)
Base.metadata.create_all(bind=engine)

# Подключаем роутеры
app.include_router(checks.router)

@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": "Credit Document Checker API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "healthy"}