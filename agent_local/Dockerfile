FROM python:3.12-slim
WORKDIR /app
COPY agent_local/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY agent_local /app/agent_local
COPY web /app/web
COPY config /app/config
EXPOSE 8000
CMD ["uvicorn", "agent_local.main:app", "--host", "0.0.0.0", "--port", "8000"]
