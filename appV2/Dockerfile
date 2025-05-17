FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

EXPOSE 8001

CMD ["flask", "run", "--host=0.0.0.0", "--port=8001"] 