"""
windows_old.py
==============
Erkennt den Ordner C:\\Windows.old (Reste eines Windows-Upgrades) und startet
die offizielle Windows-Datenträgerbereinigung, um ihn zu entfernen.

WARUM nicht einfach loeschen?
  Windows.old gehoert dem System-Konto 'TrustedInstaller'. Ein normales
  Loeschen scheitert daher an einer Sperre - selbst als Administrator.
  Der unterstuetzte, sichere Weg ist die Datenträgerbereinigung (cleanmgr)
  bzw. die Speicher-Einstellungen. Genau das stossen wir hier an.

Dieses Modul loescht NICHTS selbst - es misst nur und startet das
Windows-Werkzeug, das die noetigen Rechte hat.
"""

from __future__ import annotations

import ctypes
import os
import subprocess
from pathlib import Path


def get_windows_old_path() -> Path | None:
    """Liefert den Pfad zu Windows.old, falls vorhanden - sonst None."""
    drive = os.environ.get("SystemDrive", "C:")
    path = Path(drive + "\\") / "Windows.old"
    return path if path.is_dir() else None


def scan_windows_old() -> tuple[bool, int]:
    """Prueft, ob Windows.old existiert, und schaetzt seine Groesse (Bytes).

    Manche Dateien sind durch Rechte gesperrt; die werden uebersprungen,
    die Groesse kann daher leicht zu niedrig sein.
    """
    path = get_windows_old_path()
    if path is None:
        return False, 0

    total = 0
    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(Path(entry.path))
                        elif entry.is_file(follow_symlinks=False):
                            total += entry.stat(follow_symlinks=False).st_size
                    except OSError:
                        continue
        except OSError:
            continue
    return True, total


def launch_disk_cleanup() -> bool:
    """Startet die Windows-Datenträgerbereinigung (cleanmgr) mit Admin-Rechten.

    Dort kann der Punkt 'Vorherige Windows-Installation(en)' angehakt werden,
    um Windows.old sicher zu entfernen. Liefert True, wenn der Start gelang.
    """
    try:
        # 'runas' loest die UAC-Abfrage aus und startet cleanmgr erhoeht,
        # sodass die System-Eintraege (inkl. Windows.old) sichtbar sind.
        rc = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "cleanmgr.exe", None, None, 1)
        return rc > 32
    except Exception:  # noqa: BLE001
        return False


def open_storage_settings() -> bool:
    """Oeffnet alternativ die Windows-Speicher-Einstellungen."""
    try:
        subprocess.Popen(["explorer", "ms-settings:storagesense"])
        return True
    except Exception:  # noqa: BLE001
        return False


if __name__ == "__main__":
    from folder_scan import human_size
    exists, size = scan_windows_old()
    if exists:
        print(f"Windows.old gefunden: {human_size(size)}")
        print(f"  Pfad: {get_windows_old_path()}")
        print("  Entfernen ueber: Datenträgerbereinigung (cleanmgr) ->")
        print("  'Vorherige Windows-Installation(en)' anhaken.")
    else:
        print("Kein Windows.old vorhanden.")
