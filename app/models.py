from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Professor(db.Model):
    id_professor = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

class Turma(db.Model):
    id_turma = db.Column(db.Integer, primary_key=True)
    nome_turma = db.Column(db.String(50))
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id_professor'))
    horario = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id_turma': self.id_turma,
            'nome_turma': self.nome_turma,
            'id_professor': self.id_professor,
            'horario': self.horario
        }