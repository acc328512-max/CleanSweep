"""
hibernation.py
==============
Zeigt den Status des Ruhezustands und kann ihn ab-/anschalten.

Windows legt fuer den Ruhezustand (und den "Schnellstart") die Datei
C:\\hiberfil.sys an - so gross wie der Arbeitsspeicher, also oft 8-32 GB.
Mit 'powercfg /h off' wird der Ruhezustand abgeschaltet und die Datei
geloescht. Das gibt sofort viel Platz frei.

KOMPROMISS: Danach gibt es keinen Ruhezustand und keinen "Schnellstart"
mehr (der PC faehrt minimal langsamer hoch). Jederzeit mit 'powercfg /h on'
umkehrbar. Beide Befehle brauchen ADMIN-Rechte.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_NO_WINDOW = 0x08000000  # CREATE_NO_WINDOW


def get_hiberfile_path() -> Path:
    drive = os.environ.get("SystemDrive", "C:")
    return Path(drive + "\\") / "hiberfil.sys"


def hibernation_enabled() -> bool:
    """True, wenn der Ruhezustand aktiv ist (hiberfil.sys existiert)."""
    try:
        return get_hiberfile_path().exists()
    except OSError:
        return False


def hiberfile_size() -> int:
    """Groesse von hiberfil.sys in Bytes (0, wenn nicht vorhanden/lesbar)."""
    try:
        return get_hiberfile_path().stat().st_size
    except OSError:
        return 0


def _powercfg(switch: str) -> tuple[bool, str]:
    """Fuehrt 'powercfg /h <switch>' aus. Liefert (Erfolg, Meldung)."""
    try:
        result = subprocess.run(
            ["powercfg", "/h", switch],
            capture_output=True, text=True, creationflags=_NO_WINDOW)
        if result.returncode == 0:
            return True, "ok"
        msg = (result.stderr or result.stdout or "").strip()
        return False, msg or f"powercfg gab Code {result.returncode} zurueck"
    except FileNotFoundError:
        return False, "powercfg nicht gefunden"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def disable_hibernation() -> tuple[bool, str]:
    """Schaltet den Ruhezustand ab und loescht hiberfil.sys (braucht Admin)."""
    return _powercfg("off")


def enable_hibernation() -> tuple[bool, str]:
    """Schaltet den Ruhezustand wieder ein (braucht Admin)."""
    return _powercfg("on")


if __name__ == "__main__":
    from folder_scan import human_size
    if hibernation_enabled():
        print(f"Ruhezustand: AKTIV  (hiberfil.sys: {human_size(hiberfile_size())})")
    else:
        print("Ruhezustand: AUS (keine hiberfil.sys)")
