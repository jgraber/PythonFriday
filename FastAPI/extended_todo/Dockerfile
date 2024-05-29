FROM python:3.12-slim

WORKDIR /app/todo

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

WORKDIR /app/

CMD ["uvicorn", "todo.main:app", "--host", "0.0.0.0", "--port", "8000"]