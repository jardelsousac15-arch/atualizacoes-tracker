# Atualizações Tracker - Guia para Agentes

## Visão Geral
Aplicação web para rastrear atualizações/futuras anotações com Flask + SQLite + Railway.

## Arquivos Principais
- `web_app.py` - App principal (deploy Railway)
- `utils.py` - Funções auxiliares de fuso horário

## Deploy
```bash
cd C:\Users\jarde\Documents\.agent\skills\skills\atualizacoes-tracker
"C:\Program Files\Git\cmd\git.exe" init
"C:\Program Files\Git\cmd\git.exe" add -A
"C:\Program Files\Git\cmd\git.exe" commit -m "primeiro commit"
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/SEU_USUARIO/atualizacoes-tracker.git
"C:\Program Files\Git\cmd\git.exe" push -u origin main
```
Conectar o repositório no Railway e fazer deploy automático.

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
