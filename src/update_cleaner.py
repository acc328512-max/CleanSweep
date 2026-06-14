"""
update_cleaner.py
=================
Findet und bereinigt heruntergeladene Windows-Update-Pakete im Ordner
    C:\\Windows\\SoftwareDistribution\\Download

Nach der Installation eines Updates sind diese Pakete nutzlos und belegen
oft mehrere GB. Windows legt den Ordner bei Bedarf selbst neu an.

Besonderheiten:
  * Der Ordner liegt im Windows-Verzeichnis -> LOESCHEN braucht ADMIN-Rechte
    (Scannen/Groesse lesen geht meist auch ohne).
  * Sauber ist es, vorher die Dienste 'wuauserv' (Windows Update) und 'bits'
    zu stoppen und danach wieder zu starten, damit keine Dateien gesperrt sind.
  * Geloescht wird ENDGUELTIG (nicht in den Papierkorb) - sonst waere der
    Platz weiter belegt. Es sind reine Wegwerf-Daten.
"""

from __future__ import annotations

import ctypes
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


# Dienste, die vor dem Leeren gestoppt werden sollten.
_UPDATE_SERVICES = ["wuauserv", "bits"]

# Damit aufgerufene net.exe-Befehle kein schwarzes Fenster aufpoppen lassen.
_NO_WINDOW = 0x08000000  # CREATE_NO_WINDOW


def get_update_cache_path() -> Path:
    """Pfad zum Windows-Update-Download-Ordner."""
    sysroot = os.environ.get("SystemRoot", r"C:\Windows")
    return Path(sysroot) / "SoftwareDistribution" / "Download"


def is_admin() -> bool:
    """True, wenn das Programm mit Administrator-Rechten laeuft."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:  # noqa: BLE001
        return False


def relaunch_as_admin() -> bool:
    """Startet das aktuelle Programm neu - mit Administrator-Rechten.

    Zeigt die Windows-Abfrage zur Rechte-Erhoehung (UAC). Liefert True, wenn
    der Neustart angestossen wurde (der Aufrufer sollte sich dann beenden).
    """
    try:
        script = os.path.abspath(sys.argv[0])
        params = " ".join(f'"{a}"' for a in sys.argv[1:])
        # ShellExecuteW mit Verb 'runas' loest die UAC-Abfrage aus.
        rc = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        return rc > 32  # >32 = Erfolg laut WinAPI
    except Exception:  # noqa: BLE001
        return False


@dataclass
class UpdateCacheInfo:
    """Statistik zum Update-Cache."""
    path: Path
    exists: bool
    size_bytes: int
    file_count: int


def scan_update_cache() -> UpdateCacheInfo:
    """Ermittelt Groesse und Dateianzahl des Update-Caches (read-only)."""
    path = get_update_cache_path()
    if not path.is_dir():
        return UpdateCacheInfo(path, False, 0, 0)

    size, count = 0, 0
    for _p, st in _iter_files(path):
        size += st.st_size
        count += 1
    return UpdateCacheInfo(path, True, size, count)


def _iter_files(root: Path):
    """Geht rekursiv alle Dateien durch und liefert (Path, stat-Ergebnis)."""
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(Path(entry.path))
                        elif entry.is_file(follow_symlinks=False):
                            yield Path(entry.path), entry.stat(follow_symlinks=False)
                    except OSError:
                        continue
        except OSError:
            continue


def _run_service(action: str, name: str) -> bool:
    """Startet oder stoppt einen Windows-Dienst via 'net'. True bei Erfolg."""
    try:
        result = subprocess.run(
            ["net", action, name],
            capture_output=True, text=True, creationflags=_NO_WINDOW)
        return result.returncode == 0
    except Exception:  # noqa: BLE001
        return False


@dataclass
class UpdateCleanResult:
    """Ergebnis der Update-Cache-Bereinigung."""
    deleted_files: int
    freed_bytes: int
    skipped_files: int
    admin_required: bool        # True, wenn Admin-Rechte fehlten (nichts getan)
    services_stopped: bool      # konnten die Dienste gestoppt werden?


def clean_update_cache(manage_services: bool = True) -> UpdateCleanResult:
    """Leert den Update-Cache endgueltig (braucht ADMIN-Rechte).

    Stoppt optional die Update-Dienste vorher und startet sie danach wieder.
    Gesperrte Dateien werden uebersprungen.
    """
    if not is_admin():
        return UpdateCleanResult(0, 0, 0, admin_required=True,
                                 services_stopped=False)

    path = get_update_cache_path()
    if not path.is_dir():
        return UpdateCleanResult(0, 0, 0, False, False)

    # Dienste anhalten, damit keine Dateien in Benutzung sind.
    stopped = False
    if manage_services:
        stopped = all(_run_service("stop", s) for s in _UPDATE_SERVICES)

    deleted, freed, skipped = 0, 0, 0
    try:
        for file_path, st in _iter_files(path):
            try:
                size = st.st_size
                os.remove(file_path)
                deleted += 1
                freed += size
            except OSError:
                skipped += 1
        _remove_empty_dirs(path)
    finally:
        # Dienste in JEDEM Fall wieder starten (auch bei Fehlern dazwischen).
        if manage_services:
            for s in _UPDATE_SERVICES:
                _run_service("start", s)

    return UpdateCleanResult(deleted, freed, skipped, False, stopped)


def _remove_empty_dirs(root: Path) -> None:
    """Entfernt leere Unterordner (den root-Ordner selbst NICHT)."""
    for dirpath, _dirs, _files in os.walk(root, topdown=False):
        if Path(dirpath) == root:
            continue
        try:
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
        except OSError:
            continue


if __name__ == "__main__":
    from folder_scan import human_size
    info = scan_update_cache()
    print(f"Update-Cache: {info.path}")
    print(f"  existiert: {info.exists}")
    print(f"  Groesse:   {human_size(info.size_bytes)} ({info.file_count} Dateien)")
    print(f"  Admin:     {is_admin()}")
