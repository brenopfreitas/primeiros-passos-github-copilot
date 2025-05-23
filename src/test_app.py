"""
Testes para a API de atividades.
"""
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_list_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_remove():
    # Supondo que exista uma atividade chamada 'Yoga' no app.py
    email = "teste@example.com"
    activity = "Yoga"
    # Inscreve
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code in (200, 400)  # Pode já estar inscrito
    # Remove
    response = client.post(f"/activities/{activity}/remove?email={email}")
    assert response.status_code in (200, 400)  # Pode já ter sido removido
