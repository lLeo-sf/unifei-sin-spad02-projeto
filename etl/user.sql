-- CRIAR USUÁRIOS
CREATE USER rescue_admin WITH PASSWORD 'senha_admin_super_segura';
CREATE USER rescue_org WITH PASSWORD 'senha_org_segura';
CREATE USER rescue_viewer WITH PASSWORD 'senha_view_apenas';

-- PERMISSÕES BÁSICAS
GRANT CONNECT ON DATABASE rescue_db TO rescue_admin, rescue_org, rescue_viewer;
GRANT USAGE ON SCHEMA public TO rescue_admin, rescue_org, rescue_viewer;

-- ADMIN: todas as permissões
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rescue_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO rescue_admin;

-- ORG: inserção e atualização (sem exclusão)
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO rescue_org;

-- VIEWER: somente leitura
GRANT SELECT ON ALL TABLES IN SCHEMA public TO rescue_viewer;

-- PERMISSÕES FUTURAS
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO rescue_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE ON TABLES TO rescue_org;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO rescue_viewer;

-- SEQUÊNCIAS (caso use SERIAL ou IDENTITY)
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO rescue_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO rescue_org;
