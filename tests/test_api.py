from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/healthz').json()['ok'] is True
def test_run_risk(): assert client.post('/api/run/REQ-08').json()['decision']=='FLAG_RISK'
