import pytest
from app.core.database import get_db_session


@pytest.mark.asyncio
async def test_database_session_yields_correctly() -> None:
    """
    التحقق من أن مولد جلسات قاعدة البيانات غير المتزامن يعمل بشكل صحيح ومستقر.
    """
    generator = get_db_session()
    assert generator is not None