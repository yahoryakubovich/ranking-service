# Project Setup and Development

## 1. Installing `uv`

To install `uv`, you can use pip. Run the following command in your terminal:

```bash
pip install uv
```

## 2. Creating and Activating a Virtual Environment with uv

### Creating the Virtual Environment

```bash
uv venv .venv --seed
```

### Activating the Virtual Environment

**Windows (cmd / PowerShell):**

```bash
.\.venv\Scripts\activate
```

**macOS / Linux (bash, zsh):**

```bash
source .venv/bin/activate
```

### Installing Project Dependencies

```bash
uv sync
```

---

## 🚀 Running the Application

### Local Development

For local development, ensure your `.env` file is configured as follows:

```ini
REDIS_HOST=127.0.0.1
```

To ensure correct module imports (using `app` instead of `src.app`), run the server from the `src` directory:

```bash
cd src
```

On Windows (cmd / PowerShell):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

On macOS / Linux (bash, zsh):
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "0.0.0.0:8000"
```

### Docker Deployment

For running via Docker, ensure your `.env` file is configured as follows:

```ini
REDIS_HOST=redis
```

Use the following commands:

```bash
make docker-build
```

```bash
make up
```

---

## 📊 Scores Computing & Redis Population

After starting the Redis container or local instance, run these commands via terminal to prepare the environment

### Compute Scores

Calculates ranking scores:

```bash
make compute-scores
```

### Populate Redis

Populate Redis with the required data:

```bash
make populate-redis
```