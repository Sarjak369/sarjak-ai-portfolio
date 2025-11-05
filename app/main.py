"""
Main application entry point.
Combines FastAPI (for future API endpoints) with Gradio interface.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import gradio as gr
from loguru import logger
from app.ui.gradio_app import create_gradio_interface
from app.config import settings
from fastapi.staticfiles import StaticFiles
from app.ui.gradio_app import create_gradio_interface, ASSETS_DIR

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered portfolio assistant with RAG"
)

# serve static assets (profile.png)
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

# Health check endpoint


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Root redirect to Gradio
@app.get("/")
async def root():
    """Redirect root to Gradio interface."""
    return RedirectResponse(url="/gradio")


# Create and mount Gradio interface
logger.info("Creating Gradio interface...")
demo = create_gradio_interface()

# Mount Gradio app
app = gr.mount_gradio_app(app, demo, path="/gradio")

logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} ready!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=7860,
        reload=settings.DEBUG
    )
