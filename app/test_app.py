import pytest
from models import db, Aluno
from app import app
from test_data import test_alunos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/escola'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            for aluno in test_alunos:
                db.session.add(Aluno(**aluno))
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.mark.parametrize("aluno_id, expected_nome", [(aluno['aluno_id'], aluno['nome']) for aluno in test_alunos])
def test_listar_alunos(client, aluno_id, expected_nome):
    response = client.get('/alunos')
    assert response.status_code == 200
    assert any(aluno['aluno_id'] == aluno_id and aluno['nome'] == expected_nome for aluno in response.json)

def test_cadastrar_aluno(client):
    novo_aluno = {'aluno_id': 'A011', 'nome': 'João', 'endereco': 'Rua K, 2425', 'cidade': 'Campinas', 'estado': 'SP', 'cep': '11000-000', 'pais': 'Brasil', 'telefone': '1212-1212'}
    response = client.post('/alunos', json=novo_aluno)
    assert response.status_code == 201
    assert response.json['nome'] == 'João'
    assert response.json['endereco'] == 'Rua K, 2425'

@pytest.mark.parametrize("aluno_id, dados_alterados", [('A001', {'nome': 'João Silva Alterado'})])
def test_alterar_aluno(client, aluno_id, dados_alterados):
    response = client.put(f'/alunos/{aluno_id}', json=dados_alterados)
    assert response.status_code == 200
    assert response.json['nome'] == dados_alterados['nome']

@pytest.mark.parametrize("aluno_id", ['A001'])
def test_excluir_aluno(client, aluno_id):
    response = client.delete(f'/alunos/{aluno_id}')
    assert response.status_code == 204
    response = client.get('/alunos')
    assert not any(aluno['aluno_id'] == aluno_id for aluno in response.json)