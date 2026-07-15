from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Check
from app.schemas import CheckResponse, CheckListResponse
from app.services.check_service import process_check
from app.utils.file_utils import get_file_extension

router = APIRouter(prefix="/api/checks", tags=["checks"])

def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CheckResponse)
async def create_check(
    files: List[UploadFile] = File(...),
    program: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Создаёт новую проверку пакета документов.
    Принимает файлы и название программы.
    """
    # Проверяем программу
    if program not in ['federal', 'regional']:
        raise HTTPException(
            status_code=422,
            detail="Программа должна быть 'federal' или 'regional'"
        )

    if not files:
        raise HTTPException(
            status_code=422,
            detail="Файлы не загружены"
        )

    # Читаем загруженные файлы
    file_infos = []
    for file in files:
        content = await file.read()
        file_infos.append({
            'filename': file.filename,
            'content': content,
            'extension': get_file_extension(file.filename)
        })

    result = process_check(file_infos, program)
    return result

@router.get("/", response_model=List[CheckListResponse])
def list_checks(db: Session = Depends(get_db)):
    """
    Возвращает список всех проверок.
    Сортировка по дате создания (новые сверху).
    """
    checks = db.query(Check).order_by(Check.created_at.desc()).all()
    
    result = []
    for check in checks:
        doc_count = len(check.documents) if check.documents else 0
        result.append({
            "id": check.id,
            "program": check.program,
            "status": check.status,
            "doc_count": doc_count,
            "created_at": check.created_at
        })
    
    return result

@router.get("/{check_id}", response_model=CheckResponse)
def get_check(check_id: str, db: Session = Depends(get_db)):
    """
    Возвращает детальную информацию о конкретной проверке.
    """
    # Проверяем корректность UUID
    try:
        import uuid
        check_uuid = uuid.UUID(check_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Проверка не найдена")

    # Ищем проверку в базе
    check = db.query(Check).filter(Check.id == check_uuid).first()
    if not check:
        raise HTTPException(status_code=404, detail="Проверка не найдена")

    # Тексты статусов для ответа
    status_labels = {
        'approved': 'Можно заявлять в банк',
        'rejected': 'Нельзя заявлять в банк',
        'check_in_progress': 'Требуется проверка'
    }

    return {
        "check_id": str(check.id),
        "status": check.status,
        "status_label": status_labels.get(check.status, 'Неизвестно'),
        "reason": None,
        "issues": check.issues or [],
        "documents": check.documents or [],
        "extracted": check.extracted or {},
        "checked_at": check.created_at.isoformat() + "Z"
    }