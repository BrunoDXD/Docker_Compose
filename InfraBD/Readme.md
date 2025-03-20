# Construir a imagem
docker build -t minha-imagem-postgres .

# Executar o contêiner
docker run --name meu-container-postgres -d -p 5432:5432 minha-imagem-postgres