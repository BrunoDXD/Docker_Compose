import pytest
from models import db, Turma
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/escola'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_listar_turmas(client):
    response = client.get('/turmas')
    assert response.status_code == 200
    assert len(response.json) > 0  # Verifica se há pelo menos uma turma no banco de dados

def test_cadastrar_turma(client):
    nova_turma = {'nome_turma': 'Turma 3', 'id_professor': 1, 'horario': '09:00 - 13:00'}
    response = client.post('/turmas', json=nova_turma)
    assert response.status_code == 201
    assert response.json['nome_turma'] == 'Turma 3'
    assert response.json['horario'] == '09:00 - 13:00'

def test_alterar_turma(client):
    dados_alterados = {'nome_turma': 'Turma 1 Alterada', 'id_professor': 1, 'horario': '10:00 - 14:00'}
    response = client.put('/turmas/1', json=dados_alterados)
    assert response.status_code == 200
    assert response.json['nome_turma'] == 'Turma 1 Alterada'
    assert response.json['horario'] == '10:00 - 14:00'

def test_excluir_turma(client):
    response = client.delete('/turmas/1')
    assert response.status_code == 204
    response = client.get('/turmas')
    assert not any(turma['id_turma'] == 1 for turma in response.json)