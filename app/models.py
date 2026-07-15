from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class Check(Base):
    __tablename__ = "checks"

    # Уникальный идентификатор проверки
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Тип программы: federal или regional
    program = Column(String, nullable=False)
    
    # Текущий статус проверки
    status = Column(String, nullable=False)
    
    # Список загруженных документов
    documents = Column(JSON, nullable=False, default=list)
    
    # Все найденные проблемы (ошибки и предупреждения)
    issues = Column(JSON, nullable=True, default=list)
    
    # Данные, извлечённые из документов
    extracted = Column(JSON, nullable=True, default=dict)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)