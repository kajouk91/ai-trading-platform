import logging
import sys
import structlog
from app.core.config import settings


def configure_logging() -> None:
    """
    تهيئة وإعداد مكتبة structlog لتقديم سجلات (Logs) احترافية بصيغة JSON في بيئة الإنتاج،
    وبصيغة نصية ملونة سهلة القراءة في بيئة التطوير المحلية.
    """
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.ENVIRONMENT == "production":
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )

    # إعادة توجيه السجلات القياسية لبايثون لتوحيد المخرجات
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )


logger = structlog.get_logger()