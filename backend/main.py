from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Text Summarization API",
    description="API for text summarization using AI models",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routes
from app.api.routes.summarization import router as summarization_router
from app.api.routes.feedback import router as feedback_router
from app.api.routes.documents import router as documents_router

app.include_router(summarization_router, prefix="/api/summarization", tags=["Summarization"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Text Summarization API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
