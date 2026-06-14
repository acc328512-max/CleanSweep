"""
recycle_bin.py
==============
Fragt Groesse/Anzahl des Windows-Papierkorbs ab und leert ihn - ueber die
offizielle Windows-Shell-API (SHQueryRecycleBin / SHEmptyRecycleBin).

Wichtig: Wir verschieben in anderen Funktionen Dinge in den Papierkorb. Der
Platz wird aber erst frei, wenn der Papierkorb GELEERT wird. Genau das macht
dieses Modul - ueber alle Laufwerke hinweg.

Achtung: Leeren ist endgueltig (Inhalt des Papierkorbs ist danach weg).
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass


# Struktur fuer SHQueryRecycleBin.
class _SHQUERYRBINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("i64Size", ctypes.c_int64),
        ("i64NumItems", ctypes.c_int64),
    ]


# Flags fuer SHEmptyRecycleBin: ohne Rueckfrage, ohne Fortschrittsfenster,
# ohne Sound (die Rueckfrage uebernimmt unsere GUI).
_SHERB_NOCONFIRMATION = 0x00000001
_SHERB_NOPROGRESSUI = 0x00000002
_SHERB_NOSOUND = 0x00000004


@dataclass
class RecycleInfo:
    size_bytes: int
    num_items: int


def query_recycle_bin() -> RecycleInfo:
    """Liefert Gesamtgroesse und Anzahl der Objekte im Papierkorb (alle Laufwerke)."""
    info = _SHQUERYRBINFO()
    info.cbSize = ctypes.sizeof(_SHQUERYRBINFO)
    try:
        # pszRootPath = None  ->  ueber ALLE Laufwerke abfragen.
        rc = ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(info))
        if rc == 0:  # S_OK
            return RecycleInfo(int(info.i64Size), int(info.i64NumItems))
    except Exception:  # noqa: BLE001
        pass
    return RecycleInfo(0, 0)


def empty_recycle_bin() -> bool:
    """Leert den Papierkorb (alle Laufwerke), endgueltig. True bei Erfolg."""
    flags = _SHERB_NOCONFIRMATION | _SHERB_NOPROGRESSUI | _SHERB_NOSOUND
    try:
        rc = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
        # 0 = S_OK; einige Systeme liefern auch bei "schon leer" einen Fehlercode.
        return rc == 0
    except Exception:  # noqa: BLE001
        return False


if __name__ == "__main__":
    from folder_scan import human_size
    info = query_recycle_bin()
    print(f"Papierkorb: {human_size(info.size_bytes)} in {info.num_items} Objekten")
