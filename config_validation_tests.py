from app.core.config import settings


def test_settings_successfully_loaded() -> None:
    """
    التحقق من صحة تحميل متغيرات البيئة وعدم وجود قيم صلبة بداخل الكود.
    """
    assert settings.PROJECT_NAME == "AI Personal Trading Platform"
    assert isinstance(settings.TRADING_PAIRS, list)
    assert "EURUSD" in settings.TRADING_PAIRS
    assert "MT5" in settings.SUPPORTED_EXCHANGES
    assert settings.ENVIRONMENT == "testing"


def test_database_connection_strings() -> None:
    """
    التحقق من سلامة وصلاحية صياغة روابط الاتصال بقاعدة البيانات.
    """
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.sync_database_url.startswith("postgresql://")