from flask import Flask, request, jsonify
from models import db, Turma
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/turmas', methods=['GET'])
def listar_turmas():
    turmas = Turma.query.all()
    return jsonify([turma.to_dict() for turma in turmas])

@app.route('/turmas', methods=['POST'])
def cadastrar_turma():
    dados = request.json
    nova_turma = Turma(**dados)
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify(nova_turma.to_dict()), 201

@app.route('/turmas/<turma_id>', methods=['PUT'])
def alterar_turma(turma_id):
    dados = request.json
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    for key, value in dados.items():
        setattr(turma, key, value)
    db.session.commit()
    return jsonify(turma.to_dict())

@app.route('/turmas/<turma_id>', methods=['DELETE'])
def excluir_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    db.session.delete(turma)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)