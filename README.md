# TravelPlan API

REST API do planowania podróży - zarządzanie wyjazdami, taskami na każdy dzień i pogodą dla destynacji. 

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- Redis
- Docker
- pytest
- GitHub Actions CI

## Uruchomienie lokalne

1. Sklonuj repo
```bash
git clone https://github.com/maciek435/travelplan.git
cd travelplan
```

2. Stwóz plik `.env` na podstawie zmiennych:
POSTGRES_USER=travelplan
POSTGRES_PASSWORD=travelplan
POSTGRES_DB=travelplan
DATABASE_URL=postgresql+asyncpg://travelplan:travelplan@localhost:5432/travelplan
SECRET_KEY=twoj_sekretny_klucz
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENWEATHER_API_KEY=twoj_klucz

3. Uruchom bazę danych i Redis
```bash
docker compose up -d
```

4. Zastosuj migracje
```bash
alembic upgrade head
```

5. Uruchom aplikację
```bash
uvicorn app.main:app --reload
```

6. Otwórz dokumentację API: http://localhost:8000/docs

## Endpoints

### Auth
- `POST /auth/register` — rejestracja
- `POST /auth/login` — logowanie, zwraca JWT token
- `GET /auth/me` — dane zalogowanego użytkownika

### Trips
- `GET /trips/` — lista podróży
- `POST /trips/` — nowa podróż
- `GET /trips/{id}` — szczegóły podróży
- `PUT /trips/{id}` — edycja podróży
- `DELETE /trips/{id}` — usunięcie podróży
- `GET /trips/{id}/weather` — pogoda dla destynacji

### Day Tasks
- `GET /day-tasks/{trip_id}` — taski dla podróży
- `POST /day-tasks/` — nowy task
- `PUT /day-tasks/{id}` — edycja taska
- `DELETE /day-tasks/{id}` — usunięcie taska

## CI badge
[![CI](https://github.com/maciek435/travelplan/actions/workflows/ci.yml/badge.svg)](https://github.com/maciek435/travelplan/actions/workflows/ci.yml)