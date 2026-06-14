"""
dism_cleanup.py
===============
Bereinigt den Windows-Komponentenspeicher (WinSxS) mit DISM.

Hintergrund:
Im Ordner C:\\Windows\\WinSxS sammeln sich nach Updates alte, durch neuere
ersetzte Komponenten an. Die Windows-Datenträgerbereinigung raeumt davon nur
einen Teil. 'DISM /StartComponentCleanup' geht gruendlicher vor - und mit der
zusaetzlichen Option '/ResetBase' werden auch alle ersetzten Versionen
endgueltig entfernt.

Wichtig:
  * Braucht ADMIN-Rechte.
  * '/ResetBase' bedeutet: bereits installierte Updates lassen sich danach
    NICHT mehr deinstallieren (Speicher gegen Flexibilitaet getauscht).
  * DISM kann einige Minuten laufen - daher in der GUI im Hintergrund-Thread.

Dieses Modul ruft nur das offizielle Windows-Werkzeug DISM auf.
"""

from __future__ import annotations

import re
import subprocess

from update_cleaner import is_admin   # gemeinsame Admin-Erkennung wiederverwenden

_NO_WINDOW = 0x08000000  # CREATE_NO_WINDOW (kein schwarzes Fenster)

_BASE = ["dism.exe", "/Online", "/Cleanup-Image"]


def _run_dism(extra: list[str]) -> tuple[bool, str]:
    """Fuehrt einen DISM-Befehl aus und liefert (Erfolg, Ausgabetext)."""
    if not is_admin():
        return False, "Administrator-Rechte noetig."
    try:
        result = subprocess.run(
            _BASE + extra,
            capture_output=True, text=True, errors="replace",
            creationflags=_NO_WINDOW)
        output = (result.stdout or "") + (result.stderr or "")
        return result.returncode == 0, output.strip()
    except FileNotFoundError:
        return False, "DISM wurde nicht gefunden."
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def analyze_component_store() -> tuple[bool, str]:
    """Analysiert den Komponentenspeicher und zeigt, was bereinigbar waere."""
    return _run_dism(["/AnalyzeComponentStore"])


def _extract_reclaimable_count(output: str) -> int | None:
    """Liest die Anzahl der bereinigbaren/ersetzten Pakete aus der Ausgabe.

    Diese Zahl ist die ehrliche Erfolgskennzahl - NICHT die "empfohlen"-Zeile
    (die steht schon bei 1 Paket auf "Ja"). Sprachunabhaengig per Stichwort.
    """
    keys = ("reclaimable", "bereinigbar", "wiederherstellbar")
    for line in output.splitlines():
        low = line.lower()
        if any(k in low for k in keys):
            m = re.search(r"(\d+)\s*$", line.strip())
            if m:
                return int(m.group(1))
    return None


def summarize_analysis(output: str) -> str:
    """Erzeugt eine klare BEWERTUNG aus der DISM-Analyse.

    Stuetzt sich auf die Anzahl bereinigbarer Pakete (nicht auf die
    "empfohlen"-Zeile, die fast immer "Ja" sagt). Zeigt zusaetzlich die
    relevanten Originalzeilen.
    """
    # Relevante Originalzeilen sammeln.
    keys = ("empfohlen", "recommended", "bereinigbar", "reclaimable",
            "wiederherstellbar")
    hits = []
    for line in output.splitlines():
        low = line.lower()
        if any(k in low for k in keys):
            cleaned = line.strip()
            if cleaned and cleaned not in hits:
                hits.append(cleaned)

    # Bewertung anhand der Paketanzahl.
    n = _extract_reclaimable_count(output)
    if n is None:
        verdict = ""
    elif n == 0:
        verdict = "BEWERTUNG: Komponentenspeicher ist sauber - nichts zu tun.\n"
    elif n <= 5:
        verdict = (f"BEWERTUNG: Nur {n} ersetzte(s) Paket(e) - das ist auf einem "
                   f"aktuellen Windows normal und gesund.\n"
                   f"Hinweis: DISM zeigt 'empfohlen: Ja' schon ab 1 Paket - das "
                   f"heisst NICHT, dass die Bereinigung fehlschlug.\n")
    else:
        verdict = (f"BEWERTUNG: {n} ersetzte Pakete - eine Bereinigung lohnt "
                   f"sich noch.\n")

    if not verdict and not hits:
        return ""
    block = verdict
    if hits:
        block += "\n".join("  " + h for h in hits) + "\n"
    return block + "-" * 50 + "\n\n"


def start_component_cleanup(reset_base: bool = False) -> tuple[bool, str]:
    """Bereinigt den Komponentenspeicher. reset_base=True entfernt auch
    ersetzte Update-Versionen endgueltig (dann keine Update-Deinstallation mehr).
    """
    extra = ["/StartComponentCleanup"]
    if reset_base:
        extra.append("/ResetBase")
    return _run_dism(extra)


if __name__ == "__main__":
    print("Admin:", is_admin())
    ok, out = analyze_component_store()
    print("Analyse erfolgreich:", ok)
    print(out)
