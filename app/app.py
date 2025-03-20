
from flask import Flask, request, jsonify
from models import db, Aluno
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([aluno.to_dict() for aluno in alunos])

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.json
    novo_aluno = Aluno(**dados)
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify(novo_aluno.to_dict()), 201

@app.route('/alunos/<aluno_id>', methods=['PUT'])
def alterar_aluno(aluno_id):
    dados = request.json
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    for key, value in dados.items():
        setattr(aluno, key, value)
    db.session.commit()
    return jsonify(aluno.to_dict())

@app.route('/alunos/<aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404
    db.session.delete(aluno)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
