
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aluno(db.Model):
    __tablename__ = 'alunos'
    aluno_id = db.Column(db.String(5), primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    endereco = db.Column(db.String(60))
    cidade = db.Column(db.String(15))
    estado = db.Column(db.String(15))
    cep = db.Column(db.String(10))
    pais = db.Column(db.String(15))
    telefone = db.Column(db.String(24))

    def to_dict(self):
        return {
            'aluno_id': self.aluno_id,
            'nome': self.nome,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'pais': self.pais,
            'telefone': self.telefone
        }
