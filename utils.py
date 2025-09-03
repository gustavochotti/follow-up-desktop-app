# utils.py
import re
import datetime
import os
import sys

def _only_digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")

def format_ddmmyyyy_from_digits(s: str) -> str | None:
    digits = _only_digits(s)
    if len(digits) != 8:
        return None
    d, m, y = digits[0:2], digits[2:4], digits[4:8]
    try:
        _ = datetime.datetime(int(y), int(m), int(d))
        return f"{d}/{m}/{y}"
    except Exception:
        return None

def format_br_phone_from_digits(s: str) -> str | None:
    d = re.sub(r"\D", "", s or "")
    d = d[:11]
    if len(d) == 11: return f"({d[0:2]}) {d[2:7]}-{d[7:]}"
    if len(d) == 10: return f"({d[0:2]}) {d[2:6]}-{d[6:]}"
    if len(d) == 9: return f"{d[0:5]}-{d[5:]}"
    if len(d) == 8: return f"{d[0:4]}-{d[4:]}"
    return None

def normalize_money(s: str) -> str:
    s = (s or "").strip().replace("R$", "").replace(".", "").replace(",", ".")
    if not s: return ""
    try:
        val = float(s)
        return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return ""

def resource_path(relative_path: str) -> str:
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, "assets", relative_path)