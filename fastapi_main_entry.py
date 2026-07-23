from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import configure_logging, logger

# تهيئة الإعدادات العامة للـ Logging بمجرد استيراد الملف
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    إدارة دورة حياة التطبيق (Lifespan) لتهيئة الموارد عند التشغيل وتحريرها عند الإيقاف بشكل غير متزامن.
    """
    await logger.ainfo("بدء تشغيل منصة التداول الشخصية بالذكاء الاصطناعي...")
    yield
    await logger.ainfo("إيقاف منصة التداول الشخصية بالذكاء الاصطناعي...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """
    نقطة فحص الصحة العامة للتطبيق للتحقق من استقرار الخادم.
    """
    return {"status": "healthy", "project": settings.PROJECT_NAME}