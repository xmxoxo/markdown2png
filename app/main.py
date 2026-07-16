from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.api.routes import router
from app.core.config import settings
import os

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

output_dir_name = os.path.basename(os.path.normpath(settings.OUTPUT_DIR))
app.mount(f"/{output_dir_name}", StaticFiles(directory=settings.OUTPUT_DIR), name="output")
# app.mount("/template", StaticFiles(directory=settings.TEMPLATE_DIR), name="template")

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} API Service", "version": settings.APP_VERSION}