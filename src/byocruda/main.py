from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BYOCRUDA",
    description="Build Your Own CRUD Application",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint returning basic API information."""
    return {
        "message": "Welcome to BYOCRUDA API",
        "version": "0.1.0",
        "status": "operational"
    }
