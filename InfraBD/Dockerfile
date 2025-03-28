# Use a imagem oficial do PostgreSQL
FROM postgres:latest

# Defina variáveis de ambiente para o PostgreSQL
ENV POSTGRES_DB escola
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres

# Copie o arquivo SQL para o contêiner
COPY escola.sql /docker-entrypoint-initdb.d/

# Exponha a porta padrão do PostgreSQL
EXPOSE 5432