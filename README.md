# Finance Tracker

Fullstack-приложение для учёта бюджета и накоплений.

## Стек

- **Backend:** FastAPI, SQLAlchemy 2, PostgreSQL, pytest
- **Frontend:** Vue 3, TypeScript, Vite, Tailwind CSS, FSD-архитектура

## Запуск

```bash
docker compose up --build
```

- API: http://localhost:8000
- Frontend: http://localhost:5173 (dev: `cd frontend && npm run dev`)
- Документация API: http://localhost:8000/docs

## Тесты

```bash
docker compose exec backend python -m pytest tests/ -v
```

Тестовая БД `finance_tracker_test` создаётся автоматически через init-скрипт `docker/postgres/init/`.

## Линтинг

**Frontend:**
```bash
cd frontend && npm run lint       # проверка
cd frontend && npm run lint:fix   # автоисправление
cd frontend && npm run format     # prettier
```

**Backend:**
```bash
cd backend && ruff check .        # проверка
cd backend && ruff check . --fix  # автоисправление
cd backend && ruff format .       # форматирование
```

## Структура проекта

```
backend/
  app/
    api/        ← роутеры FastAPI
    models.py   ← SQLAlchemy модели
    schemas.py  ← Pydantic схемы
    db.py       ← подключение к БД
    main.py     ← точка входа

frontend/src/   ← FSD-архитектура
  shared/       ← переиспользуемая инфраструктура
  entities/     ← бизнес-сущности
  widgets/      ← виджеты страниц
  pages/        ← компоновка страниц
```
