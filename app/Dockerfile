FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-flask

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]