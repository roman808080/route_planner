FROM python:3.9-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ .
CMD [ \
    "gunicorn", "main:app",\
    "--workers", "4", "--worker-class",\
    "uvicorn.workers.UvicornWorker",\
    "--bind", "0.0.0.0:8000"\
]
