"""
temp_cleaner.py
===============
Findet und bereinigt temporaere Dateien (Temp-Ordner).

Anders als bei verwaisten Programm-Ordnern loeschen wir Temp-Dateien
ENDGUELTIG (nicht in den Papierkorb): Der Zweck ist, Platz freizugeben -
im Papierkorb waere der Platz noch belegt. Temp-Dateien sind ohnehin
Wegwerf-Daten; Windows raeumt sie selbst auf.

Sicherheit:
  * gesperrte / gerade benutzte Dateien werden uebersprungen (nicht erzwungen)
  * optional nur Dateien aelter als X Tage loeschen
  * der Temp-Ordner selbst bleibt bestehen, nur sein Inhalt wird geleert
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path


def get_temp_locations() -> list[Path]:
    """Liefert die zu bereinigenden Temp-Ordner (nur existierende, ohne Doppel)."""
    candidates = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Temp"),
    ]
    locations: list[Path] = []
    seen: set[str] = set()
    for c in candidates:
        if not c:
            continue
        p = Path(c)
        key = str(p).lower()
        if key not in seen and p.is_dir():
            seen.add(key)
            locations.append(p)
    return locations


@dataclass
class TempLocation:
    """Ein Temp-Ordner mit Statistik."""
    path: Path
    size_bytes: int
    file_count: int


def scan_temp() -> list[TempLocation]:
    """Ermittelt Groesse und Dateianzahl je Temp-Ordner (read-only)."""
    results: list[TempLocation] = []
    for loc in get_temp_locations():
        size, count = 0, 0
        for _path, st in _iter_files(loc):
            size += st.st_size
            count += 1
        results.append(TempLocation(loc, size, count))
    return results


def _iter_files(root: Path):
    """Geht rekursiv alle Dateien durch und liefert (Path, stat).

    Folgt keinen Symlinks/Junctions und ignoriert gesperrte Eintraege.
    """
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


@dataclass
class TempCleanResult:
    """Ergebnis einer Temp-Bereinigung."""
    deleted_files: int
    freed_bytes: int
    skipped_files: int      # gesperrt / in Benutzung / zu jung


def clean_temp(min_age_days: float = 0.0) -> TempCleanResult:
    """Loescht Temp-Dateien endgueltig (gesperrte werden uebersprungen).

    min_age_days: nur Dateien loeschen, die seit so vielen Tagen unveraendert
    sind (0 = alle). Schuetzt Dateien, die gerade frisch angelegt wurden.
    """
    now = time.time()
    deleted, freed, skipped = 0, 0, 0
    cutoff = min_age_days * 86400.0

    for loc in get_temp_locations():
        for path, st in _iter_files(loc):
            if cutoff and (now - st.st_mtime) < cutoff:
                skipped += 1
                continue
            try:
                size = st.st_size
                os.remove(path)
                deleted += 1
                freed += size
            except OSError:
                skipped += 1  # gesperrt / in Benutzung -> in Ruhe lassen
        _remove_empty_dirs(loc)

    return TempCleanResult(deleted, freed, skipped)


def _remove_empty_dirs(root: Path) -> None:
    """Entfernt leere Unterordner (den root-Ordner selbst NICHT)."""
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if Path(dirpath) == root:
            continue
        try:
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
        except OSError:
            continue


if __name__ == "__main__":
    from folder_scan import human_size
    locs = scan_temp()
    total = sum(l.size_bytes for l in locs)
    print(f"Temp-Ordner ({human_size(total)} gesamt):\n")
    for l in locs:
        print(f"  {human_size(l.size_bytes):>10}  {l.file_count:>6} Dateien  {l.path}")
