FROM python:3.12-slim

# create non-root user
RUN useradd --create-home appuser
WORKDIR /app

# system deps (minimal)
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

COPY app/ /app/

RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=5000
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=2"]