"""
orphan_finder.py
================
Gleicht die gescannten Ordner mit den installierten Programmen ab und findet
"verwaiste" Ordner: Ordner, zu denen es KEIN installiertes Programm (mehr)
gibt - also wahrscheinlich Reste einer unsauberen Deinstallation.

WICHTIG: "verwaist" ist eine VERMUTUNG, keine Gewissheit. Deshalb vergeben
wir einen Sicherheits-Score und schuetzen System-Ordner ausdruecklich.
Je nach Fundort (category) urteilen wir unterschiedlich vorsichtig.

Dieses Modul AENDERT NICHTS - es analysiert nur.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from registry_scan import InstalledProgram, get_installed_programs
from folder_scan import FolderInfo, scan_program_folders, age_days


# Ordnernamen, die wir NIEMALS als verwaist melden (System / gemeinsame Teile).
# Klein geschrieben fuer den Vergleich.
PROTECTED_NAMES = {
    # --- Englische System-Ordnernamen ---
    "common files", "internet explorer", "windows defender",
    "windows nt", "windows mail", "windows media player",
    "windows photo viewer", "windows portable devices",
    "windows security", "windowsapps", "windowspowershell",
    "microsoft", "microsoft.net", "microsoft office",
    "microsoft sql server", "microsoft visual studio",
    "dotnet", "msbuild", "reference assemblies",
    "uninstall information", "modifiablewindowsapps",
    "common", "shared", "intel", "amd", "nvidia corporation", "nvidia",
    "realtek", "application verifier",
    # --- Lokalisierte System-Ordnernamen (Windows uebersetzt manche!) ---
    "gemeinsame dateien",          # = Common Files (Deutsch)
    "fichiers communs",            # = Common Files (Franzoesisch)
    "archivos comunes",            # = Common Files (Spanisch)
    "file comuni",                 # = Common Files (Italienisch)
}

# Oberste Laufwerk-Ordner, die zum BETRIEBSSYSTEM gehoeren -> immer schuetzen.
# (Sonst wuerden wir z.B. C:\Windows als "verwaist" melden - katastrophal.)
DRIVE_ROOT_PROTECTED = {
    "windows", "windows.old", "users", "benutzer", "programdata",
    "program files", "program files (x86)", "programme",
    "$recycle.bin", "system volume information", "recovery",
    "perflogs", "msocache", "$windows.~bt", "$windows.~ws",
    "$sysreset", "documents and settings", "config.msi",
    "boot", "efi", "intel", "amd", "drivers", "dell", "hp", "lenovo",
    "inetpub", "onedrivetemp", "msdia80.dll", "pagefile.sys",
    "hiberfil.sys", "swapfile.sys", "dumpstack.log.tmp", "appdata",
}

# Bekannte ProgramData-Ordner, die zum System/Windows gehoeren -> schuetzen.
PROGRAMDATA_PROTECTED = {
    "microsoft", "packages", "package cache", "temp", "tmp", "ssh",
    "softwaredistribution", "packercrashcanary", "windows",
    "windowsholographicdevices", "usooshared", "ntuser.pol",
    "regid.1991-06.com.microsoft", "comms", "dell", "intel", "amd",
    "nvidia corporation", "nvidia",
}

# Bekannte AppData-Ordner, die keine "Installation" sind -> schuetzen.
APPDATA_PROTECTED = {
    "microsoft", "packages", "temp", "tmp", "programs", "google",
    "comms", "connecteddevicesplatform", "publishers", "d3dscache",
    "elevateddiagnostics", "diagnostics", "vialib", "crashdumps",
    "package cache", "powershell", "windowsapps", "appv",
}

# Basis-Sicherheit je Kategorie. Wo auch eigene Daten liegen koennen, starten
# wir niedriger -> weniger Gefahr, etwas Falsches vorzuschlagen.
CATEGORY_BASE_CONFIDENCE = {
    "program_files": 60,
    "user_programs": 60,
    "programdata": 45,
    "drive_root": 35,
    "appdata_local": 30,
    "appdata_roaming": 30,
}


@dataclass
class OrphanCandidate:
    """Ein Ordner, der moeglicherweise verwaist ist.

    Wichtig: 'confidence' beantwortet nur die Frage "ist das ein Rest?".
    'warning' beantwortet getrennt davon die Frage "wie riskant ist Loeschen?"
    - z.B. weil ein grosser Ordner ein aktives Spiel sein KOENNTE. Beides
    bewusst getrennt, damit wir wertvolle grosse Treffer nicht verstecken.
    """
    folder: FolderInfo
    confidence: int          # 0-100: wie sicher sind wir, dass es Rest ist?
    reason: str              # menschenlesbare Begruendung
    warning: str = ""        # zusaetzlicher Warnhinweis (leer = keiner)


def _normalize(text: str) -> str:
    """Vereinheitlicht Namen fuer den Vergleich (klein, ohne Version/Zeichen)."""
    text = text.lower()
    text = re.sub(r"\(.*?\)", " ", text)          # Klammern raus
    text = re.sub(r"[\d.]+(?:bit)?", " ", text)   # Versionsnummern raus
    text = re.sub(r"[^a-z0-9 ]", " ", text)       # Sonderzeichen -> Leerzeichen
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokens(text: str) -> set[str]:
    """Zerlegt einen normalisierten Namen in aussagekraeftige Woerter."""
    stop = {"the", "inc", "ltd", "gmbh", "corp", "corporation", "co", "llc"}
    return {w for w in _normalize(text).split() if len(w) > 2 and w not in stop}


def _build_program_index(programs: list[InstalledProgram]) -> tuple[set[str], list[set[str]]]:
    """Baut Suchindizes aus den installierten Programmen auf.

    Liefert:
      * eine Menge normalisierter Install-Pfade (fuer exakten Pfad-Match)
      * eine Liste von Token-Mengen (Programmname + Hersteller) fuer Fuzzy-Match
    """
    install_paths: set[str] = set()
    token_sets: list[set[str]] = []

    for p in programs:
        if p.install_location:
            install_paths.add(p.install_location.rstrip("\\").lower())
        toks = _tokens(p.name) | _tokens(p.publisher)
        if toks:
            token_sets.append(toks)

    return install_paths, token_sets


def _is_protected(folder: FolderInfo) -> bool:
    """True, wenn der Ordner aufgrund seiner Kategorie/Namens geschuetzt ist."""
    name = folder.name.lower()
    if name in PROTECTED_NAMES:
        return True
    if folder.category == "drive_root" and name in DRIVE_ROOT_PROTECTED:
        return True
    if folder.category == "programdata" and name in PROGRAMDATA_PROTECTED:
        return True
    if folder.category in ("appdata_local", "appdata_roaming") and name in APPDATA_PROTECTED:
        return True
    return False


def find_orphans(min_confidence: int = 0,
                 min_age_days: float = 0.0,
                 progress: bool = False) -> list[OrphanCandidate]:
    """Findet verwaiste Ordner.

    min_confidence: nur Kandidaten ab dieser Sicherheit zurueckgeben (0-100).
    min_age_days:   nur Ordner, die seit so vielen Tagen NICHT mehr veraendert
                    wurden (0 = kein Filter). Ordner mit unbekanntem Alter
                    werden bei aktivem Filter ausgeblendet.
    """
    programs = get_installed_programs()
    folders = scan_program_folders(compute_sizes=True, progress=progress)
    install_paths, token_sets = _build_program_index(programs)

    candidates: list[OrphanCandidate] = []

    for folder in folders:
        folder_path_lc = str(folder.path).rstrip("\\").lower()

        # 0) Alters-Filter: nur seit min_age_days unberuehrte Ordner zeigen.
        if min_age_days > 0:
            age = age_days(folder.last_modified)
            if age < min_age_days:   # zu kuerzlich genutzt ODER Alter unbekannt (-1)
                continue

        # 1) Geschuetzter System-/Sonderordner? -> nie als verwaist melden.
        if _is_protected(folder):
            continue

        # 2) Exakter Treffer ueber den Install-Pfad eines Programms?
        #    (Programm liegt in oder unterhalb dieses Ordners)
        path_match = any(
            ip == folder_path_lc or ip.startswith(folder_path_lc + "\\")
            for ip in install_paths
        )
        if path_match:
            continue  # sauber zugeordnet -> kein Rest

        # 3) Fuzzy-Treffer ueber Ordnername gegen Programmnamen?
        folder_tokens = _tokens(folder.name)
        is_matched = False
        if folder_tokens:
            for toks in token_sets:
                if folder_tokens & toks:   # gemeinsame Woerter -> Treffer
                    is_matched = True
                    break

        if is_matched:
            continue  # wahrscheinlich zugeordnet

        # 4) Kein Treffer -> verwaister Kandidat. Sicherheit + Warnung bestimmen.
        confidence, reason = _score_orphan(folder, folder_tokens)
        warning = _risk_warning(folder)

        if confidence >= min_confidence:
            candidates.append(OrphanCandidate(
                folder=folder,
                confidence=confidence,
                reason=reason,
                warning=warning,
            ))

    # Groesster Speicher-Gewinn zuerst (das ist ja das Ziel), dann Sicherheit.
    candidates.sort(key=lambda c: (c.folder.size_bytes, c.confidence), reverse=True)
    return candidates


def _risk_warning(folder: FolderInfo) -> str:
    """Liefert einen Warnhinweis zum LOESCH-Risiko (unabhaengig vom Score).

    Grosse Ordner sind oft aktive Spiele/Programme, die nur nicht in der
    Registry stehen. Wir verstecken sie NICHT (sie bringen den meisten Platz),
    sondern markieren sie deutlich zum Pruefen.
    """
    if folder.size_bytes > 5_000_000_000:        # > 5 GB
        return "SEHR GROSS - erst pruefen, ob aktives Spiel/Programm!"
    if folder.size_bytes > 1_000_000_000:        # > 1 GB
        return "GROSS - evtl. aktives Programm (Steam/Epic?), bitte pruefen"
    return ""


def _score_orphan(folder: FolderInfo, folder_tokens: set[str]) -> tuple[int, str]:
    """Schaetzt ein, wie sicher ein Ordner ein loeschbarer Rest ist.

    Konservativ: im Zweifel niedriger Score (-> wird nicht voreilig geloescht).
    Die Basis haengt von der Kategorie ab (siehe CATEGORY_BASE_CONFIDENCE).
    """
    confidence = CATEGORY_BASE_CONFIDENCE.get(folder.category, 40)
    reasons = [f"Kein passendes Programm ({folder.category})"]

    # Leerer/winziger Ordner ist oft ein harmloser Rest.
    if folder.size_bytes == 0:
        confidence += 15
        reasons.append("Ordner ist leer")
    elif folder.size_bytes < 1_000_000:  # < ~1 MB
        confidence += 5
        reasons.append("sehr klein")

    # WANN wurde der Ordner zuletzt veraendert? Das ist das wichtigste Signal
    # dafuer, ob die zugehoerige App noch GENUTZT wird. Kuerzlich genutzt ->
    # ziemlich sicher KEIN Rest. Lange unberuehrt -> eher ein Rest.
    days = age_days(folder.last_modified)
    if days < 0:
        pass  # Alter unbekannt -> keine Aenderung
    elif days < 14:
        confidence -= 40
        reasons.append("kuerzlich genutzt (<2 Wochen) - wohl KEIN Rest")
    elif days < 90:
        confidence -= 20
        reasons.append("vor kurzem genutzt (<3 Monate)")
    elif days > 365:
        confidence += 15
        reasons.append("seit >1 Jahr unberuehrt")

    # Hinweis: Die GROESSE fliesst bewusst NICHT in die Sicherheit ein.
    # Ein grosser Ordner kann genauso ein echter Rest sein (= grosser
    # Speicher-Gewinn). Das Loesch-Risiko grosser Ordner behandeln wir
    # getrennt ueber _risk_warning().

    # Ohne erkennbare Woerter koennen wir schlecht urteilen -> vorsichtiger.
    if not folder_tokens:
        confidence -= 20
        reasons.append("Name schwer einzuordnen (Vorsicht)")

    confidence = max(0, min(100, confidence))
    return confidence, "; ".join(reasons)


if __name__ == "__main__":
    from folder_scan import human_size

    orphans = find_orphans(progress=True)
    print(f"\nMoegliche verwaiste Ordner: {len(orphans)}\n")
    for o in orphans:
        print(f"  [{o.confidence:3d}%] {human_size(o.folder.size_bytes):>10}  "
              f"{o.folder.path}")
        print(f"         -> {o.reason}")
        if o.warning:
            print(f"         /!\\ {o.warning}")
