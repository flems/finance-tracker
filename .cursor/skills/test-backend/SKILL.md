---
name: test-backend
description: >-
  Запускает тесты бэкенда и исправляет упавшие. Применять когда пользователь
  просит проверить эндпоинты, запустить тесты или убедиться что API не сломано.
---

# Скилл: тестирование бэкенда

## Когда использовать

- После добавления или изменения эндпоинтов на бэке
- Когда нужно убедиться что существующие ручки не сломаны
- По явной просьбе пользователя ("запусти тесты", "проверь апи")

## Структура тестов

```
backend/
  tests/
    conftest.py                    ← TestClient + тестовая Postgres БД (sport_tracker_test)
    test_budget.py                 ← тесты /budget/categories/*
    test_budget_distribution.py    ← тесты /budget/distribution, /budget/incomes/*, /budget/items/*
```

**Тестовая БД:** `postgresql://sport_user:sport_password@db:5432/sport_tracker_test`
Создаётся и очищается автоматически через `autouse` фикстуру в `conftest.py`.

## Запуск

```bash
docker compose exec backend python -m pytest tests/ -v
```

Для конкретного файла:
```bash
docker compose exec backend python -m pytest tests/test_budget.py -v
docker compose exec backend python -m pytest tests/test_budget_distribution.py -v
```

## Алгоритм работы

1. Запусти тесты командой выше
2. Если все **PASSED** — готово, сообщи пользователю
3. Если есть **FAILED** или **ERROR**:
   - Прочитай traceback упавшего теста
   - Определи причину: изменился контракт API, сломана логика, или тест устарел
   - Исправь код бэкенда (приоритет) или обнови тест если контракт намеренно изменился
   - Запусти снова, повтори до зелёного

## Когда добавлять новые тесты

При добавлении нового эндпоинта — добавить тесты в соответствующий файл `tests/test_<router>.py`.

Обязательные сценарии для каждого эндпоинта:
- **happy path** — корректный запрос возвращает ожидаемый статус и тело
- **not found** — несуществующий id → `404` + `code: NOT_FOUND`
- **валидация** — дубликат уникального поля → `409` + нужный `code`
- **граничные значения** — null-поля, пустые строки если применимо

## Формат ошибок (из api-contracts.mdc)

Все ошибки возвращают:
```json
{ "status": "error", "code": "КОД", "message": "текст" }
```
Тест должен проверять и `status_code`, и `body["code"]`.
