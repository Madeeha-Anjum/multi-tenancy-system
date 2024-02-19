# DBT Server

## Development Setup

### 1. Venv

```bash
    python3 -m venv .venv # create venv
    source .venv/Scripts/activate # activate venv
    pip install -r requirements.txt # install requirements
```

### 2. Run dev server

```bash
    uvicorn main:app  --reload
```

## Alembic Starting

1. `alembic stamp head` # pull the latest migration from the database
2. run all migrations on al tenants `alembic upgrade head`
