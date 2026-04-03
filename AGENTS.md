# Atualizações Tracker - Guia para Agentes

## Visão Geral
Aplicação web para rastrear atualizações/futuras anotações com Flask + SQLite + Railway.

## Arquivos Principais
- `web_app.py` - App principal (deploy Railway)
- `utils.py` - Funções auxiliares de fuso horário

## Deploy no Render

1. Criar repositório no GitHub
2. Acessar [render.com](https://render.com) → New → Web Service
3. Conectar GitHub e selecionar o repositório
4. Configurar:
   - **Root Directory:** (vazio)
   - **Build Command:** (vazio - não usa build)
   - **Start Command:** `gunicorn web_app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free
5. Clicar em "Create Web Service"

Aguardar deploy (~1-2 minutos). URL será algo como: `https://atualizacoes-tracker.onrender.com`

## Funcionalidades
- Adicionar atualização/nota com título e descrição
- Marcar como feito ou pendente
- Filtrar por: Todas, Pendentes, Feitas
- Excluir atualizações
- Auto-refresh a cada 10 segundos
- Estatísticas (total, pendentes, feitas)

## Fuso Horário Brasil (UTC-3)
Todos os arquivos usam `timestamp_brasil()` para registrar datas no fuso correto.

## API Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | / | Interface web |
| GET | /api/atualizacoes | Lista todas |
| POST | /api/adicionar | Adicionar nova |
| POST | /api/toggle/<id> | Toggle feito/pendente |
| DELETE | /api/deletar/<id> | Deletar |

## Dependências
```
flask>=3.1.0
```
