# Image Processing API

A simple FastAPI backend that allows user authentication and image uploads.

## Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `POST /images`
```