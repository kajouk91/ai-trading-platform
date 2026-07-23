import asyncio
from typing import Generator
import pytest
from app.core.config import settings

# ضبط بيئة العمل كبيئة اختبارات تلقائياً لمنع تلويث قاعدة البيانات الفعلية
settings.ENVIRONMENT = "testing"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    توفير حلقة أحداث (Event Loop) نظيفة لكل جلسة اختبار لتشغيل المهام غير المتزامنة.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()