## FatSecret сервис (питание)

- **Как поднять бэкенд (API + БД)**
  - Из корня проекта:

```bash
docker-compose up --build
```

- **Где лежат креды FatSecret**
  - В `docker-compose.yml` в сервисе `backend` в блоке `environment`:
    - `OAUTH_CONSUMER_KEY`
    - `OAUTH_CONSUMER_SECRET`
    - `ACCESS_TOKEN`
    - `ACCESS_TOKEN_SECRET`

- **Как запустить разово**
  - Из корня проекта (за сегодня по UTC):

```bash
docker-compose run --rm backend python -m app.services.fatsecret.sync_food
```

- **Как запустить за конкретную дату**

```bash
docker-compose run --rm backend python -m app.services.fatsecret.sync_food YYYY-MM-DD
```

Дата передаётся последним аргументом в формате `2026-03-12`. Если дату не указывать, берётся текущий день (UTC). 


