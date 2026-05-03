# Finance Tracker — Frontend

Фронтенд на Vue 3 + TypeScript с FSD-архитектурой.

## Технологии

- Vue 3 + TypeScript
- Vite
- Vue Router
- Tailwind CSS
- Feature-Sliced Design (FSD)

## Установка

```bash
npm install
```

## Запуск

```bash
npm run dev
```

Приложение доступно по адресу http://localhost:5173

## Сборка

```bash
npm run build
```

## Линтинг

```bash
npm run lint        # ESLint проверка
npm run lint:fix    # ESLint автоисправление
npm run format      # Prettier форматирование
npm run format:check
```

## Структура `src/`

```
shared/     ← HTTP-клиент, UI-примитивы (без бизнес-логики)
entities/   ← бизнес-сущности: api + ui (только props/slots) + lib
widgets/    ← виджеты страниц: fetch, состояние, компоновка
pages/      ← только компоновка виджетов, без логики
router/
App.vue
main.ts
```

Каждый слой может импортировать только из слоёв **ниже** себя.
