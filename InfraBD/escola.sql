\c template1;

DROP DATABASE IF EXISTS escola;
CREATE DATABASE escola;

\c escola;

CREATE TABLE alunos (
    aluno_id character varying(5) NOT NULL,
    nome character varying(40) NOT NULL,
    endereco character varying(60),
    cidade character varying(15),
    estado character varying(15),
    cep character varying(10),
    pais character varying(15),
    telefone character varying(24)
);

INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone) VALUES
('A001', 'João Silva', 'Rua A, 123', 'São Paulo', 'SP', '01000-000', 'Brasil', '1111-1111'),
('A002', 'Maria Souza', 'Rua B, 456', 'Rio de Janeiro', 'RJ', '02000-000', 'Brasil', '2222-2222'),
('A003', 'Carlos Pereira', 'Rua C, 789', 'Belo Horizonte', 'MG', '03000-000', 'Brasil', '3333-3333'),
('A004', 'Ana Costa', 'Rua D, 1011', 'Porto Alegre', 'RS', '04000-000', 'Brasil', '4444-4444'),
('A005', 'Pedro Santos', 'Rua E, 1213', 'Curitiba', 'PR', '05000-000', 'Brasil', '5555-5555'),
('A006', 'Fernanda Lima', 'Rua F, 1415', 'Salvador', 'BA', '06000-000', 'Brasil', '6666-6666'),
('A007', 'Lucas Almeida', 'Rua G, 1617', 'Fortaleza', 'CE', '07000-000', 'Brasil', '7777-7777'),
('A008', 'Juliana Rodrigues', 'Rua H, 1819', 'Manaus', 'AM', '08000-000', 'Brasil', '8888-8888'),
('A009', 'Rafael Ferreira', 'Rua I, 2021', 'Recife', 'PE', '09000-000', 'Brasil', '9999-9999'),
('A010', 'Beatriz Oliveira', 'Rua J, 2223', 'Brasília', 'DF', '10000-000', 'Brasil','1010-1010');