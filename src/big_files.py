"""
big_files.py
============
Findet die groessten Einzeldateien auf allen festen Laufwerken.

Das ergaenzt den Ordner-Scan: oft liegt der meiste Platz in einzelnen
riesigen Dateien (alte Videos, ISO-Abbilder, Backups), die ein
Programm-Ordner-Scan gar nicht zeigt.

Read-only: dieses Modul findet und meldet nur. Das Loeschen ausgewaehlter
Dateien laeuft - wie bei den Ordnern - ueber den Papierkorb (cleaner-Logik),
mit einer eigenen Sicherheitspruefung gegen System-Dateien.
"""

from __future__ import annotations

import heapq
import os
import time
from dataclasses import dataclass
from pathlib import Path

from folder_scan import get_fixed_drives, _is_reparse_point


@dataclass
class BigFile:
    """Eine grosse Datei."""
    path: Path
    size_bytes: int
    last_modified: float


# Ordner, die wir beim Suchen ueberspringen (System / sinnlos zu loeschen).
_SKIP_DIR_NAMES = {
    "windows", "$recycle.bin", "system volume information",
    "windowsapps", "winsxs",
}


def find_large_files(top_n: int = 50,
                     min_size_bytes: int = 100_000_000,  # 100 MB
                     min_age_days: float = 0.0,
                     progress=None) -> list[BigFile]:
    """Liefert die groessten Dateien (>= min_size_bytes) ueber alle Platten.

    top_n: wie viele der groessten Dateien zurueckgeben.
    min_age_days: nur Dateien, die seit so vielen Tagen NICHT mehr veraendert
                  wurden (0 = kein Filter).
    progress: optionale Callback-Funktion progress(pfad_str) fuer Statusanzeige.
    """
    # Min-Heap mit (size, laufende_nummer, BigFile); wir halten nur top_n.
    heap: list[tuple[int, int, BigFile]] = []
    counter = 0
    cutoff = min_age_days * 86400.0
    now = time.time()

    for drive in get_fixed_drives():
        if progress:
            progress(f"durchsuche {drive} ...")
        for path, st in _iter_all_files(drive):
            size = st.st_size
            if size < min_size_bytes:
                continue
            if cutoff and (now - st.st_mtime) < cutoff:
                continue  # zu kuerzlich genutzt -> ueberspringen
            counter += 1
            bf = BigFile(path, size, st.st_mtime)
            if len(heap) < top_n:
                heapq.heappush(heap, (size, counter, bf))
            elif size > heap[0][0]:
                heapq.heapreplace(heap, (size, counter, bf))

    # Groesste zuerst.
    largest = [item[2] for item in heap]
    largest.sort(key=lambda b: b.size_bytes, reverse=True)
    return largest


def _iter_all_files(root: Path):
    """Geht rekursiv ALLE Dateien eines Laufwerks durch (robust, ohne Symlinks).

    Ueberspringt bekannte System-Ordner, um Zeit zu sparen und keine
    Systemdateien vorzuschlagen.
    """
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            if _is_reparse_point(entry):
                                continue
                            if entry.name.lower() in _SKIP_DIR_NAMES:
                                continue
                            stack.append(Path(entry.path))
                        elif entry.is_file(follow_symlinks=False):
                            yield Path(entry.path), entry.stat(follow_symlinks=False)
                    except OSError:
                        continue
        except OSError:
            continue


def is_safe_to_delete_file(path: Path) -> tuple[bool, str]:
    """Sicherheitspruefung fuer das Loeschen einer EINZELNEN grossen Datei."""
    if not path.exists() or not path.is_file():
        return False, "Datei existiert nicht (mehr)"

    norm = str(path).lower()
    sysroot = os.environ.get("SystemRoot", r"C:\Windows").lower()
    if norm.startswith(sysroot):
        return False, "Liegt im Windows-Systemordner"

    # Typische, niemals zu loeschende System-/Auslagerungsdateien.
    forbidden_names = {"pagefile.sys", "hiberfil.sys", "swapfile.sys",
                       "ntuser.dat", "bootmgr"}
    if path.name.lower() in forbidden_names:
        return False, "System-/Auslagerungsdatei"

    return True, ""


if __name__ == "__main__":
    from folder_scan import human_size, human_age
    print("Suche groesste Dateien (>= 100 MB) ... das dauert.")
    files = find_large_files(top_n=30, progress=print)
    print(f"\nDie {len(files)} groessten Dateien:\n")
    for f in files:
        print(f"  {human_size(f.size_bytes):>10}  {human_age(f.last_modified):>14}  {f.path}")
