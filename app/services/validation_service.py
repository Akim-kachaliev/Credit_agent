from app.utils.file_utils import detect_file_type, is_allowed_format, get_file_size_kb

# Какие документы нужны для каждой программы
REQUIRED_DOCS = {
    'federal': ['contract', 'specification', 'invoice', 'act'],
    'regional': ['contract', 'invoice', 'act']
}

# Названия документов для вывода пользователю
DOC_NAMES = {
    'contract': 'договор',
    'specification': 'спецификация',
    'invoice': 'счёт',
    'act': 'акт/УПД'
}

# Максимальный размер файла (20 МБ в килобайтах)
MAX_FILE_SIZE_KB = 20 * 1024

def validate_package(files, program):
    """
    Проверяет пакет документов на соответствие требованиям.
    Возвращает список ошибок и список предупреждений.
    """
    errors = []
    warnings = []
    found_types = []

    # Проверяем каждый файл
    for file_info in files:
        filename = file_info['filename']
        content = file_info['content']
        
        # Проверка расширения
        if not is_allowed_format(filename):
            errors.append({
                'level': 'error',
                'message': f'Недопустимый формат файла: {filename} (разрешены: PDF, DOCX, JPG, PNG)'
            })
            continue

        # Проверка размера
        size_kb = get_file_size_kb(content)
        if size_kb > MAX_FILE_SIZE_KB:
            errors.append({
                'level': 'error',
                'message': f'Файл превышает 20 МБ: {filename} ({size_kb:.1f} КБ)'
            })

        # Определяем тип документа
        doc_type = detect_file_type(filename)
        if doc_type:
            found_types.append(doc_type)
        else:
            warnings.append({
                'level': 'warning',
                'message': f'Не удалось определить тип документа: {filename}'
            })

    # Проверяем наличие всех обязательных документов
    required = REQUIRED_DOCS.get(program, [])
    missing = [doc for doc in required if doc not in found_types]

    for doc in missing:
        errors.append({
            'level': 'error',
            'message': f'Отсутствует обязательный документ: {DOC_NAMES.get(doc, doc)}'
        })

    return errors, warnings