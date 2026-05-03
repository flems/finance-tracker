---
name: fsd-review
description: Проверяет фронтенд на соответствие FSD-структуре и исправляет нарушения. Применять когда пользователь просит проверить код на FSD, провести ревью структуры или исправить нарушения FSD.
---

# FSD Review

## Алгоритм

### Шаг 1 — Прочитать правило
Прочитай `.cursor/rules/fsd-structure.mdc` — это единственный источник истины по слоям.

### Шаг 2 — Просканировать цель
Если пользователь указал конкретную страницу: просмотри `pages/<page>/`, `widgets/<page>-page/` и связанные `entities/`.
Если не указал — просмотри всё дерево `frontend/src/`.

### Шаг 3 — Найти нарушения

Проверь каждый файл по чеклисту:

- [ ] Тип бизнес-сущности и fetch-функции находятся в `entities/<entity>/api/`, а не в `widgets/` или корне
- [ ] UI-компонент отображения (таблица, карточка, список) находится в `entities/<entity>/ui/`, принимает только `props`
- [ ] UI-компонент мутации (форма, кнопка действия) находится в `widgets/<name>-page/components/<action>/ui/`
- [ ] Виджет страницы лежит в `widgets/<name>-page/` (kebab-case + суффикс `-page`)
- [ ] Виджет не рисует таблицы/формы сам — делегирует в `entities`
- [ ] `pages/<page>/` содержит только компоновку виджета, без логики и API-вызовов
- [ ] Нет запрещённых импортов (наприме�� `entities` → `widgets`)

### Шаг 4 — Отчёт о нарушениях

Перед исправлением показать список:
```
❌ widgets/budget-page/index.vue содержит интерфейс BudgetCategory → переместить в entities/budget-category/api/
❌ widgets/budget-page/index.vue рисует таблицу напрямую → вынести в entities/budget-category/ui/BudgetCategoryTable.vue
```

### Шаг 5 — Исправить

Для каждого нарушения:
1. Создать файл в правильном месте
2. Обновить все импорты во всех затронутых файлах
3. Удалить старый файл если он полностью перемещён

### Шаг 6 — Итоговый отчёт

```
✅ Исправлено:
- entities/budget-category/api/budgetCategoryApi.ts  (перемещено из widgets/budget-page/index.vue)
- entities/budget-category/ui/BudgetCategoryTable.vue (выделено из widgets/budget-page/index.vue)
- widgets/budget-page/index.vue  (теперь только оркестрация)

Структура соответствует FSD.
```
