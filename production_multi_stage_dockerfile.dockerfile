# --- المرحلة الأولى: بناء التبعيات واستخلاص العجلات البرمجية ---
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# تجهيز البيئة الافتراضية وتثبيت الحزم
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- المرحلة الثانية: بيئة التشغيل النهائية الخفيفة والمحمية ---
FROM python:3.12-slim AS runner

WORKDIR /app

# تثبيت متطلبات التشغيل الأساسية فقط لتقليل حجم الحاوية وثغراتها
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# نسخ البيئة الافتراضية بالكامل من مرحلة البناء
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# إنشاء مستخدم ومجموعة بصلاحيات محدودة (Non-root user)
RUN groupadd -r trading && useradd -r -g trading trading

# نسخ كود التطبيق مع إعطاء الصلاحيات للمستخدم الجديد
COPY --chown=trading:trading app/ /app/app/
COPY --chown=trading:trading pyproject.toml /app/

EXPOSE 8000

USER trading

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]