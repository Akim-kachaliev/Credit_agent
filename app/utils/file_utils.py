import os

# Разрешённые расширения файлов
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.jpg', '.png'}

# Ключевые слова для определения типа документа
DOC_TYPES = {
    'contract': ['договор', 'contract'],
    'specification': ['спецификация', 'specification'],
    'invoice': ['счёт', 'счет', 'invoice'],
    'act': ['акт', 'упд', 'act', 'upd']
}

def detect_file_type(filename):
    """
    Определяет тип документа по имени файла.
    Возвращает: contract, specification, invoice, act или None
    """
    name = filename.lower()
    
    for doc_type, keywords in DOC_TYPES.items():
        for keyword in keywords:
            if keyword in name:
                return doc_type
    
    return None

def get_file_extension(filename):
    """Возвращает расширение файла"""
    return os.path.splitext(filename)[1].lower()

def is_allowed_format(filename):
    """Проверяет, разрешён ли формат файла"""
    ext = get_file_extension(filename)
    return ext in ALLOWED_EXTENSIONS

def get_file_size_kb(content):
    """Возвращает размер файла в килобайтах"""
    return len(content) / 1024