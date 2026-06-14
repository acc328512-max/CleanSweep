"""
cleaner.py
==========
Das Loesch-Modul (Phase 2). Verschiebt Ordner in den PAPIERKORB - niemals
echtes/endgueltiges Loeschen. Damit ist jede Aktion umkehrbar.

SICHERHEIT (Defense-in-Depth):
Dieses Modul VERTRAUT dem Orphan-Finder NICHT blind. Vor jeder Loeschung
laeuft eine eigene, unabhaengige Pruefung `is_safe_to_delete()`, die
System-Ordner, Laufwerks-Wurzeln und die Scan-Wurzeln selbst kategorisch
ablehnt. Selbst wenn der Finder sich irrt, kann hier nichts Kritisches
geloescht werden.

Jede Loeschung wird ausserdem protokolliert.
"""

from __future__ import annotations

import datetime
import os
from dataclasses import dataclass
from pathlib import Path

from send2trash import send2trash

from folder_scan import (
    get_scan_locations, get_fixed_drives, FolderInfo, human_size,
)
from orphan_finder import _is_protected, OrphanCandidate


# Standard-Pfad fuer das Loesch-Protokoll (neben dem Projekt).
DEFAULT_LOG = Path(__file__).resolve().parent.parent / "cleansweep_loeschungen.log"


def _never_delete_paths() -> set[str]:
    """Baut die Menge von Pfaden, die NIEMALS geloescht werden duerfen.

    Das sind: alle Laufwerks-Wurzeln, alle Scan-Wurzeln selbst (z.B.
    'C:\\Program Files') sowie zentrale Windows-Systemordner.
    """
    forbidden: set[str] = set()

    for drive in get_fixed_drives():
        forbidden.add(str(drive).rstrip("\\").lower())

    for loc in get_scan_locations():
        forbidden.add(str(loc.path).rstrip("\\").lower())

    # Zentrale Systemordner ausdruecklich sperren.
    sysroot = os.environ.get("SystemRoot", r"C:\Windows")
    userprofile = os.environ.get("USERPROFILE", "")
    systemdrive = os.environ.get("SystemDrive", "C:")
    extra = [
        sysroot,
        userprofile,
        os.path.join(systemdrive + "\\", "Users"),
        os.path.join(systemdrive + "\\", "ProgramData"),
        os.path.join(systemdrive + "\\", "Program Files"),
        os.path.join(systemdrive + "\\", "Program Files (x86)"),
    ]
    for e in extra:
        if e:
            forbidden.add(e.rstrip("\\").lower())

    return forbidden


def is_safe_to_delete(folder: FolderInfo) -> tuple[bool, str]:
    """Unabhaengige Sicherheitspruefung VOR dem Loeschen.

    Liefert (True, "") wenn das Loeschen erlaubt ist, sonst
    (False, Begruendung). Sehr konservativ - im Zweifel: nein.
    """
    path = folder.path
    norm = str(path).rstrip("\\").lower()

    # 1) Existiert der Ordner ueberhaupt (noch)?
    if not path.exists():
        return False, "Pfad existiert nicht (mehr)"

    if not path.is_dir():
        return False, "Kein Ordner"

    # 2) Auf der Verbotsliste (Laufwerks-Wurzel, Scan-Wurzel, Systemordner)?
    if norm in _never_delete_paths():
        return False, "Geschuetzter System-/Wurzelordner"

    # 3) Zu "flach"? Ein Pfad wie 'C:\\' oder 'C:\\Foo' direkt unter der
    #    Wurzel ist erlaubt (drive_root-Kandidat), aber niemals die Wurzel
    #    selbst. Path('C:\\').parts == ('C:\\',) -> Laenge 1 = Wurzel.
    if len(path.parts) < 2:
        return False, "Das ist eine Laufwerks-Wurzel"

    # 4) Liegt der Ordner innerhalb eines Windows-Systemordners?
    sysroot = os.environ.get("SystemRoot", r"C:\Windows").rstrip("\\").lower()
    if norm == sysroot or norm.startswith(sysroot + "\\"):
        return False, "Liegt im Windows-Systemordner"

    # 5) Greift die Schutzliste aus dem Orphan-Finder? (doppelte Absicherung)
    if _is_protected(folder):
        return False, "Steht auf der Schutzliste (geschuetzter Name)"

    return True, ""


@dataclass
class DeleteResult:
    """Ergebnis einer einzelnen Loesch-Aktion."""
    path: Path
    size_bytes: int
    success: bool
    message: str


def move_to_trash(folder: FolderInfo, log_path: Path = DEFAULT_LOG) -> DeleteResult:
    """Verschiebt EINEN Ordner in den Papierkorb - mit Sicherheitspruefung.

    Loescht niemals endgueltig. Protokolliert das Ergebnis.
    """
    safe, reason = is_safe_to_delete(folder)
    if not safe:
        result = DeleteResult(folder.path, folder.size_bytes, False,
                              f"ABGELEHNT: {reason}")
        _write_log(log_path, result)
        return result

    try:
        # send2trash erwartet einen normalen Pfad-String.
        send2trash(str(folder.path))
        result = DeleteResult(folder.path, folder.size_bytes, True,
                              "in Papierkorb verschoben")
    except Exception as exc:  # noqa: BLE001 - wir wollen jede Ursache loggen
        result = DeleteResult(folder.path, folder.size_bytes, False,
                              f"FEHLER: {exc}")

    _write_log(log_path, result)
    return result


def _write_log(log_path: Path, result: DeleteResult) -> None:
    """Schreibt eine Zeile ins Loesch-Protokoll (best effort)."""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (f"{stamp}\t{'OK ' if result.success else 'NEIN'}\t"
            f"{human_size(result.size_bytes):>10}\t{result.path}\t"
            f"{result.message}\n")
    try:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(line)
    except OSError:
        pass  # Logging-Fehler darf den Ablauf nicht stoppen.


def trash_path(path: Path, size_bytes: int = 0,
               log_path: Path = DEFAULT_LOG) -> DeleteResult:
    """Verschiebt einen beliebigen Pfad (Datei ODER Ordner) in den Papierkorb.

    Ohne eigene Sicherheitspruefung - der Aufrufer ist dafuer verantwortlich
    (z.B. big_files.is_safe_to_delete_file fuer einzelne Dateien). Loggt das
    Ergebnis. Loescht niemals endgueltig.
    """
    try:
        send2trash(str(path))
        result = DeleteResult(path, size_bytes, True, "in Papierkorb verschoben")
    except Exception as exc:  # noqa: BLE001
        result = DeleteResult(path, size_bytes, False, f"FEHLER: {exc}")
    _write_log(log_path, result)
    return result


def delete_candidates(candidates: list[OrphanCandidate],
                      log_path: Path = DEFAULT_LOG) -> list[DeleteResult]:
    """Verschiebt eine Liste von Kandidaten in den Papierkorb."""
    results: list[DeleteResult] = []
    for cand in candidates:
        results.append(move_to_trash(cand.folder, log_path=log_path))
    return results


if __name__ == "__main__":
    # Sicherheits-Selbsttest (ohne echte Kandidaten anzufassen!):
    # Wir pruefen, dass kritische Pfade zuverlaessig ABGELEHNT werden.
    from folder_scan import FolderInfo as FI

    print("Verbotsliste (Auszug):")
    for p in sorted(_never_delete_paths())[:15]:
        print("   ", p)

    tests = [
        FI("Windows", Path(os.environ.get("SystemRoot", r"C:\Windows")), 0, "drive_root"),
        FI("Program Files", Path(r"C:\Program Files"), 0, "program_files"),
        FI("C-Wurzel", Path("C:\\"), 0, "drive_root"),
        FI("Users", Path(r"C:\Users"), 0, "drive_root"),
    ]
    print("\nSicherheitspruefung kritischer Pfade (alle muessen NEIN sein):")
    for f in tests:
        ok, reason = is_safe_to_delete(f)
        print(f"   {f.path}  ->  {'ERLAUBT (!!)' if ok else 'abgelehnt'}: {reason}")
