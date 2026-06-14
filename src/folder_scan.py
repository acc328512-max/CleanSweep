"""
folder_scan.py
==============
Scannt potentielle Programm-Orte auf ALLEN lokalen Festplatten.

Wir suchen NICHT blind jeden Ordner ab (das waere langsam und sinnlos -
deine Fotos sind keine Installation). Stattdessen scannen wir die Orte, an
denen Programme tatsaechlich liegen, und zwar auf jedem festen Laufwerk:

  * <Laufwerk>:\\Program Files
  * <Laufwerk>:\\Program Files (x86)
  * <Laufwerk>:\\            (oberste Ordner -> portable Apps, Spiele)
  * %LOCALAPPDATA%\\Programs
  * %LOCALAPPDATA%           (App-Daten)
  * %APPDATA%                (App-Daten, "Roaming")
  * %PROGRAMDATA%

Jeder gefundene Ordner bekommt eine "category", damit das Bewertungs-Modul
weiss, wie vorsichtig es sein muss (Laufwerk-Wurzel/AppData = vorsichtiger).

Dieses Modul AENDERT NICHTS - es liest nur Ordnernamen und Groessen.
"""

from __future__ import annotations

import ctypes
import os
import string
from dataclasses import dataclass
from pathlib import Path


# Windows-Konstante: ein "festes" Laufwerk (HDD/SSD), kein USB/Netzwerk/CD.
_DRIVE_FIXED = 3


def get_fixed_drives() -> list[Path]:
    """Liefert alle lokalen FESTEN Laufwerke (C:\\, D:\\ ...).

    Wir ueberspringen bewusst USB-Sticks, Netzlaufwerke und CD/DVD, denn dort
    Installationen aufzuraeumen ergibt keinen Sinn und ist riskant.
    """
    drives: list[Path] = []
    for letter in string.ascii_uppercase:
        root = f"{letter}:\\"
        try:
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(root)
        except OSError:
            continue
        if drive_type == _DRIVE_FIXED and os.path.isdir(root):
            drives.append(Path(root))
    return drives


@dataclass(frozen=True)
class ScanLocation:
    """Ein Ort, dessen direkte Unterordner wir als Kandidaten betrachten."""
    path: Path
    category: str   # z.B. "program_files", "drive_root", "appdata_local" ...


def get_scan_locations() -> list[ScanLocation]:
    """Stellt die Liste aller zu durchsuchenden Orte zusammen (nur existierende)."""
    locations: list[ScanLocation] = []
    seen: set[str] = set()

    def add(path_str: str, category: str) -> None:
        if not path_str:
            return
        p = Path(path_str)
        key = str(p).lower()
        if key in seen:
            return
        if p.is_dir():
            seen.add(key)
            locations.append(ScanLocation(p, category))

    # --- Pro Festplatte: Program Files + Laufwerks-Wurzel -----------------
    for drive in get_fixed_drives():
        add(str(drive / "Program Files"), "program_files")
        add(str(drive / "Program Files (x86)"), "program_files")
        # Oberste Ordner des Laufwerks (Spiele, portable Apps liegen oft hier).
        add(str(drive), "drive_root")

    # --- Benutzer- und Systemdaten ---------------------------------------
    local = os.environ.get("LOCALAPPDATA", "")
    roaming = os.environ.get("APPDATA", "")
    add(os.path.join(local, "Programs"), "user_programs")
    add(local, "appdata_local")
    add(roaming, "appdata_roaming")
    add(os.environ.get("PROGRAMDATA", r"C:\ProgramData"), "programdata")

    return locations


@dataclass
class FolderInfo:
    """Ein direkter Unterordner eines Scan-Ortes."""
    name: str            # Ordnername (z.B. "Google")
    path: Path           # voller Pfad
    size_bytes: int      # Gesamtgroesse inkl. aller Unterordner
    category: str        # Kategorie des Scan-Ortes (siehe ScanLocation)
    last_modified: float = 0.0  # neueste Aenderungszeit (Unix-Zeit) im Ordner


def _is_reparse_point(entry: os.DirEntry) -> bool:
    """True, wenn der Eintrag ein Symlink/Junction ist (nicht hineingehen!)."""
    try:
        attrs = entry.stat(follow_symlinks=False).st_file_attributes  # type: ignore[attr-defined]
        FILE_ATTRIBUTE_REPARSE_POINT = 0x400
        return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except (OSError, AttributeError):
        return False


def _folder_stats(path: Path) -> tuple[int, float]:
    """Berechnet Gesamtgroesse (Bytes) UND neueste Aenderungszeit eines Ordners.

    Beides in EINEM Durchlauf, um den teuren rekursiven Scan nicht zu
    verdoppeln. Robust gegen gesperrte Dateien; folgt keinen Symlinks/
    Junctions (sonst droht Endlosschleife oder Doppelzaehlung).
    """
    total = 0
    # Mit dem Aenderungsdatum des Ordners selbst starten, damit auch LEERE
    # Ordner (ohne Dateien) ein sinnvolles "zuletzt geaendert" bekommen.
    try:
        latest = path.stat().st_mtime
    except OSError:
        latest = 0.0
    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            if not _is_reparse_point(entry):
                                stack.append(Path(entry.path))
                        elif entry.is_file(follow_symlinks=False):
                            st = entry.stat(follow_symlinks=False)
                            total += st.st_size
                            if st.st_mtime > latest:
                                latest = st.st_mtime
                    except OSError:
                        continue
        except OSError:
            continue
    return total, latest


def scan_program_folders(compute_sizes: bool = True,
                         progress: bool = False) -> list[FolderInfo]:
    """Liefert alle direkten Unterordner aller Scan-Orte mit ihrer Groesse."""
    results: list[FolderInfo] = []
    locations = get_scan_locations()

    for loc in locations:
        if progress:
            print(f"      scanne {loc.path} ...")
        try:
            with os.scandir(loc.path) as it:
                for entry in it:
                    try:
                        if not entry.is_dir(follow_symlinks=False):
                            continue
                        if _is_reparse_point(entry):
                            continue
                    except OSError:
                        continue
                    folder_path = Path(entry.path)
                    if compute_sizes:
                        size, latest = _folder_stats(folder_path)
                    else:
                        size, latest = 0, 0.0
                    results.append(FolderInfo(
                        name=entry.name,
                        path=folder_path,
                        size_bytes=size,
                        category=loc.category,
                        last_modified=latest,
                    ))
        except OSError:
            continue
    return results


def human_size(num_bytes: int) -> str:
    """Wandelt Bytes in eine lesbare Form um (z.B. '1.4 GB')."""
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def age_days(last_modified: float) -> float:
    """Tage seit der letzten Aenderung. -1, wenn unbekannt."""
    import time
    if not last_modified:
        return -1.0
    return (time.time() - last_modified) / 86400.0


def human_age(last_modified: float) -> str:
    """Lesbares Alter der letzten Aenderung (z.B. 'vor 3 Tagen'), uebersetzbar."""
    from i18n import t
    days = age_days(last_modified)
    if days < 0:
        return t("unbekannt")
    if days < 1:
        return t("heute")
    if days < 30:
        return t("vor {n} Tagen").format(n=int(days))
    if days < 365:
        return t("vor {n} Monaten").format(n=int(days / 30))
    return t("vor {n} Jahren").format(n=f"{days / 365:.1f}")


if __name__ == "__main__":
    print("Feste Laufwerke:", ", ".join(str(d) for d in get_fixed_drives()))
    print("Scan-Orte:")
    for loc in get_scan_locations():
        print(f"  [{loc.category:16}] {loc.path}")
    print()
    folders = scan_program_folders(progress=True)
    folders.sort(key=lambda f: f.size_bytes, reverse=True)
    print(f"\nGefundene Ordner: {len(folders)}\n")
    for f in folders[:40]:
        print(f"  {human_size(f.size_bytes):>10}  [{f.category:14}]  {f.path}")
