import json
from typing import Any, List, Literal
from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # إعدادات المشروع العامة
    PROJECT_NAME: str = "AI Personal Trading Platform"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"

    # إعدادات قاعدة البيانات PostgreSQL & TimescaleDB
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def database_url(self) -> str:
        # رابط الاتصال غير المتزامن لقاعدة البيانات
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @computed_field
    @property
    def sync_database_url(self) -> str:
        # رابط الاتصال المتزامن لقاعدة البيانات (مطلوب لـ Alembic)
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # إعدادات Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @computed_field
    @property
    def redis_url(self) -> str:
        # رابط الاتصال بـ Redis
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # إعدادات RabbitMQ
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"

    # أسماء القنوات من البيئة
    QUEUE_MARKET_DATA: str = "market_data_queue"
    QUEUE_DECISIONS: str = "trading_decisions_queue"
    QUEUE_EXECUTION_LOGS: str = "execution_logs_queue"

    # إعدادات التداول الممررة من ملف البيئة
    TRADING_PAIRS: List[str]
    SUPPORTED_EXCHANGES: List[str]
    TIMEFRAMES: List[str]

    @field_validator(
        "TRADING_PAIRS", "SUPPORTED_EXCHANGES", "TIMEFRAMES", mode="before"
    )
    @classmethod
    def parse_json_list(cls, v: Any) -> List[str]:
        """
        يقوم بتحليل مصفوفة النصوص المدخلة بصيغة JSON من ملف البيئة وتحويلها لقائمة بايثون حقيقية.
        """
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                return [x.strip() for x in v.split(",") if x.strip()]
        return v

    # إعدادات إدارة المخاطر
    MAX_RISK_PER_TRADE_PERCENT: float = 1.5
    MAX_OPEN_TRADES: int = 5
    DEFAULT_LEVERAGE: int = 100

    # إعدادات MetaTrader 5
    MT5_LOGIN: int
    MT5_PASSWORD: str
    MT5_SERVER: str


settings = Settings()