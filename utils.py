from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

try:
    FUSO_BRASIL = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BRASIL = timezone(timedelta(hours=-3))

def agora_brasil():
    return datetime.now(FUSO_BRASIL)

def data_brasil():
    return agora_brasil().date()

def timestamp_brasil():
    return agora_brasil()
