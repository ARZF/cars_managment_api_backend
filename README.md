## Cars Management API (FastAPI)

A simple **cars management REST API** built with **FastAPI** and **SQLAlchemy**.  
It supports:

- **User authentication** with JWT (login/register)
- **Role-based access control** (`user`, `admin`)
- **Cars management** (register, update, delete, search by plate number)
- **Approval / rejection counts** for cars
- A **scheduled cleanup task** that periodically deletes cars with too many rejections

---

## Tech Stack

- **Python** 3.11+
- **FastAPI** (`fastapi`, `uvicorn`)
- **SQLAlchemy** (ORM)
- **SQLite** (local development DB)
- **Passlib** + **bcrypt** (password hashing)
- **python-jose** (JWT tokens)

---

## Getting Started

### 1. Clone and enter the project

```bash
git clone <your-repo-url> cars_managment_api_backend
cd cars_managment_api_backend
```

### 2. Create & activate virtualenv

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux / macOS
```

### 3. Install dependencies

```bash
pip install -U pip
pip install -r requirement.txt
```

Or, if you use `uv`:

```bash
uv pip install -r requirements.txt
```

### 4. Environment variables

The app loads settings from `.env` via `core/config.py`:

- `SECRET_KEY` – secret used to sign JWTs (required)
- `ALGORITHM` – JWT algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` – token lifetime in minutes (default: `30`)

Example `.env`:

```env
SECRET_KEY=super-secret-key-change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the API

From the project root:

```bash
uvicorn main:app --reload
```

The API will be available at:

- Swagger docs: `http://127.0.0.1:8000/docs`
- ReDoc docs: `http://127.0.0.1:8000/redoc`

---

## Running with Docker

### Build and run using Docker directly

```bash
docker build -t cars-management-api .
docker run --env-file .env -p 8000:8000 cars-management-api
```

### Or use Docker Compose

```bash
docker compose up --build
```

This will:

- Build the image from the `Dockerfile`
- Start the app service from `docker-compose.yml`
- Expose the API at `http://localhost:8000`
- Load environment variables from `.env`
- Mount `database.db` so your SQLite data persists between container restarts

---

## Database

Configuration is in `database.py`:

- Uses SQLite: `sqlite:///./database.db`
- Base class: `Base = declarative_base()`
- Session factory: `SessionLocal`

### Models (in `Models.py`)

- `User`
  - `id`, `email`, `hashed_password`, `role`
  - `created_at`, `updated_at`
- `Car`
  - `id`, `plate_number`, `brand`, `model`, `year`
  - `rejection_report`, `rejection_count`, `approved_count`
- `Report`
  - `id`, `reason`
  - `car_id` → `cars.id`
  - `user_id` → `users.id`

`main.py` calls `Base.metadata.create_all(bind=engine)` on startup to create tables automatically (suitable for development).

---

## Authentication & Authorization

### Auth helpers (`auth.py`)

- `hash_password(password: str) -> str`
- `verify_password(plain_password, hashed_password) -> bool`
- `create_access_token(user_id: int, role: str) -> str`
- `decode_token(token: str) -> dict`

### Dependencies (`depends.py`)

- `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")`
- `get_current_user` – decodes JWT and loads `User` from DB
- `require_role(required_role: str)` – dependency factory enforcing a specific user role

### Auth routes (`routers/auth.py`)

- `POST /auth/register`
  - Body: `RegisterRequest { email, password, role }`
  - Only admins can create users (uses `require_role("admin")`)
  - Validates role against `ALLOWED_ROLES = {"user", "admin"}`
- `POST /auth/login`
  - Body: `LoginRequest { email, password }`
  - Returns `{ access_token, token_type }` (JWT)
- `POST /auth/logout`
  - Simple success message (no token blacklist)

---

## Cars API

### Schemas (`schemas.py`)

- `CarRequest` – `plate_number`, `brand`, `model`, `year`
- `CarResponse` – `id`, `plate_number`, `brand`, `model`, `year`, `rejection_report`, `rejection_count`, `approved_count`
- `RejectCarRequest` – `rejection_report: str`

### Routes (`routers/cars.py`)

Prefix: `/cars`

- `GET /cars/search/{plate_number}`  
  - Auth required (`get_current_user`)  
  - Returns `CarResponse` or 404.

- `POST /cars/{car_id}/approve`  
  - Auth required (`get_current_user`)  
  - Increments `approved_count` and returns updated `CarResponse`.

- `POST /cars/{car_id}/reject`  
  - Auth & admin required (`require_role("admin")`)  
  - Accepts `RejectCarRequest` with a rejection report.  
  - (Extend this to update `rejection_report` and `rejection_count`.)

- `POST /cars/register`  
  - Admin only  
  - Creates a new car from `CarRequest`.

- `PUT /cars/{car_id}`  
  - Admin only  
  - Updates car data.

- `DELETE /cars/{car_id}`  
  - Admin only  
  - Deletes a car.

---

## Users API

### Routes (`routers/users.py`)

Prefix: `/users`

- `GET /users/dashboard`  
  - Any authenticated user.  
  - Returns a welcome message containing the user’s email.

- `GET /users/admin`  
  - Admin only (`require_role("admin")`).  
  - Returns a simple “Admin access granted” message.

---

## Scheduled Cleanup Task

In `main.py` the app uses `fastapi-utils` to run a periodic background task:

```python
@app.on_event("startup")
@repeat_every(seconds=3600)
def delete_rejected_cars_task() -> None:
    db = SessionLocal()
    try:
        db.query(Car).filter(Car.rejection_count >= 3).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()
```

This **runs every hour** and deletes all cars whose `rejection_count` is 3 or more.

---

## Development Tips

- To start with a fresh DB during development, you can delete `database.db`; the tables will be recreated on the next run.
- Use the interactive docs at `/docs` to:
  - Register an admin user.
  - Login and copy the JWT.
  - Authorize in the Swagger UI (top right “Authorize” button) to test protected endpoints.

---

## License

You can add your preferred license information here (e.g. MIT).

