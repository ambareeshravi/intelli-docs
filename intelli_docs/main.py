from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from intelli_docs.api.routes import qa
from intelli_docs.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="An intelligent document Q&A system using LLMs, RAG, and MCP",
    version="1.0.0"
)

# add CORS middleware
# this can be configured later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include differnt routers
app.include_router(
    qa.router,
    prefix=settings.API_V1_STR,
    tags=["qa"]
)

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Welcome to the Intelligent Document Q&A System",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    # run the app at localhost and port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000) 