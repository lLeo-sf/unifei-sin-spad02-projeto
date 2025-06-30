# ETL RescueGroups

## Visão Geral
Script Python que consome a RescueGroups API v5 e popula um banco PostgreSQL com dados de animais e organizações, além de criar views e triggers.

## Tecnologias
- Python 3.10+
- requests
- psycopg2

## Pré-requisitos
- Python 3.10 ou superior
- PostgreSQL em `localhost:5432`
- Banco `rescue` criado
- Usuário e senha ajustados em `etl/etl.py`

## Instalação
1. Clone este repositório e navegue até a pasta `etl`:
   ```bash
   cd etl
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install requests psycopg2-binary
   ```

## Configuração
- No `etl/etl.py`, edite o dicionário `DB_CONFIG` com suas credenciais.
- Ajuste `API_URL` e `HEADERS` (chave de API RescueGroups).

## Preparação do Banco
Execute na ordem:
```sql
\i user.sql
\i indices.sql
\i trigger.sql
\i "view animal_available.sql"
\i "view orgs_basic_info.sql"
```

## Execução
```bash
python etl.py
```
Isso criará tabelas e fará insert paginado de animais e organizações.

## Estrutura de Pastas
```
etl/
  ├ etl.py                    # Script principal
  ├ user.sql                  # Criação de usuário/roles
  ├ indices.sql               # Índices para performance
  ├ trigger.sql               # Triggers e funções associadas
  ├ view animal_available.sql # View de animais disponíveis
  └ view orgs_basic_info.sql  # View de informações básicas de organizações
```
