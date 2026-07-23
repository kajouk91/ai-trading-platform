from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings
from app.core.logging import logger

# إنشاء محرك الاتصال غير المتزامن لقاعدة البيانات
async_engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    echo=False,
)

# مصنع الجلسات غير المتزامنة لضمان استقرار العمليات
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    تابع لتوفير جلسة تواصل غير متزامنة مع قاعدة البيانات (Dependency Injection لـ FastAPI).
    يضمن تنفيذ المعاملات (Commit) تلقائياً، أو التراجع عنها (Rollback) في حالة حدوث أخطاء.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            await logger.aerror(
                "تم التراجع عن المعاملة بسبب خطأ في قاعدة البيانات", error=str(e)
            )
            raise
        finally:
            await session.close()