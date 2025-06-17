import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from models import db, Turma, Professor, Aluno, Pagamento, Presenca, Atividade, AtividadeAluno, Usuario
from config import Config
from datetime import datetime

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

# Inicialização do banco de dados com tratamento de erro
try:
    with app.app_context():
        db.create_all()
        logger.info("Tabelas do banco de dados criadas com sucesso")
except Exception as e:
    logger.error(f"Erro ao criar tabelas do banco de dados: {e}")

# Rota raiz
@app.route('/')
def index():
    return jsonify({
        "message": "API da Escola Infantil",
        "endpoints": {
            "professores": "/professores",
            "turmas": "/turmas",
            "alunos": "/alunos",
            "pagamentos": "/pagamentos",
            "presencas": "/presencas",
            "atividades": "/atividades"
        }
    })

# Rotas para Professores
@app.route('/professores', methods=['GET'])
def listar_professores():
    try:
        professores = Professor.query.all()
        logger.info('READ: Listagem de todos os professores solicitada.')
        return jsonify([professor.to_dict() for professor in professores])
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar professores - {e}')
        return jsonify({'error': 'Falha ao listar professores'}), 500

@app.route('/professores/<professor_id>', methods=['GET'])
def obter_professor(professor_id):
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            logger.warning(f'READ: Professor com ID {professor_id} não encontrado.')
            return jsonify({'error': 'Professor não encontrado'}), 404
        logger.info(f'READ: Professor com ID {professor_id} encontrado.')
        return jsonify(professor.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao obter professor com ID {professor_id} - {e}')
        return jsonify({'error': 'Falha ao obter professor'}), 500

@app.route('/professores', methods=['POST'])
def cadastrar_professor():
    try:
        dados = request.json
        professor = Professor(
            nome_completo=dados['nome_completo'],
            email=dados['email'],
            telefone=dados['telefone']
        )
        db.session.add(professor)
        db.session.commit()
        logger.info(f'CREATE: Professor {professor.nome_completo} inserido com sucesso.')
        return jsonify(professor.to_dict()), 201
    except Exception as e:
        logger.error(f'ERROR: Falha ao cadastrar professor - {e}')
        return jsonify({'error': 'Falha ao cadastrar professor'}), 500

@app.route('/professores/<professor_id>', methods=['PUT'])
def atualizar_professor(professor_id):
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            logger.warning(f'UPDATE: Professor com ID {professor_id} não encontrado.')
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        dados = request.json
        if 'nome_completo' in dados:
            professor.nome_completo = dados['nome_completo']
        if 'email' in dados:
            professor.email = dados['email']
        if 'telefone' in dados:
            professor.telefone = dados['telefone']
        
        db.session.commit()
        logger.info(f'UPDATE: Professor com ID {professor_id} atualizado com sucesso.')
        return jsonify(professor.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao atualizar professor com ID {professor_id} - {e}')
        return jsonify({'error': 'Falha ao atualizar professor'}), 500

@app.route('/professores/<professor_id>', methods=['DELETE'])
def excluir_professor(professor_id):
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            logger.warning(f'DELETE: Professor com ID {professor_id} não encontrado.')
            return jsonify({'error': 'Professor não encontrado'}), 404
        
        db.session.delete(professor)
        db.session.commit()
        logger.info(f'DELETE: Professor com ID {professor_id} removido com sucesso.')
        return '', 204
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir professor com ID {professor_id} - {e}')
        return jsonify({'error': 'Falha ao excluir professor'}), 500

# Rotas para Turmas
@app.route('/turmas', methods=['GET'])
def listar_turmas():
    try:
        turmas = Turma.query.all()
        logger.info('READ: Listagem de todas as turmas solicitada.')
        return jsonify([turma.to_dict() for turma in turmas])
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar turmas - {e}')
        return jsonify({'error': 'Falha ao listar turmas'}), 500

@app.route('/turmas/<turma_id>', methods=['GET'])
def obter_turma(turma_id):
    try:
        turma = Turma.query.get(turma_id)
        if not turma:
            logger.warning(f'READ: Turma com ID {turma_id} não encontrada.')
            return jsonify({'error': 'Turma não encontrada'}), 404
        logger.info(f'READ: Turma com ID {turma_id} encontrada.')
        return jsonify(turma.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao obter turma com ID {turma_id} - {e}')
        return jsonify({'error': 'Falha ao obter turma'}), 500

@app.route('/turmas', methods=['POST'])
def cadastrar_turma():
    try:
        dados = request.json
        turma = Turma(
            nome_turma=dados['nome_turma'],
            id_professor=dados['id_professor'],
            horario=dados['horario']
        )
        db.session.add(turma)
        db.session.commit()
        logger.info(f'CREATE: Turma {turma.nome_turma} inserida com sucesso.')
        return jsonify(turma.to_dict()), 201
    except Exception as e:
        logger.error(f'ERROR: Falha ao cadastrar turma - {e}')
        return jsonify({'error': 'Falha ao cadastrar turma'}), 500

@app.route('/turmas/<turma_id>', methods=['PUT'])
def atualizar_turma(turma_id):
    try:
        turma = Turma.query.get(turma_id)
        if not turma:
            logger.warning(f'UPDATE: Turma com ID {turma_id} não encontrada.')
            return jsonify({'error': 'Turma não encontrada'}), 404
        
        dados = request.json
        if 'nome_turma' in dados:
            turma.nome_turma = dados['nome_turma']
        if 'id_professor' in dados:
            turma.id_professor = dados['id_professor']
        if 'horario' in dados:
            turma.horario = dados['horario']
        
        db.session.commit()
        logger.info(f'UPDATE: Turma com ID {turma_id} atualizada com sucesso.')
        return jsonify(turma.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao atualizar turma com ID {turma_id} - {e}')
        return jsonify({'error': 'Falha ao atualizar turma'}), 500

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

# Rotas para Alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    try:
        alunos = Aluno.query.all()
        logger.info('READ: Listagem de todos os alunos solicitada.')
        return jsonify([aluno.to_dict() for aluno in alunos])
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar alunos - {e}')
        return jsonify({'error': 'Falha ao listar alunos'}), 500

@app.route('/alunos/<aluno_id>', methods=['GET'])
def obter_aluno(aluno_id):
    try:
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            logger.warning(f'READ: Aluno com ID {aluno_id} não encontrado.')
            return jsonify({'error': 'Aluno não encontrado'}), 404
        logger.info(f'READ: Aluno com ID {aluno_id} encontrado.')
        return jsonify(aluno.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao obter aluno com ID {aluno_id} - {e}')
        return jsonify({'error': 'Falha ao obter aluno'}), 500

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    try:
        dados = request.json
        data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date() if 'data_nascimento' in dados else None
        
        aluno = Aluno(
            nome_completo=dados['nome_completo'],
            data_nascimento=data_nascimento,
            id_turma=dados['id_turma'],
            nome_responsavel=dados['nome_responsavel'],
            telefone_responsavel=dados['telefone_responsavel'],
            email_responsavel=dados['email_responsavel'],
            informacoes_adicionais=dados.get('informacoes_adicionais')
        )
        db.session.add(aluno)
        db.session.commit()
        logger.info(f'CREATE: Aluno {aluno.nome_completo} inserido com sucesso.')
        return jsonify(aluno.to_dict()), 201
    except Exception as e:
        logger.error(f'ERROR: Falha ao cadastrar aluno - {e}')
        return jsonify({'error': 'Falha ao cadastrar aluno'}), 500

@app.route('/alunos/<aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    try:
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            logger.warning(f'UPDATE: Aluno com ID {aluno_id} não encontrado.')
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        dados = request.json
        if 'nome_completo' in dados:
            aluno.nome_completo = dados['nome_completo']
        if 'data_nascimento' in dados:
            aluno.data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        if 'id_turma' in dados:
            aluno.id_turma = dados['id_turma']
        if 'nome_responsavel' in dados:
            aluno.nome_responsavel = dados['nome_responsavel']
        if 'telefone_responsavel' in dados:
            aluno.telefone_responsavel = dados['telefone_responsavel']
        if 'email_responsavel' in dados:
            aluno.email_responsavel = dados['email_responsavel']
        if 'informacoes_adicionais' in dados:
            aluno.informacoes_adicionais = dados['informacoes_adicionais']
        
        db.session.commit()
        logger.info(f'UPDATE: Aluno com ID {aluno_id} atualizado com sucesso.')
        return jsonify(aluno.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao atualizar aluno com ID {aluno_id} - {e}')
        return jsonify({'error': 'Falha ao atualizar aluno'}), 500

@app.route('/alunos/<aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    try:
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            logger.warning(f'DELETE: Aluno com ID {aluno_id} não encontrado.')
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        db.session.delete(aluno)
        db.session.commit()
        logger.info(f'DELETE: Aluno com ID {aluno_id} removido com sucesso.')
        return '', 204
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir aluno com ID {aluno_id} - {e}')
        return jsonify({'error': 'Falha ao excluir aluno'}), 500

# Rotas para Pagamentos
@app.route('/pagamentos', methods=['GET'])
def listar_pagamentos():
    try:
        pagamentos = Pagamento.query.all()
        logger.info('READ: Listagem de todos os pagamentos solicitada.')
        return jsonify([pagamento.to_dict() for pagamento in pagamentos])
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar pagamentos - {e}')
        return jsonify({'error': 'Falha ao listar pagamentos'}), 500

@app.route('/pagamentos/<pagamento_id>', methods=['GET'])
def obter_pagamento(pagamento_id):
    try:
        pagamento = Pagamento.query.get(pagamento_id)
        if not pagamento:
            logger.warning(f'READ: Pagamento com ID {pagamento_id} não encontrado.')
            return jsonify({'error': 'Pagamento não encontrado'}), 404
        logger.info(f'READ: Pagamento com ID {pagamento_id} encontrado.')
        return jsonify(pagamento.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao obter pagamento com ID {pagamento_id} - {e}')
        return jsonify({'error': 'Falha ao obter pagamento'}), 500

@app.route('/pagamentos', methods=['POST'])
def cadastrar_pagamento():
    try:
        dados = request.json
        data_pagamento = datetime.strptime(dados['data_pagamento'], '%Y-%m-%d').date() if 'data_pagamento' in dados else None
        
        pagamento = Pagamento(
            id_aluno=dados['id_aluno'],
            data_pagamento=data_pagamento,
            valor_pago=dados['valor_pago'],
            forma_pagamento=dados['forma_pagamento'],
            referencia=dados['referencia'],
            status=dados['status']
        )
        db.session.add(pagamento)
        db.session.commit()
        logger.info(f'CREATE: Pagamento para aluno ID {pagamento.id_aluno} inserido com sucesso.')
        return jsonify(pagamento.to_dict()), 201
    except Exception as e:
        logger.error(f'ERROR: Falha ao cadastrar pagamento - {e}')
        return jsonify({'error': 'Falha ao cadastrar pagamento'}), 500

@app.route('/pagamentos/<pagamento_id>', methods=['PUT'])
def atualizar_pagamento(pagamento_id):
    try:
        pagamento = Pagamento.query.get(pagamento_id)
        if not pagamento:
            logger.warning(f'UPDATE: Pagamento com ID {pagamento_id} não encontrado.')
            return jsonify({'error': 'Pagamento não encontrado'}), 404
        
        dados = request.json
        if 'id_aluno' in dados:
            pagamento.id_aluno = dados['id_aluno']
        if 'data_pagamento' in dados:
            pagamento.data_pagamento = datetime.strptime(dados['data_pagamento'], '%Y-%m-%d').date()
        if 'valor_pago' in dados:
            pagamento.valor_pago = dados['valor_pago']
        if 'forma_pagamento' in dados:
            pagamento.forma_pagamento = dados['forma_pagamento']
        if 'referencia' in dados:
            pagamento.referencia = dados['referencia']
        if 'status' in dados:
            pagamento.status = dados['status']
        
        db.session.commit()
        logger.info(f'UPDATE: Pagamento com ID {pagamento_id} atualizado com sucesso.')
        return jsonify(pagamento.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao atualizar pagamento com ID {pagamento_id} - {e}')
        return jsonify({'error': 'Falha ao atualizar pagamento'}), 500

@app.route('/pagamentos/<pagamento_id>', methods=['DELETE'])
def excluir_pagamento(pagamento_id):
    try:
        pagamento = Pagamento.query.get(pagamento_id)
        if not pagamento:
            logger.warning(f'DELETE: Pagamento com ID {pagamento_id} não encontrado.')
            return jsonify({'error': 'Pagamento não encontrado'}), 404
        
        db.session.delete(pagamento)
        db.session.commit()
        logger.info(f'DELETE: Pagamento com ID {pagamento_id} removido com sucesso.')
        return '', 204
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir pagamento com ID {pagamento_id} - {e}')
        return jsonify({'error': 'Falha ao excluir pagamento'}), 500

# Rotas para Presenças
@app.route('/presencas', methods=['GET'])
def listar_presencas():
    try:
        presencas = Presenca.query.all()
        logger.info('READ: Listagem de todas as presenças solicitada.')
        return jsonify([presenca.to_dict() for presenca in presencas])
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar presenças - {e}')
        return jsonify({'error': 'Falha ao listar presenças'}), 500

@app.route('/presencas/<presenca_id>', methods=['GET'])
def obter_presenca(presenca_id):
    try:
        presenca = Presenca.query.get(presenca_id)
        if not presenca:
            logger.warning(f'READ: Presença com ID {presenca_id} não encontrada.')
            return jsonify({'error': 'Presença não encontrada'}), 404
        logger.info(f'READ: Presença com ID {presenca_id} encontrada.')
        return jsonify(presenca.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao obter presença com ID {presenca_id} - {e}')
        return jsonify({'error': 'Falha ao obter presença'}), 500

@app.route('/presencas', methods=['POST'])
def cadastrar_presenca():
    try:
        dados = request.json
        data_presenca = datetime.strptime(dados['data_presenca'], '%Y-%m-%d').date() if 'data_presenca' in dados else None
        
        presenca = Presenca(
            id_aluno=dados['id_aluno'],
            data_presenca=data_presenca,
            presente=dados['presente']
        )
        db.session.add(presenca)
        db.session.commit()
        logger.info(f'CREATE: Presença para aluno ID {presenca.id_aluno} inserida com sucesso.')
        return jsonify(presenca.to_dict()), 201
    except Exception as e:
        logger.error(f'ERROR: Falha ao cadastrar presença - {e}')
        return jsonify({'error': 'Falha ao cadastrar presença'}), 500

@app.route('/presencas/<presenca_id>', methods=['PUT'])
def atualizar_presenca(presenca_id):
    try:
        presenca = Presenca.query.get(presenca_id)
        if not presenca:
            logger.warning(f'UPDATE: Presença com ID {presenca_id} não encontrada.')
            return jsonify({'error': 'Presença não encontrada'}), 404
        
        dados = request.json
        if 'id_aluno' in dados:
            presenca.id_aluno = dados['id_aluno']
        if 'data_presenca' in dados:
            presenca.data_presenca = datetime.strptime(dados['data_presenca'], '%Y-%m-%d').date()
        if 'presente' in dados:
            presenca.presente = dados['presente']
        
        db.session.commit()
        logger.info(f'UPDATE: Presença com ID {presenca_id} atualizada com sucesso.')
        return jsonify(presenca.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao atualizar presença com ID {presenca_id} - {e}')
        return jsonify({'error': 'Falha ao atualizar presença'}), 500

@app.route('/presencas/<presenca_id>', methods=['DELETE'])
def excluir_presenca(presenca_id):
    try:
        presenca = Presenca.query.get(presenca_id)
        if not presenca:
            logger.warning(f'DELETE: Presença com ID {presenca_id} não encontrada.')
            return jsonify({'error': 'Presença não encontrada'}), 404
        
        db.session.delete(presenca)
        db.session.commit()
        logger.info(f'DELETE: Presença com ID {presenca_id} removida com sucesso.')
        return '', 204
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir presença com ID {presenca_id} - {e}')
        return jsonify({'error': 'Falha ao excluir presença'}), 500

# Rotas para Atividades
@app.route('/atividades', methods=['GET'])
def listar_atividades():
    try:
        atividades = Atividade.query.all()
        logger.info('READ: Listagem de todas as atividades solicitada.')
        return jsonify([atividade.to_dict() for atividade in atividades])
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar atividades - {e}')
        return jsonify({'error': 'Falha ao listar atividades'}), 500

@app.route('/atividades/<atividade_id>', methods=['GET'])
def obter_atividade(atividade_id):
    try:
        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            logger.warning(f'READ: Atividade com ID {atividade_id} não encontrada.')
            return jsonify({'error': 'Atividade não encontrada'}), 404
        logger.info(f'READ: Atividade com ID {atividade_id} encontrada.')
        return jsonify(atividade.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao obter atividade com ID {atividade_id} - {e}')
        return jsonify({'error': 'Falha ao obter atividade'}), 500

@app.route('/atividades', methods=['POST'])
def cadastrar_atividade():
    try:
        dados = request.json
        data_realizacao = datetime.strptime(dados['data_realizacao'], '%Y-%m-%d').date() if 'data_realizacao' in dados else None
        
        atividade = Atividade(
            descricao=dados['descricao'],
            data_realizacao=data_realizacao
        )
        db.session.add(atividade)
        db.session.commit()
        logger.info(f'CREATE: Atividade {atividade.descricao} inserida com sucesso.')
        return jsonify(atividade.to_dict()), 201
    except Exception as e:
        logger.error(f'ERROR: Falha ao cadastrar atividade - {e}')
        return jsonify({'error': 'Falha ao cadastrar atividade'}), 500

@app.route('/atividades/<atividade_id>', methods=['PUT'])
def atualizar_atividade(atividade_id):
    try:
        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            logger.warning(f'UPDATE: Atividade com ID {atividade_id} não encontrada.')
            return jsonify({'error': 'Atividade não encontrada'}), 404
        
        dados = request.json
        if 'descricao' in dados:
            atividade.descricao = dados['descricao']
        if 'data_realizacao' in dados:
            atividade.data_realizacao = datetime.strptime(dados['data_realizacao'], '%Y-%m-%d').date()
        
        db.session.commit()
        logger.info(f'UPDATE: Atividade com ID {atividade_id} atualizada com sucesso.')
        return jsonify(atividade.to_dict())
    except Exception as e:
        logger.error(f'ERROR: Falha ao atualizar atividade com ID {atividade_id} - {e}')
        return jsonify({'error': 'Falha ao atualizar atividade'}), 500

@app.route('/atividades/<atividade_id>', methods=['DELETE'])
def excluir_atividade(atividade_id):
    try:
        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            logger.warning(f'DELETE: Atividade com ID {atividade_id} não encontrada.')
            return jsonify({'error': 'Atividade não encontrada'}), 404
        
        db.session.delete(atividade)
        db.session.commit()
        logger.info(f'DELETE: Atividade com ID {atividade_id} removida com sucesso.')
        return '', 204
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir atividade com ID {atividade_id} - {e}')
        return jsonify({'error': 'Falha ao excluir atividade'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)