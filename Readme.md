# Sistema de Gestão - Escola Infantil

Sistema completo de gestão para escola infantil com interface web, API REST documentada e monitoramento.

## 🚀 Tecnologias

- **Backend**: Flask + SQLAlchemy
- **Banco de Dados**: PostgreSQL
- **Documentação API**: Swagger/OpenAPI (Flask-RESTX)
- **Monitoramento**: Prometheus + Grafana
- **Containerização**: Docker + Docker Compose
- **Testes**: Pytest

## 📋 Funcionalidades

### Interface Web
- Dashboard com estatísticas
- Gestão de professores, turmas, alunos
- Controle de pagamentos e atividades
- Interface responsiva em português

### API REST
- CRUD completo para todas as entidades
- Documentação automática com Swagger
- Endpoints organizados por namespaces
- Validação de dados

### Monitoramento
- Métricas com Prometheus
- Dashboards no Grafana
- Logs estruturados com rotação
- Monitoramento do PostgreSQL

## 🏗️ Arquitetura

```
├── app/                    # Aplicação Flask
│   ├── templates/          # Templates HTML
│   ├── app.py             # Aplicação principal
│   ├── models.py          # Modelos do banco
│   └── config.py          # Configurações
├── grafana/               # Configuração Grafana
├── prometheus/            # Configuração Prometheus
├── InfraBD/              # Scripts do banco
└── docker-compose.yml    # Orquestração
```

## 🐳 Como Executar

### Pré-requisitos
- Docker Desktop instalado e rodando
- Git

### Execução
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd Docker_Compose

# Execute o projeto
docker-compose up -d

# Para reconstruir após mudanças
docker-compose up --build -d
```

## 🌐 Acessos

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **Interface Web** | http://localhost:5001 | - |
| **API Swagger** | http://localhost:5001/swagger/ | - |
| **Grafana** | http://localhost:3000 | admin/admin |
| **Prometheus** | http://localhost:9090 | - |
| **PostgreSQL** | localhost:5432 | postgres/postgres |

## 📊 Banco de Dados

### Entidades
- **Professores**: Dados pessoais e contato
- **Turmas**: Nome, professor responsável, horário
- **Alunos**: Dados pessoais, responsáveis, turma
- **Pagamentos**: Controle financeiro por aluno
- **Atividades**: Atividades pedagógicas
- **Presenças**: Controle de frequência

### Relacionamentos
- Professor → Turmas (1:N)
- Turma → Alunos (1:N)
- Aluno → Pagamentos (1:N)
- Atividade ↔ Alunos (N:N)

## 🔧 API Endpoints

### Professores
- `GET /professores/` - Lista professores
- `POST /professores/` - Cria professor
- `GET /professores/{id}` - Obtém professor
- `PUT /professores/{id}` - Atualiza professor
- `DELETE /professores/{id}` - Remove professor

### Turmas
- `GET /turmas/` - Lista turmas
- `POST /turmas/` - Cria turma
- `GET /turmas/{id}` - Obtém turma
- `PUT /turmas/{id}` - Atualiza turma
- `DELETE /turmas/{id}` - Remove turma

### Alunos
- `GET /alunos/` - Lista alunos
- `POST /alunos/` - Cria aluno
- `GET /alunos/{id}` - Obtém aluno
- `PUT /alunos/{id}` - Atualiza aluno
- `DELETE /alunos/{id}` - Remove aluno

### Pagamentos
- `GET /pagamentos/` - Lista pagamentos
- `POST /pagamentos/` - Cria pagamento
- `GET /pagamentos/{id}` - Obtém pagamento
- `PUT /pagamentos/{id}` - Atualiza pagamento
- `DELETE /pagamentos/{id}` - Remove pagamento

### Atividades
- `GET /atividades/` - Lista atividades
- `POST /atividades/` - Cria atividade
- `GET /atividades/{id}` - Obtém atividade
- `PUT /atividades/{id}` - Atualiza atividade
- `DELETE /atividades/{id}` - Remove atividade

## 📝 Exemplos de Uso

### Criar Professor
```bash
curl -X POST http://localhost:5001/professores/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "Maria Silva",
    "email": "maria@escola.com",
    "telefone": "(11) 99999-9999"
  }'
```

### Criar Turma
```bash
curl -X POST http://localhost:5001/turmas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_turma": "Maternal I",
    "id_professor": 1,
    "horario": "08:00-12:00"
  }'
```

## 🧪 Testes

```bash
# Executar testes
docker-compose run test

# Logs dos testes
docker-compose logs test
```

## 📈 Monitoramento

### Métricas Disponíveis
- Performance da aplicação Flask
- Métricas do PostgreSQL
- Uso de recursos do sistema
- Logs estruturados

### Dashboards Grafana
- Overview do sistema
- Métricas de banco de dados
- Performance da aplicação

## 🛠️ Comandos Úteis

```bash
# Ver logs da aplicação
docker-compose logs -f web

# Parar todos os serviços
docker-compose down

# Remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Reconstruir apenas um serviço
docker-compose up --build -d web

# Acessar container
docker-compose exec web bash
```

## 📁 Estrutura de Arquivos

```
Docker_Compose/
├── app/
│   ├── templates/          # Templates HTML
│   │   ├── index.html     # Dashboard principal
│   │   ├── professores.html
│   │   ├── turmas.html
│   │   ├── alunos.html
│   │   └── ...
│   ├── app.py             # Aplicação Flask principal
│   ├── models.py          # Modelos SQLAlchemy
│   ├── config.py          # Configurações
│   ├── requirements.txt   # Dependências Python
│   └── Dockerfile         # Container da aplicação
├── grafana/
│   ├── provisioning/      # Configurações automáticas
│   └── Dockerfile
├── prometheus/
│   ├── prometheus.yml     # Configuração do Prometheus
│   └── Dockerfile
├── InfraBD/
│   ├── escola.sql         # Script inicial do banco
│   └── Dockerfile
├── docker-compose.yml     # Orquestração dos serviços
└── README.md             # Este arquivo
```

## 🔒 Segurança

- Senhas em variáveis de ambiente
- Validação de entrada nos endpoints
- Logs de auditoria para operações CRUD
- Isolamento de rede entre containers

## 🚀 Deploy em Produção

### Variáveis de Ambiente
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
FLASK_ENV=production
SECRET_KEY=your-secret-key
```

### Considerações
- Use PostgreSQL externo em produção
- Configure backup automático
- Implemente autenticação/autorização
- Use HTTPS com certificado SSL
- Configure monitoramento de alertas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação da API em `/swagger/`
- Verifique os logs com `docker-compose logs`

---

**Desenvolvido com ❤️ para gestão educacional**