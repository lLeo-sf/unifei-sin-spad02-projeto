# Relatório Ad Hoc

## Visão Geral
Este é o frontend em React de um gerador de relatórios Ad Hoc, consumindo uma API em Python para consultas dinâmicas a um banco PostgreSQL.

## Tecnologias
- React 18 (Create React App)
- Axios

## Pré-requisitos
- Node.js ≥ 14
- npm ≥ 6

## Instalação
1. Clone este repositório e navegue até a pasta do app:
   ```bash
   cd app/relatorio-ad-hoc
   ```
2. Instale as dependências (use a flag para evitar conflitos de peer-deps):
   ```bash
   npm install --legacy-peer-deps
   ```

## Execução em Desenvolvimento
```bash
npm start
```
O servidor rodará em `http://localhost:3000/` por padrão.

## Build para Produção
```bash
npm run build
```
Os arquivos finais ficarão em `build/`.

## Estrutura de Pastas
```
public/          # HTML e assets estáticos
src/
  ├── components/   # UI (DropArea, FilterSection, etc.)
  ├── services/     # axiosClient, metadataService, searchService
  ├── App.js        # Componente raiz
  └── index.js      # Entry point
```

## Configuração
- A API deve estar rodando em `http://localhost:8000` (padrão do backend).
- Caso mude porta ou host, atualize `axiosClient.js`.

