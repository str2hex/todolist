FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
WORKDIR web/www
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]