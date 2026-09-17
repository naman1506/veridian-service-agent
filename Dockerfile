FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python -m eval.run_eval && python -c 'from app.orchestrator import Orchestrator; Orchestrator().run_all()' && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
