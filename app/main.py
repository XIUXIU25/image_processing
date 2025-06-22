from fastapi import FastAPI
from app import auth
from app.routes import images

app = FastAPI()

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(images.router, prefix="/images", tags=["Images"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Image Processing API"}
