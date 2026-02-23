FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py .
COPY genome_agent_mapper.py .
COPY msl_ledger.py .
COPY hormonal_orchestrator.py .
COPY eve_protocol.py .
COPY main.py .

EXPOSE 8888

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
