import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify, render_template, redirect
from flask_restx import Api, Resource, fields
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

# Configuração do Swagger
api = Api(app, 
    version='1.0', 
    title='API Escola Infantil',
    description='Sistema de Gestão para Escola Infantil',
    doc='/swagger/'
)

# Namespaces
ns_professores = api.namespace('professores', description='Operações com professores')
ns_turmas = api.namespace('turmas', description='Operações com turmas')
ns_alunos = api.namespace('alunos', description='Operações com alunos')
ns_pagamentos = api.namespace('pagamentos', description='Operações com pagamentos')
ns_atividades = api.namespace('atividades', description='Operações com atividades')

# Modelos Swagger
professor_model = api.model('Professor', {
    'nome_completo': fields.String(required=True, description='Nome completo do professor'),
    'email': fields.String(required=True, description='Email do professor'),
    'telefone': fields.String(required=True, description='Telefone do professor')
})

turma_model = api.model('Turma', {
    'nome_turma': fields.String(required=True, description='Nome da turma'),
    'id_professor': fields.Integer(required=True, description='ID do professor'),
    'horario': fields.String(required=True, description='Horário da turma')
})

aluno_model = api.model('Aluno', {
    'nome_completo': fields.String(required=True, description='Nome completo do aluno'),
    'data_nascimento': fields.String(required=True, description='Data de nascimento (YYYY-MM-DD)'),
    'id_turma': fields.Integer(required=True, description='ID da turma'),
    'nome_responsavel': fields.String(required=True, description='Nome do responsável'),
    'telefone_responsavel': fields.String(required=True, description='Telefone do responsável'),
    'email_responsavel': fields.String(required=True, description='Email do responsável'),
    'informacoes_adicionais': fields.String(description='Informações adicionais')
})

pagamento_model = api.model('Pagamento', {
    'id_aluno': fields.Integer(required=True, description='ID do aluno'),
    'data_pagamento': fields.String(required=True, description='Data do pagamento (YYYY-MM-DD)'),
    'valor_pago': fields.Float(required=True, description='Valor pago'),
    'forma_pagamento': fields.String(required=True, description='Forma de pagamento'),
    'referencia': fields.String(required=True, description='Referência do pagamento'),
    'status': fields.String(required=True, description='Status do pagamento')
})

atividade_model = api.model('Atividade', {
    'descricao': fields.String(required=True, description='Descrição da atividade'),
    'data_realizacao': fields.String(required=True, description='Data de realização (YYYY-MM-DD)')
})

# Inicialização do banco de dados com tratamento de erro
try:
    with app.app_context():
        db.create_all()
        logger.info("Tabelas do banco de dados criadas com sucesso")
except Exception as e:
    logger.error(f"Erro ao criar tabelas do banco de dados: {e}")

# Rota para API
@app.route('/api')
def api_index():
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

# Rotas para Professores com Swagger
@ns_professores.route('/')
class ProfessoresList(Resource):
    @ns_professores.doc('listar_professores')
    def get(self):
        """Lista todos os professores"""
        try:
            professores = Professor.query.all()
            logger.info('READ: Listagem de todos os professores solicitada.')
            return [professor.to_dict() for professor in professores]
        except Exception as e:
            logger.error(f'ERROR: Falha ao listar professores - {e}')
            return {'error': 'Falha ao listar professores'}, 500
    
    @ns_professores.doc('cadastrar_professor')
    @ns_professores.expect(professor_model)
    def post(self):
        """Cadastra um novo professor"""
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
            return professor.to_dict(), 201
        except Exception as e:
            logger.error(f'ERROR: Falha ao cadastrar professor - {e}')
            return {'error': 'Falha ao cadastrar professor'}, 500

@ns_professores.route('/<int:professor_id>')
class ProfessorResource(Resource):
    @ns_professores.doc('obter_professor')
    def get(self, professor_id):
        """Obtém um professor por ID"""
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                logger.warning(f'READ: Professor com ID {professor_id} não encontrado.')
                return {'error': 'Professor não encontrado'}, 404
            logger.info(f'READ: Professor com ID {professor_id} encontrado.')
            return professor.to_dict()
        except Exception as e:
            logger.error(f'ERROR: Falha ao obter professor com ID {professor_id} - {e}')
            return {'error': 'Falha ao obter professor'}, 500
    
    @ns_professores.doc('atualizar_professor')
    @ns_professores.expect(professor_model)
    def put(self, professor_id):
        """Atualiza um professor"""
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                logger.warning(f'UPDATE: Professor com ID {professor_id} não encontrado.')
                return {'error': 'Professor não encontrado'}, 404
            
            dados = request.json
            if 'nome_completo' in dados:
                professor.nome_completo = dados['nome_completo']
            if 'email' in dados:
                professor.email = dados['email']
            if 'telefone' in dados:
                professor.telefone = dados['telefone']
            
            db.session.commit()
            logger.info(f'UPDATE: Professor com ID {professor_id} atualizado com sucesso.')
            return professor.to_dict()
        except Exception as e:
            logger.error(f'ERROR: Falha ao atualizar professor com ID {professor_id} - {e}')
            return {'error': 'Falha ao atualizar professor'}, 500
    
    @ns_professores.doc('excluir_professor')
    def delete(self, professor_id):
        """Exclui um professor"""
        try:
            professor = Professor.query.get(professor_id)
            if not professor:
                logger.warning(f'DELETE: Professor com ID {professor_id} não encontrado.')
                return {'error': 'Professor não encontrado'}, 404
            
            db.session.delete(professor)
            db.session.commit()
            logger.info(f'DELETE: Professor com ID {professor_id} removido com sucesso.')
            return '', 204
        except Exception as e:
            logger.error(f'ERROR: Falha ao excluir professor com ID {professor_id} - {e}')
            return {'error': 'Falha ao excluir professor'}, 500

# Rotas para Turmas com Swagger
@ns_turmas.route('/')
class TurmasList(Resource):
    @ns_turmas.doc('listar_turmas')
    def get(self):
        """Lista todas as turmas"""
        try:
            turmas = Turma.query.all()
            logger.info('READ: Listagem de todas as turmas solicitada.')
            return [turma.to_dict() for turma in turmas]
        except Exception as e:
            logger.error(f'ERROR: Falha ao listar turmas - {e}')
            return {'error': 'Falha ao listar turmas'}, 500
    
    @ns_turmas.doc('cadastrar_turma')
    @ns_turmas.expect(turma_model)
    def post(self):
        """Cadastra uma nova turma"""
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
            return turma.to_dict(), 201
        except Exception as e:
            logger.error(f'ERROR: Falha ao cadastrar turma - {e}')
            return {'error': 'Falha ao cadastrar turma'}, 500

@ns_turmas.route('/<int:turma_id>')
class TurmaResource(Resource):
    @ns_turmas.doc('obter_turma')
    def get(self, turma_id):
        """Obtém uma turma por ID"""
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                logger.warning(f'READ: Turma com ID {turma_id} não encontrada.')
                return {'error': 'Turma não encontrada'}, 404
            logger.info(f'READ: Turma com ID {turma_id} encontrada.')
            return turma.to_dict()
        except Exception as e:
            logger.error(f'ERROR: Falha ao obter turma com ID {turma_id} - {e}')
            return {'error': 'Falha ao obter turma'}, 500
    
    @ns_turmas.doc('atualizar_turma')
    @ns_turmas.expect(turma_model)
    def put(self, turma_id):
        """Atualiza uma turma"""
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                logger.warning(f'UPDATE: Turma com ID {turma_id} não encontrada.')
                return {'error': 'Turma não encontrada'}, 404
            
            dados = request.json
            if 'nome_turma' in dados:
                turma.nome_turma = dados['nome_turma']
            if 'id_professor' in dados:
                turma.id_professor = dados['id_professor']
            if 'horario' in dados:
                turma.horario = dados['horario']
            
            db.session.commit()
            logger.info(f'UPDATE: Turma com ID {turma_id} atualizada com sucesso.')
            return turma.to_dict()
        except Exception as e:
            logger.error(f'ERROR: Falha ao atualizar turma com ID {turma_id} - {e}')
            return {'error': 'Falha ao atualizar turma'}, 500
    
    @ns_turmas.doc('excluir_turma')
    def delete(self, turma_id):
        """Exclui uma turma"""
        try:
            turma = Turma.query.get(turma_id)
            if not turma:
                logger.warning(f'DELETE: Turma com ID {turma_id} não encontrada.')
                return {'error': 'Turma não encontrada'}, 404
            
            db.session.delete(turma)
            db.session.commit()
            logger.info(f'DELETE: Turma com ID {turma_id} removida com sucesso.')
            return '', 204
        except Exception as e:
            logger.error(f'ERROR: Falha ao excluir turma com ID {turma_id} - {e}')
            return {'error': 'Falha ao excluir turma'}, 500

# Rotas para Alunos com Swagger
@ns_alunos.route('/')
class AlunosList(Resource):
    @ns_alunos.doc('listar_alunos')
    def get(self):
        """Lista todos os alunos"""
        try:
            alunos = Aluno.query.all()
            logger.info('READ: Listagem de todos os alunos solicitada.')
            return [aluno.to_dict() for aluno in alunos]
        except Exception as e:
            logger.error(f'ERROR: Falha ao listar alunos - {e}')
            return {'error': 'Falha ao listar alunos'}, 500
    
    @ns_alunos.doc('cadastrar_aluno')
    @ns_alunos.expect(aluno_model)
    def post(self):
        """Cadastra um novo aluno"""
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
            return aluno.to_dict(), 201
        except Exception as e:
            logger.error(f'ERROR: Falha ao cadastrar aluno - {e}')
            return {'error': 'Falha ao cadastrar aluno'}, 500

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

# Rotas para Pagamentos com Swagger
@ns_pagamentos.route('/')
class PagamentosList(Resource):
    @ns_pagamentos.doc('listar_pagamentos')
    def get(self):
        """Lista todos os pagamentos"""
        try:
            pagamentos = Pagamento.query.all()
            logger.info('READ: Listagem de todos os pagamentos solicitada.')
            return [pagamento.to_dict() for pagamento in pagamentos]
        except Exception as e:
            logger.error(f'ERROR: Falha ao listar pagamentos - {e}')
            return {'error': 'Falha ao listar pagamentos'}, 500
    
    @ns_pagamentos.doc('cadastrar_pagamento')
    @ns_pagamentos.expect(pagamento_model)
    def post(self):
        """Cadastra um novo pagamento"""
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
            return pagamento.to_dict(), 201
        except Exception as e:
            logger.error(f'ERROR: Falha ao cadastrar pagamento - {e}')
            return {'error': 'Falha ao cadastrar pagamento'}, 500

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

# Rotas para Atividades com Swagger
@ns_atividades.route('/')
class AtividadesList(Resource):
    @ns_atividades.doc('listar_atividades')
    def get(self):
        """Lista todas as atividades"""
        try:
            atividades = Atividade.query.all()
            logger.info('READ: Listagem de todas as atividades solicitada.')
            return [atividade.to_dict() for atividade in atividades]
        except Exception as e:
            logger.error(f'ERROR: Falha ao listar atividades - {e}')
            return {'error': 'Falha ao listar atividades'}, 500
    
    @ns_atividades.doc('cadastrar_atividade')
    @ns_atividades.expect(atividade_model)
    def post(self):
        """Cadastra uma nova atividade"""
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
            return atividade.to_dict(), 201
        except Exception as e:
            logger.error(f'ERROR: Falha ao cadastrar atividade - {e}')
            return {'error': 'Falha ao cadastrar atividade'}, 500

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

# Rotas para renderizar as páginas HTML
@app.route('/')
def home():
    try:
        total_turmas = Turma.query.count()
        total_professores = Professor.query.count()
        total_alunos = Aluno.query.count()
        return render_template('index.html', 
                              total_turmas=total_turmas,
                              total_professores=total_professores,
                              total_alunos=total_alunos)
    except Exception as e:
        logger.error(f'ERROR: Falha ao renderizar página inicial - {e}')
        return render_template('error.html', error='Falha ao carregar a página inicial')

@app.route('/turmas_view')
def turmas_view():
    try:
        turmas = Turma.query.all()
        return render_template('turmas.html', turmas=turmas)
    except Exception as e:
        logger.error(f'ERROR: Falha ao renderizar página de turmas - {e}')
        return render_template('error.html', error='Falha ao carregar a página de turmas')

@app.route('/turmas/nova', methods=['GET', 'POST'])
def nova_turma():
    try:
        if request.method == 'POST':
            nome_turma = request.form['nome_turma']
            id_professor = request.form['id_professor']
            horario = request.form['horario']
            
            turma = Turma(
                nome_turma=nome_turma,
                id_professor=id_professor,
                horario=horario
            )
            db.session.add(turma)
            db.session.commit()
            logger.info(f'CREATE: Turma {turma.nome_turma} inserida com sucesso via formulário.')
            return redirect('/turmas_view')
        
        professores = Professor.query.all()
        return render_template('nova_turma.html', professores=professores)
    except Exception as e:
        logger.error(f'ERROR: Falha ao criar nova turma - {e}')
        return render_template('error.html', error='Falha ao criar nova turma')

@app.route('/turmas/<turma_id>/edit', methods=['GET', 'POST'])
def editar_turma(turma_id):
    try:
        turma = Turma.query.get(turma_id)
        if not turma:
            logger.warning(f'UPDATE: Turma com ID {turma_id} não encontrada.')
            return render_template('error.html', error='Turma não encontrada')
        
        if request.method == 'POST':
            turma.nome_turma = request.form['nome_turma']
            turma.id_professor = request.form['id_professor']
            turma.horario = request.form['horario']
            
            db.session.commit()
            logger.info(f'UPDATE: Turma com ID {turma_id} atualizada com sucesso via formulário.')
            return redirect('/turmas_view')
        
        professores = Professor.query.all()
        return render_template('editar_turma.html', turma=turma, professores=professores)
    except Exception as e:
        logger.error(f'ERROR: Falha ao editar turma com ID {turma_id} - {e}')
        return render_template('error.html', error='Falha ao editar turma')

@app.route('/turmas/<turma_id>/delete')
def deletar_turma_view(turma_id):
    try:
        turma = Turma.query.get(turma_id)
        if not turma:
            logger.warning(f'DELETE: Turma com ID {turma_id} não encontrada.')
            return render_template('error.html', error='Turma não encontrada')
        
        db.session.delete(turma)
        db.session.commit()
        logger.info(f'DELETE: Turma com ID {turma_id} removida com sucesso via interface web.')
        return redirect('/turmas_view')
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir turma com ID {turma_id} - {e}')
        return render_template('error.html', error='Falha ao excluir turma')

@app.route('/professores_view')
def professores_view():
    try:
        professores = Professor.query.all()
        return render_template('professores.html', professores=professores)
    except Exception as e:
        logger.error(f'ERROR: Falha ao renderizar página de professores - {e}')
        return render_template('error.html', error='Falha ao carregar a página de professores')

@app.route('/professores/novo', methods=['GET', 'POST'])
def novo_professor():
    try:
        if request.method == 'POST':
            nome_completo = request.form['nome_completo']
            email = request.form['email']
            telefone = request.form['telefone']
            
            professor = Professor(
                nome_completo=nome_completo,
                email=email,
                telefone=telefone
            )
            db.session.add(professor)
            db.session.commit()
            logger.info(f'CREATE: Professor {professor.nome_completo} inserido com sucesso via formulário.')
            return redirect('/professores_view')
        
        return render_template('novo_professor.html')
    except Exception as e:
        logger.error(f'ERROR: Falha ao criar novo professor - {e}')
        return render_template('error.html', error='Falha ao criar novo professor')

@app.route('/professores/<professor_id>/edit', methods=['GET', 'POST'])
def editar_professor(professor_id):
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            logger.warning(f'UPDATE: Professor com ID {professor_id} não encontrado.')
            return render_template('error.html', error='Professor não encontrado')
        
        if request.method == 'POST':
            professor.nome_completo = request.form['nome_completo']
            professor.email = request.form['email']
            professor.telefone = request.form['telefone']
            
            db.session.commit()
            logger.info(f'UPDATE: Professor com ID {professor_id} atualizado com sucesso via formulário.')
            return redirect('/professores_view')
        
        return render_template('editar_professor.html', professor=professor)
    except Exception as e:
        logger.error(f'ERROR: Falha ao editar professor com ID {professor_id} - {e}')
        return render_template('error.html', error='Falha ao editar professor')

@app.route('/professores/<professor_id>/delete')
def deletar_professor_view(professor_id):
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            logger.warning(f'DELETE: Professor com ID {professor_id} não encontrado.')
            return render_template('error.html', error='Professor não encontrado')
        
        db.session.delete(professor)
        db.session.commit()
        logger.info(f'DELETE: Professor com ID {professor_id} removido com sucesso via interface web.')
        return redirect('/professores_view')
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir professor com ID {professor_id} - {e}')
        return render_template('error.html', error='Falha ao excluir professor')

@app.route('/alunos_view')
def alunos_view():
    try:
        alunos = Aluno.query.all()
        return render_template('alunos.html', alunos=alunos)
    except Exception as e:
        logger.error(f'ERROR: Falha ao renderizar página de alunos - {e}')
        return render_template('error.html', error='Falha ao carregar a página de alunos')

@app.route('/alunos/novo', methods=['GET', 'POST'])
def novo_aluno():
    try:
        if request.method == 'POST':
            nome_completo = request.form['nome_completo']
            data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date() if request.form['data_nascimento'] else None
            id_turma = request.form['id_turma']
            nome_responsavel = request.form['nome_responsavel']
            telefone_responsavel = request.form['telefone_responsavel']
            email_responsavel = request.form['email_responsavel']
            informacoes_adicionais = request.form.get('informacoes_adicionais', '')
            
            aluno = Aluno(
                nome_completo=nome_completo,
                data_nascimento=data_nascimento,
                id_turma=id_turma,
                nome_responsavel=nome_responsavel,
                telefone_responsavel=telefone_responsavel,
                email_responsavel=email_responsavel,
                informacoes_adicionais=informacoes_adicionais
            )
            db.session.add(aluno)
            db.session.commit()
            logger.info(f'CREATE: Aluno {aluno.nome_completo} inserido com sucesso via formulário.')
            return redirect('/alunos_view')
        
        turmas = Turma.query.all()
        return render_template('novo_aluno.html', turmas=turmas)
    except Exception as e:
        logger.error(f'ERROR: Falha ao criar novo aluno - {e}')
        return render_template('error.html', error='Falha ao criar novo aluno')

@app.route('/alunos/<aluno_id>/edit', methods=['GET', 'POST'])
def editar_aluno(aluno_id):
    try:
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            logger.warning(f'UPDATE: Aluno com ID {aluno_id} não encontrado.')
            return render_template('error.html', error='Aluno não encontrado')
        
        if request.method == 'POST':
            aluno.nome_completo = request.form['nome_completo']
            aluno.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date() if request.form['data_nascimento'] else None
            aluno.id_turma = request.form['id_turma']
            aluno.nome_responsavel = request.form['nome_responsavel']
            aluno.telefone_responsavel = request.form['telefone_responsavel']
            aluno.email_responsavel = request.form['email_responsavel']
            aluno.informacoes_adicionais = request.form.get('informacoes_adicionais', '')
            
            db.session.commit()
            logger.info(f'UPDATE: Aluno com ID {aluno_id} atualizado com sucesso via formulário.')
            return redirect('/alunos_view')
        
        turmas = Turma.query.all()
        return render_template('editar_aluno.html', aluno=aluno, turmas=turmas)
    except Exception as e:
        logger.error(f'ERROR: Falha ao editar aluno com ID {aluno_id} - {e}')
        return render_template('error.html', error='Falha ao editar aluno')

@app.route('/alunos/<aluno_id>/delete')
def deletar_aluno_view(aluno_id):
    try:
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            logger.warning(f'DELETE: Aluno com ID {aluno_id} não encontrado.')
            return render_template('error.html', error='Aluno não encontrado')
        
        db.session.delete(aluno)
        db.session.commit()
        logger.info(f'DELETE: Aluno com ID {aluno_id} removido com sucesso via interface web.')
        return redirect('/alunos_view')
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir aluno com ID {aluno_id} - {e}')
        return render_template('error.html', error='Falha ao excluir aluno')

@app.route('/pagamentos_view')
def pagamentos_view():
    try:
        pagamentos = Pagamento.query.all()
        return render_template('pagamentos.html', pagamentos=pagamentos)
    except Exception as e:
        logger.error(f'ERROR: Falha ao renderizar página de pagamentos - {e}')
        return render_template('error.html', error='Falha ao carregar a página de pagamentos')

@app.route('/pagamentos/novo', methods=['GET', 'POST'])
def novo_pagamento():
    try:
        if request.method == 'POST':
            id_aluno = request.form['id_aluno']
            data_pagamento = datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d').date() if request.form['data_pagamento'] else None
            valor_pago = request.form['valor_pago']
            forma_pagamento = request.form['forma_pagamento']
            referencia = request.form['referencia']
            status = request.form['status']
            
            pagamento = Pagamento(
                id_aluno=id_aluno,
                data_pagamento=data_pagamento,
                valor_pago=valor_pago,
                forma_pagamento=forma_pagamento,
                referencia=referencia,
                status=status
            )
            db.session.add(pagamento)
            db.session.commit()
            logger.info(f'CREATE: Pagamento para aluno ID {pagamento.id_aluno} inserido com sucesso via formulário.')
            return redirect('/pagamentos_view')
        
        alunos = Aluno.query.all()
        return render_template('novo_pagamento.html', alunos=alunos)
    except Exception as e:
        logger.error(f'ERROR: Falha ao criar novo pagamento - {e}')
        return render_template('error.html', error='Falha ao criar novo pagamento')

@app.route('/pagamentos/<pagamento_id>/edit', methods=['GET', 'POST'])
def editar_pagamento(pagamento_id):
    try:
        pagamento = Pagamento.query.get(pagamento_id)
        if not pagamento:
            logger.warning(f'UPDATE: Pagamento com ID {pagamento_id} não encontrado.')
            return render_template('error.html', error='Pagamento não encontrado')
        
        if request.method == 'POST':
            pagamento.id_aluno = request.form['id_aluno']
            pagamento.data_pagamento = datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d').date() if request.form['data_pagamento'] else None
            pagamento.valor_pago = request.form['valor_pago']
            pagamento.forma_pagamento = request.form['forma_pagamento']
            pagamento.referencia = request.form['referencia']
            pagamento.status = request.form['status']
            
            db.session.commit()
            logger.info(f'UPDATE: Pagamento com ID {pagamento_id} atualizado com sucesso via formulário.')
            return redirect('/pagamentos_view')
        
        alunos = Aluno.query.all()
        return render_template('editar_pagamento.html', pagamento=pagamento, alunos=alunos)
    except Exception as e:
        logger.error(f'ERROR: Falha ao editar pagamento com ID {pagamento_id} - {e}')
        return render_template('error.html', error='Falha ao editar pagamento')

@app.route('/pagamentos/<pagamento_id>/delete')
def deletar_pagamento_view(pagamento_id):
    try:
        pagamento = Pagamento.query.get(pagamento_id)
        if not pagamento:
            logger.warning(f'DELETE: Pagamento com ID {pagamento_id} não encontrado.')
            return render_template('error.html', error='Pagamento não encontrado')
        
        db.session.delete(pagamento)
        db.session.commit()
        logger.info(f'DELETE: Pagamento com ID {pagamento_id} removido com sucesso via interface web.')
        return redirect('/pagamentos_view')
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir pagamento com ID {pagamento_id} - {e}')
        return render_template('error.html', error='Falha ao excluir pagamento')

@app.route('/atividades_view')
def atividades_view():
    try:
        atividades = Atividade.query.all()
        return render_template('atividades.html', atividades=atividades)
    except Exception as e:
        logger.error(f'ERROR: Falha ao renderizar página de atividades - {e}')
        return render_template('error.html', error='Falha ao carregar a página de atividades')

@app.route('/atividades/<atividade_id>/alunos')
def alunos_atividade(atividade_id):
    try:
        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            logger.warning(f'READ: Atividade com ID {atividade_id} não encontrada.')
            return render_template('error.html', error='Atividade não encontrada')
        
        alunos = atividade.alunos
        logger.info(f'READ: Listagem de alunos da atividade com ID {atividade_id} solicitada.')
        return render_template('alunos_atividade.html', atividade=atividade, alunos=alunos)
    except Exception as e:
        logger.error(f'ERROR: Falha ao listar alunos da atividade com ID {atividade_id} - {e}')
        return render_template('error.html', error='Falha ao listar alunos da atividade')

@app.route('/atividades/nova', methods=['GET', 'POST'])
def nova_atividade():
    try:
        if request.method == 'POST':
            descricao = request.form['descricao']
            data_realizacao = datetime.strptime(request.form['data_realizacao'], '%Y-%m-%d').date() if request.form['data_realizacao'] else None
            
            atividade = Atividade(
                descricao=descricao,
                data_realizacao=data_realizacao
            )
            
            # Se houver alunos selecionados
            alunos_ids = request.form.getlist('alunos')
            if alunos_ids:
                alunos = Aluno.query.filter(Aluno.id_aluno.in_(alunos_ids)).all()
                atividade.alunos = alunos
            
            db.session.add(atividade)
            db.session.commit()
            logger.info(f'CREATE: Atividade {atividade.descricao} inserida com sucesso via formulário.')
            return redirect('/atividades_view')
        
        alunos = Aluno.query.all()
        return render_template('nova_atividade.html', alunos=alunos)
    except Exception as e:
        logger.error(f'ERROR: Falha ao criar nova atividade - {e}')
        return render_template('error.html', error='Falha ao criar nova atividade')

@app.route('/atividades/<atividade_id>/edit', methods=['GET', 'POST'])
def editar_atividade(atividade_id):
    try:
        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            logger.warning(f'UPDATE: Atividade com ID {atividade_id} não encontrada.')
            return render_template('error.html', error='Atividade não encontrada')
        
        if request.method == 'POST':
            atividade.descricao = request.form['descricao']
            atividade.data_realizacao = datetime.strptime(request.form['data_realizacao'], '%Y-%m-%d').date() if request.form['data_realizacao'] else None
            
            # Atualizar alunos associados
            alunos_ids = request.form.getlist('alunos')
            alunos = Aluno.query.filter(Aluno.id_aluno.in_(alunos_ids)).all() if alunos_ids else []
            atividade.alunos = alunos
            
            db.session.commit()
            logger.info(f'UPDATE: Atividade com ID {atividade_id} atualizada com sucesso via formulário.')
            return redirect('/atividades_view')
        
        alunos = Aluno.query.all()
        alunos_selecionados = [aluno.id_aluno for aluno in atividade.alunos]
        return render_template('editar_atividade.html', atividade=atividade, alunos=alunos, alunos_selecionados=alunos_selecionados)
    except Exception as e:
        logger.error(f'ERROR: Falha ao editar atividade com ID {atividade_id} - {e}')
        return render_template('error.html', error='Falha ao editar atividade')

@app.route('/atividades/<atividade_id>/delete')
def deletar_atividade_view(atividade_id):
    try:
        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            logger.warning(f'DELETE: Atividade com ID {atividade_id} não encontrada.')
            return render_template('error.html', error='Atividade não encontrada')
        
        db.session.delete(atividade)
        db.session.commit()
        logger.info(f'DELETE: Atividade com ID {atividade_id} removida com sucesso via interface web.')
        return redirect('/atividades_view')
    except Exception as e:
        logger.error(f'ERROR: Falha ao excluir atividade com ID {atividade_id} - {e}')
        return render_template('error.html', error='Falha ao excluir atividade')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)