import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from models import db, Turma
from config import Config

# Configuração do logging com rotação de logs
handler = RotatingFileHandler('escola_infantil.log', maxBytes=2000, backupCount=5)
logging.basicConfig(
    handlers=[handler],
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/turmas', methods=['GET'])
def listar_turmas():
    try:
        turmas = Turma.query.all()
        logger.info('READ: Listagem de todas as turmas solicitada.')
        return jsonify([turma.to_dict() for turma in turmas])
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar turmas - {e}')
        return jsonify({'error': 'Falha ao listar turmas'}), 500

@app.route('/turmas', methods=['POST'])
def cadastrar_turma():
    try:
        dados = request.json
        nova_turma = Turma(**dados)
        db.session.add(nova_turma)
        db.session.commit()
        logger.info(f'CREATE: Turma {nova_turma.to_dict()} inserida com sucesso.')
        return jsonify(nova_turma.to_dict()), 201
    except Exception as e:
        logger.error(f'ERROR: Falha ao cadastrar turma - {e}')
        return jsonify({'error': 'Falha ao cadastrar turma'}), 500

@app.route('/turmas/<turma_id>', methods=['PUT'])
def alterar_turma(turma_id):
    try:
        dados = request.json
        turma = Turma.query.get(turma_id)
        if not turma:
            logger.warning(f'UPDATE: Turma com ID {turma_id} não encontrada.')
            return jsonify({'error': 'Turma não encontrada'}), 404
        for key, value in dados.items():
            setattr(turma, key, value)
        db.session.commit()
        logger.info(f'UPDATE: Turma com ID {turma_id} atualizada para {turma.to_dict()}.')
        return jsonify(turma.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao alterar turma com ID {turma_id} - {e}')
        return jsonify({'error': 'Falha ao alterar turma'}), 500

@app.route('/turmas/<turma_id>', methods=['DELETE'])
def excluir_turma(turma_id):
    try:
        turma = Turma.query.get(turma_id)
        if not turma:
            logger.warning(f'DELETE: Turma com ID {turma_id} não encontrada.')
            return jsonify({'error': 'Turma não encontrada'}), 404
        db.session.delete(turma)
        db.session.commit()
        logger.info(f'DELETE: Turma com ID {turma_id} removida com sucesso.')
        return '', 204
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir turma com ID {turma_id} - {e}')
        return jsonify({'error': 'Falha ao excluir turma'}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
