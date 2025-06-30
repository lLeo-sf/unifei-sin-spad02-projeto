# API de Relatório Ad Hoc

## Visão Geral
Backend em FastAPI que expõe um endpoint `/search` e um `/metadata` para consultas Ad Hoc a tabelas e relações do banco carregado pelo ETL com filtros e agrupamentos dinâmicos.

## Tecnologias
- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- Uvicorn

## Pré-requisitos
- Python 3.10 ou superior
- PostgreSQL acessível (ex.: `postgresql://postgres:password@localhost:5432/database`)

## Instalação
1. Clone este repositório e entre na pasta `api`:
   ```bash
   cd api
   ```
2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary
   ```

## Execução em Desenvolvimento
```bash
uvicorn main:app --reload --host localhost --port 8000
```
A documentação interativa ficará disponível em `http://localhost:8000/docs`.

## Configuração
- Ajuste a variável `DATABASE_URL` em `model.py` conforme seu ambiente.
- Adicione outras origens CORS em `main.py` se necessário.

## Estrutura de Pastas
```
api/
  ├ controller.py     # Define rota /search
  ├ main.py           # Cria app FastAPI e middleware
  ├ model.py          # Modelos SQLAlchemy e geração de queries
  ├ schemas.py        # Pydantic request/response
  └ view.py           # Formatação da resposta
```