from datetime import datetime
import uuid
from app.services.validation_service import validate_package
from app.models import Check
from app.database import SessionLocal
from app.utils.file_utils import detect_file_type, get_file_size_kb

def process_check(files, program):
    """
    Основная функция обработки проверки документов.
    Валидирует, определяет статус, сохраняет в БД.
    """
    # 1. Валидация пакета документов
    issues, warnings = validate_package(files, program)

    # 2. Определяем статус проверки
    has_errors = any(i['level'] == 'error' for i in issues)
    has_warnings = len(warnings) > 0

    if has_errors:
        status = "rejected"
        status_label = "Нельзя заявлять в банк"
        reason = issues[0]['message']
    elif has_warnings:
        status = "check_in_progress"
        status_label = "Требуется проверка"
        reason = "Обнаружены предупреждения"
    else:
        status = "approved"
        status_label = "Можно заявлять в банк"
        reason = None

    # 3. Собираем информацию о документах
    documents = []
    for file_info in files:
        filename = file_info['filename']
        content = file_info['content']
        doc_type = detect_file_type(filename) or "unknown"
        
        documents.append({
            "name": filename,
            "detected_type": doc_type,
            "size_kb": round(get_file_size_kb(content), 2)
        })

    # 4. Извлечение данных (пока заглушка, потом подключим AI)
    extracted = {
        "contractor": "ООО «ТехАгро»",
        "amount": "1 250 000 ₽",
        "date": "01.03.2025",
        "subject": "Поставка минеральных удобрений"
    }

    all_issues = issues + warnings

    # 5. Сохраняем результат в базу данных
    db = SessionLocal()
    try:
        check = Check(
            id=uuid.uuid4(),
            program=program,
            status=status,
            documents=documents,
            issues=all_issues,
            extracted=extracted
        )
        db.add(check)
        db.commit()
        db.refresh(check)

        # 6. Формируем ответ
        return {
            "check_id": str(check.id),
            "status": status,
            "status_label": status_label,
            "reason": reason,
            "issues": all_issues,
            "documents": documents,
            "extracted": extracted,
            "checked_at": datetime.utcnow().isoformat() + "Z"
        }
    finally:
        db.close()