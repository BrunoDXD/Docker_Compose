CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255),
    email VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE Turma (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50),
    id_professor INT,
    horario VARCHAR(100),
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor)
);

CREATE TABLE Aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255),
    data_nascimento DATE,
    id_turma INT,
    nome_responsavel VARCHAR(255),
    telefone_responsavel VARCHAR(20),
    email_responsavel VARCHAR(100),
    informacoes_adicionais TEXT,
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma)
);

CREATE TABLE Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INT,
    data_pagamento DATE,
    valor_pago DECIMAL(10, 2),
    forma_pagamento VARCHAR(50),
    referencia VARCHAR(100),
    status VARCHAR(20),
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
);

CREATE TABLE Presenca (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INT,
    data_presenca DATE,
    presente BOOLEAN,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
);

CREATE TABLE Atividade (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT,
    data_realizacao DATE
);

CREATE TABLE Atividade_Aluno (
    id_atividade INT,
    id_aluno INT,
    PRIMARY KEY (id_atividade, id_aluno),
    FOREIGN KEY (id_atividade) REFERENCES Atividade(id_atividade),
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno)
);

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE,
    senha VARCHAR(255),
    nivel_acesso VARCHAR(20),
    id_professor INT,
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor)
);

INSERT INTO Professor (nome_completo, email, telefone) VALUES
('Professor A', 'profA@example.com', '1234567890'),
('Professor B', 'profB@example.com', '1234567891'),
('Professor C', 'profC@example.com', '1234567892'),
('Professor D', 'profD@example.com', '1234567893'),
('Professor E', 'profE@example.com', '1234567894'),
('Professor F', 'profF@example.com', '1234567895'),
('Professor G', 'profG@example.com', '1234567896'),
('Professor H', 'profH@example.com', '1234567897'),
('Professor I', 'profI@example.com', '1234567898'),
('Professor J', 'profJ@example.com', '1234567899');

INSERT INTO Turma (nome_turma, id_professor, horario) VALUES
('Turma 1', 1, '08:00 - 12:00'),
('Turma 2', 2, '08:00 - 12:00'),
('Turma 3', 3, '08:00 - 12:00'),
('Turma 4', 4, '08:00 - 12:00'),
('Turma 5', 5, '08:00 - 12:00'),
('Turma 6', 6, '13:00 - 17:00'),
('Turma 7', 7, '13:00 - 17:00'),
('Turma 8', 8, '13:00 - 17:00'),
('Turma 9', 9, '13:00 - 17:00'),
('Turma 10', 10, '13:00 - 17:00');

INSERT INTO Aluno (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais) VALUES
('Aluno A', '2010-01-01', 1, 'Responsável A', '9876543210', 'respA@example.com', NULL),
('Aluno B', '2010-02-01', 2, 'Responsável B', '9876543211', 'respB@example.com', NULL),
('Aluno C', '2010-03-01', 3, 'Responsável C', '9876543212', 'respC@example.com', NULL),
('Aluno D', '2010-04-01', 4, 'Responsável D', '9876543213', 'respD@example.com', NULL),
('Aluno E', '2010-05-01', 5, 'Responsável E', '9876543214', 'respE@example.com', NULL),
('Aluno F', '2010-06-01', 6, 'Responsável F', '9876543215', 'respF@example.com', NULL),
('Aluno G', '2010-07-01', 7, 'Responsável G', '9876543216', 'respG@example.com', NULL),
('Aluno H', '2010-08-01', 8, 'Responsável H', '9876543217', 'respH@example.com', NULL),
('Aluno I', '2010-09-01', 9, 'Responsável I', '9876543218', 'respI@example.com', NULL),
('Aluno J', '2010-10-01', 10, 'Responsável J', '9876543219', 'respJ@example.com', NULL);

INSERT INTO Pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status) VALUES
(1, '2023-01-01', '500.00', 'Cartão', 'Mensalidade Janeiro', 'Pago'),
(2, '2023-02-01', '500.00', 'Cartão', 'Mensalidade Fevereiro', 'Pago'),
(3, '2023-03-01', '500.00', 'Cartão', 'Mensalidade Março', 'Pago'),
(4, '2023-04-01', '500.00', 'Cartão', 'Mensalidade Abril', 'Pago'),
(5, '2023-05-01', '500.00', 'Cartão', 'Mensalidade Maio', 'Pago'),
(6, '2023-06-01', '500.00', 'Cartão', 'Mensalidade Junho', 'Pago'),
(7, '2023-07-01', '500.00', 'Cartão', 'Mensalidade Julho', 'Pago'),
(8, '2023-08-01', '500.00', 'Cartão', 'Mensalidade Agosto', 'Pago'),
(9, '2023-09-01', '500.00', 'Cartão', 'Mensalidade Setembro', 'Pago'),
(10, '2023-10-01', '500.00', 'Cartão', 'Mensalidade Outubro', 'Pago');

INSERT INTO Presenca (id_aluno, data_presenca, presente) VALUES
(1, '2023-01-01', TRUE),
(2, '2023-01-01', TRUE),
(3, '2023-01-01', TRUE),
(4, '2023-01-01', TRUE),
(5, '2023-01-01', TRUE),
(6, '2023-01-01', TRUE),
(7, '2023-01-01', TRUE),
(8, '2023-01-01', TRUE),
(9, '2023-01-01', TRUE),
(10, '2023-01-01', TRUE);

INSERT INTO Atividade (descricao, data_realizacao) VALUES
('Atividade A', '2023-01-01'),
('Atividade B', '2023-02-01'),
('Atividade C', '2023-03-01'),
('Atividade D', '2023-04-01'),
('Atividade E', '2023-05-01'),
('Atividade F', '2023-06-01'),
('Atividade G', '2023-07-01'),
('Atividade H', '2023-08-01'),
('Atividade I', '2023-09-01'),
('Atividade J', '2023-10-01');

INSERT INTO Atividade_Aluno (id_atividade, id_aluno) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO Usuario (login, senha, nivel_acesso, id_professor) VALUES
('usuarioA', 'senhaA', 'administrador', NULL),
('usuarioB', 'senhaB', 'professor', 1),
('usuarioD', 'senhaD', 'professor', 2),
('usuarioE', 'senhaE', 'professor', 3),
('usuarioF', 'senhaF', 'professor', 4),
('usuarioG', 'senhaG', 'professor', 5),
('usuarioH', 'senhaH', 'professor', 6),
('usuarioI', 'senhaI', 'professor', 7),
('usuarioJ', 'senhaJ', 'professor', 8);