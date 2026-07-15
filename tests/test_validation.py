import pytest
from app.services.validation_service import validate_package
from app.utils.file_utils import detect_file_type

# === Тесты определения типа документа ===

def test_detect_contract():
    """Должен определять договор"""
    assert detect_file_type('договор_поставки.pdf') == 'contract'
    assert detect_file_type('contract_123.pdf') == 'contract'

def test_detect_specification():
    """Должен определять спецификацию"""
    assert detect_file_type('спецификация_товаров.xlsx') == 'specification'
    assert detect_file_type('specification.pdf') == 'specification'

def test_detect_invoice():
    """Должен определять счёт"""
    assert detect_file_type('счёт_на_оплату.pdf') == 'invoice'
    assert detect_file_type('invoice_123.pdf') == 'invoice'

def test_detect_act():
    """Должен определять акт и УПД"""
    assert detect_file_type('акт_выполненных_работ.pdf') == 'act'
    assert detect_file_type('УПД_123.pdf') == 'act'

def test_detect_unknown():
    """Неизвестный тип должен возвращать None"""
    assert detect_file_type('scan_0041.jpg') is None
    assert detect_file_type('фото.png') is None

# === Тесты валидации пакетов ===

def test_validate_federal_all_docs():
    """Федеральная программа: все 4 документа - успех"""
    files = [
        {'filename': 'договор.pdf', 'content': b'test', 'extension': '.pdf'},
        {'filename': 'спецификация.pdf', 'content': b'test', 'extension': '.pdf'},
        {'filename': 'счёт.pdf', 'content': b'test', 'extension': '.pdf'},
        {'filename': 'акт.pdf', 'content': b'test', 'extension': '.pdf'},
    ]
    errors, warnings = validate_package(files, 'federal')
    assert len(errors) == 0
    assert len(warnings) == 0

def test_validate_regional_all_docs():
    """Региональная программа: 3 документа - успех"""
    files = [
        {'filename': 'договор.pdf', 'content': b'test', 'extension': '.pdf'},
        {'filename': 'счёт.pdf', 'content': b'test', 'extension': '.pdf'},
        {'filename': 'акт.pdf', 'content': b'test', 'extension': '.pdf'},
    ]
    errors, warnings = validate_package(files, 'regional')
    assert len(errors) == 0
    assert len(warnings) == 0

def test_validate_missing_documents():
    """Должен находить отсутствующие документы"""
    files = [
        {'filename': 'договор.pdf', 'content': b'test', 'extension': '.pdf'},
    ]
    errors, warnings = validate_package(files, 'federal')
    # Должно быть 3 ошибки: нет спецификации, счёта и акта
    assert len(errors) == 3
    assert all(e['level'] == 'error' for e in errors)

def test_validate_invalid_format():
    """Должен отклонять недопустимые форматы"""
    files = [
        {'filename': 'договор.exe', 'content': b'test', 'extension': '.exe'},
    ]
    errors, warnings = validate_package(files, 'federal')
    
    # Проверяем ошибку формата
    has_format_error = any('Недопустимый формат' in e['message'] for e in errors)
    assert has_format_error
    
    # Проверяем ошибки о недостающих документах
    has_missing_error = any('Отсутствует обязательный документ' in e['message'] for e in errors)
    assert has_missing_error

def test_validate_large_file():
    """Должен отклонять файлы больше 20 МБ"""
    files = [
        {'filename': 'договор.pdf', 'content': b'x' * (21 * 1024 * 1024), 'extension': '.pdf'},
    ]
    errors, warnings = validate_package(files, 'federal')
    
    # Проверяем ошибку размера
    has_size_error = any('превышает 20 МБ' in e['message'] for e in errors)
    assert has_size_error
    
    # Проверяем ошибки о недостающих документах
    has_missing_error = any('Отсутствует обязательный документ' in e['message'] for e in errors)
    assert has_missing_error