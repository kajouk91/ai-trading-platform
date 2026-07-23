import structlog
from app.core.logging import configure_logging


def test_logging_configuration_completes() -> None:
    """
    التحقق من عمل تهيئة نظام السجلات بدون التسبب بأي أخطاء أثناء التشغيل.
    """
    configure_logging()
    test_logger = structlog.get_logger()
    assert test_logger is not None