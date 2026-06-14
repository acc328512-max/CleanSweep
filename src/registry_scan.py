"""
registry_scan.py
================
Liest die offiziell installierten Programme aus der Windows-Registry.

Windows merkt sich jedes ordentlich installierte Programm in sogenannten
"Uninstall"-Schluesseln der Registry. Genau dort schauen wir nach.

Es gibt drei relevante Orte:
  * HKLM 64-Bit : SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall
  * HKLM 32-Bit : SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall
  * HKCU        : (gleicher Pfad, aber nur fuer den aktuellen Benutzer)

Dieses Modul AENDERT NICHTS - es liest nur.
"""

from __future__ import annotations

import winreg
from dataclasses import dataclass, field


# Die Registry-Pfade, an denen Windows installierte Programme auflistet.
# (root_key, unterpfad, beschreibung)
UNINSTALL_LOCATIONS = [
    (winreg.HKEY_LOCAL_MACHINE,
     r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
     "HKLM-64bit"),
    (winreg.HKEY_LOCAL_MACHINE,
     r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
     "HKLM-32bit"),
    (winreg.HKEY_CURRENT_USER,
     r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
     "HKCU"),
]


@dataclass
class InstalledProgram:
    """Ein einzelnes, laut Registry installiertes Programm."""
    name: str                       # DisplayName
    publisher: str = ""             # Hersteller
    version: str = ""               # DisplayVersion
    install_location: str = ""      # InstallLocation (Ordner, falls angegeben)
    uninstall_string: str = ""      # Befehl zum Deinstallieren
    source: str = ""                # aus welchem Registry-Ort er stammt
    registry_key: str = ""          # voller Schluesselname (zur Nachverfolgung)


def _read_value(handle, value_name: str) -> str:
    """Liest einen einzelnen Wert aus einem geoeffneten Registry-Schluessel.

    Gibt einen leeren String zurueck, wenn der Wert nicht existiert -
    so muessen wir uns nicht ueberall um Ausnahmen kuemmern.
    """
    try:
        value, _ = winreg.QueryValueEx(handle, value_name)
        return str(value) if value is not None else ""
    except FileNotFoundError:
        return ""
    except OSError:
        return ""


def _read_programs_from(root_key, sub_path: str, source: str) -> list[InstalledProgram]:
    """Liest alle Programme aus EINEM Registry-Ort."""
    programs: list[InstalledProgram] = []

    try:
        base = winreg.OpenKey(root_key, sub_path)
    except FileNotFoundError:
        # Dieser Pfad existiert auf diesem System nicht - das ist ok.
        return programs

    with base:
        # Wie viele Unterschluessel gibt es? (jeder = ein Programm-Eintrag)
        sub_count = winreg.QueryInfoKey(base)[0]

        for i in range(sub_count):
            try:
                sub_name = winreg.EnumKey(base, i)
            except OSError:
                continue

            try:
                with winreg.OpenKey(base, sub_name) as item:
                    name = _read_value(item, "DisplayName")

                    # Eintraege ohne Namen sind fuer uns nutzlos -> ueberspringen.
                    if not name:
                        continue

                    # Updates/Hotfixes wollen wir nicht als "Programm" zaehlen.
                    system_component = _read_value(item, "SystemComponent")
                    if system_component == "1":
                        continue

                    programs.append(InstalledProgram(
                        name=name,
                        publisher=_read_value(item, "Publisher"),
                        version=_read_value(item, "DisplayVersion"),
                        install_location=_read_value(item, "InstallLocation"),
                        uninstall_string=_read_value(item, "UninstallString"),
                        source=source,
                        registry_key=f"{sub_path}\\{sub_name}",
                    ))
            except OSError:
                continue

    return programs


def get_installed_programs() -> list[InstalledProgram]:
    """Liefert alle laut Registry installierten Programme (ohne Duplikate)."""
    all_programs: list[InstalledProgram] = []
    for root_key, sub_path, source in UNINSTALL_LOCATIONS:
        all_programs.extend(_read_programs_from(root_key, sub_path, source))

    # Doppelte Eintraege (z.B. gleicher Name in 32- und 64-Bit) zusammenfassen.
    seen: set[str] = set()
    unique: list[InstalledProgram] = []
    for prog in all_programs:
        key = (prog.name.lower(), prog.version)
        dedup_key = f"{key[0]}|{key[1]}"
        if dedup_key not in seen:
            seen.add(dedup_key)
            unique.append(prog)

    return unique


if __name__ == "__main__":
    # Kleiner Selbsttest: einfach alle gefundenen Programme ausgeben.
    progs = get_installed_programs()
    print(f"Gefundene installierte Programme: {len(progs)}\n")
    for p in sorted(progs, key=lambda x: x.name.lower()):
        loc = f"  ->  {p.install_location}" if p.install_location else ""
        print(f"  [{p.source:10}] {p.name} ({p.version}){loc}")
