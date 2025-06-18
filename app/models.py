from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Professor(db.Model):
    id_professor = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id_professor': self.id_professor,
            'nome_completo': self.nome_completo,
            'email': self.email,
            'telefone': self.telefone
        }

class Turma(db.Model):
    id_turma = db.Column(db.Integer, primary_key=True)
    nome_turma = db.Column(db.String(50))
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id_professor'))
    horario = db.Column(db.String(100))
    
    professor = db.relationship('Professor', backref='turmas')
    alunos = db.relationship('Aluno', backref='turma', lazy=True)

    def to_dict(self):
        return {
            'id_turma': self.id_turma,
            'nome_turma': self.nome_turma,
            'id_professor': self.id_professor,
            'horario': self.horario
        }

class Aluno(db.Model):
    id_aluno = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255))
    data_nascimento = db.Column(db.Date)
    id_turma = db.Column(db.Integer, db.ForeignKey('turma.id_turma'))
    nome_responsavel = db.Column(db.String(255))
    telefone_responsavel = db.Column(db.String(20))
    email_responsavel = db.Column(db.String(100))
    informacoes_adicionais = db.Column(db.Text)
    
    pagamentos = db.relationship('Pagamento', backref='aluno', lazy=True)
    presencas = db.relationship('Presenca', backref='aluno', lazy=True)
    
    def to_dict(self):
        return {
            'id_aluno': self.id_aluno,
            'nome_completo': self.nome_completo,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            'id_turma': self.id_turma,
            'nome_responsavel': self.nome_responsavel,
            'telefone_responsavel': self.telefone_responsavel,
            'email_responsavel': self.email_responsavel,
            'informacoes_adicionais': self.informacoes_adicionais
        }

class Pagamento(db.Model):
    id_pagamento = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'))
    data_pagamento = db.Column(db.Date)
    valor_pago = db.Column(db.Numeric(10, 2))
    forma_pagamento = db.Column(db.String(50))
    referencia = db.Column(db.String(100))
    status = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id_pagamento': self.id_pagamento,
            'id_aluno': self.id_aluno,
            'data_pagamento': self.data_pagamento.strftime('%Y-%m-%d') if self.data_pagamento else None,
            'valor_pago': float(self.valor_pago) if self.valor_pago else None,
            'forma_pagamento': self.forma_pagamento,
            'referencia': self.referencia,
            'status': self.status
        }

class Presenca(db.Model):
    id_presenca = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'))
    data_presenca = db.Column(db.Date)
    presente = db.Column(db.Boolean)
    
    def to_dict(self):
        return {
            'id_presenca': self.id_presenca,
            'id_aluno': self.id_aluno,
            'data_presenca': self.data_presenca.strftime('%Y-%m-%d') if self.data_presenca else None,
            'presente': self.presente
        }

class Atividade(db.Model):
    id_atividade = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text)
    data_realizacao = db.Column(db.Date)
    
    alunos = db.relationship('Aluno', secondary='atividade_aluno', backref=db.backref('atividades', lazy='dynamic'))
    
    def to_dict(self):
        return {
            'id_atividade': self.id_atividade,
            'descricao': self.descricao,
            'data_realizacao': self.data_realizacao.strftime('%Y-%m-%d') if self.data_realizacao else None,
            'alunos': [{'id_aluno': aluno.id_aluno, 'nome_completo': aluno.nome_completo} for aluno in self.alunos]
        }

class AtividadeAluno(db.Model):
    __tablename__ = 'atividade_aluno'
    id_atividade = db.Column(db.Integer, db.ForeignKey('atividade.id_atividade'), primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'), primary_key=True)

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(255))
    nivel_acesso = db.Column(db.String(20))
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id_professor'), nullable=True)
    
    professor = db.relationship('Professor', backref='usuario')
    
    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'login': self.login,
            'nivel_acesso': self.nivel_acesso,
            'id_professor': self.id_professor
        }