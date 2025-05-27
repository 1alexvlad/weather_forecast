FROM python:3.13-alpine

RUN apk add --no-cache postgresql-client build-base postgresql-dev gettext

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]