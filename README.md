
## Tecnologias Utilizadas
- Framework: FastAPI
- Banco de Dados: PostgreSQL
- ORM: SQLAlchemy (com asyncio para operações assíncronas)
- Migrações: Alembic
- Validação de Dados: Pydantic
- Autenticação: JWT (JSON Web Tokens) com OAuth2
- Containerização: Docker e Docker Compose
- Servidor ASGI: Uvicorn
- Gerenciador de Pacotes: uv (ou pip com requirements.txt)

## Pré-requisitos
- Docker e Docker Compose
- Python (versão 3.10 ou superior)
- uv (opcional, mais recomendado para gerenciamento de dependências mais rápido)

## Guia de Instalação e Execução

1. Clone o Repositório
```
git clone <url_do_seu_repositorio>
cd <nome_do_seu_repositorio>
```
2. Inicie o Banco de Dados com Docker
```
docker compose up -d
O banco de dados estará acessível em localhost:5432.
```

4. Instale as Dependências
- Você pode usar uv (recomendado) ou pip.
. Com uv (Recomendado):
```
uv sync
```
2. Com pip:
```
pip install -r requirements.txt
```

3. Aplique as Migrações do Banco de Dados
Este comando utiliza o Alembic para criar todas as tabelas e relacionamentos no banco de dados que você iniciou com o Docker.
```
alembic upgrade head
```

5. Rode a Aplicação
Finalmente, inicie o servidor de desenvolvimento com Uvicorn. A flag --reload fará com que o servidor reinicie automaticamente após qualquer alteração no código.
```
uvicorn src.main:app --reload
```

Documentação da API (Auto-gerada)
O FastAPI gera automaticamente uma documentação interativa da API. Após iniciar a aplicação, acesse os seguintes links no seu navegador:
```
Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc
```
