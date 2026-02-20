FROM python:3.10-slim
WORKDIR /app
# النسخ من السياق الحالي (اللي هو داخل المجلد)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
