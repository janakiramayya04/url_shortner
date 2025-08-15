FROM python:3.13-slim-bullseye AS builder
WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim-bullseye
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser
WORKDIR /usr/src/app
COPY --chown=appuser:appuser . .
COPY --from=builder /opt/venv /opt/venv
USER appuser
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]