"""
i18n.py
=======
Uebersetzungs-Hilfe fuer CleanSweep.

Prinzip: Die DEUTSCHEN Texte im Code sind die "Schluessel". t(text) liefert
die Uebersetzung fuer die aktuell gewaehlte Sprache - oder den deutschen
Originaltext, wenn keine Uebersetzung hinterlegt ist (bzw. Sprache = de).

Unterstuetzte Sprachen: de (Quelle), en, es, pl, fr.
Eine neue Sprache = ein weiterer Eintrag in _TRANSLATIONS.
"""

from __future__ import annotations

import os

_SUPPORTED = ("de", "en", "es", "pl", "fr", "uk")
_LANG = "de"


def set_language(lang: str) -> None:
    global _LANG
    _LANG = lang if lang in _SUPPORTED else "de"


def get_language() -> str:
    return _LANG


def _config_path() -> str:
    """Pfad zur kleinen Sprach-Merkdatei (im Benutzerprofil)."""
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    return os.path.join(base, "CleanSweep", "lang.txt")


def load_saved_language() -> None:
    """Laedt die zuletzt gewaehlte Sprache (falls vorhanden)."""
    try:
        with open(_config_path(), encoding="utf-8") as fh:
            lang = fh.read().strip()
        if lang in _SUPPORTED:
            set_language(lang)
    except OSError:
        pass


def save_language(lang: str) -> None:
    """Merkt sich die Sprache fuer den naechsten Start (best effort)."""
    if lang not in _SUPPORTED:
        return
    try:
        path = _config_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(lang)
    except OSError:
        pass


def t(text: str) -> str:
    """Uebersetzt einen deutschen Text in die aktuelle Sprache (Fallback: de)."""
    if _LANG == "de":
        return text
    return _TRANSLATIONS.get(_LANG, {}).get(text, text)


_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "CleanSweep  -  Speicherplatz aufraeumen": "CleanSweep  -  Free up disk space",
        "Speicherplatz finden und sicher freigeben": "Find and safely free up disk space",
        "Bereit.": "Ready.",
        "Sprache": "Language",
        "Beginner": "Beginner",
        "Expert": "Expert",
        "Modus:": "Mode:",
        "♥ Unterstuetzen": "♥ Support",
        "Entwicklung mit einer PayPal-Spende unterstuetzen":
            "Support development with a PayPal donation",
        "Spendenlink ist noch nicht eingetragen.\n\nBitte in gui.py die Variable "
        "DONATE_URL setzen.":
            "Donation link is not set yet.\n\nPlease set the DONATE_URL variable "
            "in gui.py.",
        "  Verwaiste Ordner  ": "  Orphaned folders  ",
        "  Temp-Dateien  ": "  Temp files  ",
        "  Grosse Dateien  ": "  Large files  ",
        "  Windows-Update  ": "  Windows Update  ",
        "  Windows.old  ": "  Windows.old  ",
        "  Caches  ": "  Caches  ",
        "  System  ": "  System  ",
        "Scan starten": "Start scan",
        "Auswahl in Papierkorb": "Selection to Recycle Bin",
        "Mindest-Sicherheit:": "Min. confidence:",
        "ungenutzt seit (Monate):": "unused for (months):",
        "Temp scannen": "Scan temp",
        "Temp leeren (endgueltig)": "Empty temp (permanent)",
        "nur aelter als (Tage):": "only older than (days):",
        "Grosse Dateien suchen": "Find large files",
        "ab Groesse (MB):": "min. size (MB):",
        "Update-Cache scannen": "Scan update cache",
        "Update-Cache leeren": "Empty update cache",
        "Als Administrator neu starten": "Restart as administrator",
        "Analysieren": "Analyze",
        "Bereinigen": "Clean up",
        "ResetBase (gruendlicher)": "ResetBase (more thorough)",
        "Windows.old pruefen": "Check Windows.old",
        "Datenträgerbereinigung oeffnen (Windows.old u.a. Systemreste)":
            "Open Disk Cleanup (Windows.old & other system leftovers)",
        "Speicher-Einstellungen": "Storage settings",
        "Caches suchen": "Find caches",
        "Auswahl leeren (endgueltig)": "Empty selection (permanent)",
        "Papierkorb pruefen": "Check Recycle Bin",
        "Papierkorb leeren": "Empty Recycle Bin",
        "Status pruefen": "Check status",
        "Ruhezustand abschalten": "Disable hibernation",
        "Ruhezustand einschalten": "Enable hibernation",
        "Sicher": "Conf.",
        "Groesse": "Size",
        "Zuletzt genutzt": "Last used",
        "Kategorie": "Category",
        "Ordner": "Folder",
        "Warnung": "Warning",
        "Dateien": "Files",
        "Temp-Ordner": "Temp folder",
        "Datei": "File",
        "Anzahl": "Count",
        "Programm": "Program",
        "Beispielpfad": "Example path",
        "Springe in den Ordner": "Jump to folder",
        "Komponentenspeicher (WinSxS) - DISM": "Component store (WinSxS) - DISM",
        "Papierkorb": "Recycle Bin",
        "Ruhezustand (hiberfil.sys)": "Hibernation (hiberfil.sys)",
        "Vorgang laeuft - bitte warten (die Anzeige bewegt sich):":
            "Operation running - please wait (the bar is moving):",
        "Keine Auswahl": "No selection",
        "Abgelehnt": "Rejected",
        "Nicht gefunden": "Not found",
        "Fehler": "Error",
        "Fertig": "Done",
        "Sind Sie sicher?": "Are you sure?",
        "In den Papierkorb verschieben?": "Move to Recycle Bin?",
        "Administrator noetig": "Administrator required",
        "Bereits Administrator": "Already administrator",
        "Fehlgeschlagen": "Failed",
        "Komponentenspeicher bereinigen?": "Clean up component store?",
        "Update-Cache leeren?": "Empty update cache?",
        "Temp-Dateien endgueltig loeschen?": "Permanently delete temp files?",
        "Caches endgueltig leeren?": "Permanently empty caches?",
        "Papierkorb leeren?": "Empty Recycle Bin?",
        "Datenträgerbereinigung starten?": "Start Disk Cleanup?",
        "Ruhezustand abschalten?": "Disable hibernation?",
        "Bitte zuerst Zeilen auswaehlen.": "Please select rows first.",
        "Bitte zuerst Dateien auswaehlen.": "Please select files first.",
        "Nichts Sicheres ausgewaehlt.": "Nothing safe selected.",
        "Abgebrochen.": "Cancelled.",
        "Nicht bestaetigt.": "Not confirmed.",
        "Diese werden NICHT geloescht:\n\n": "These will NOT be deleted:\n\n",
        "Scanne alle Laufwerke (das kann eine Weile dauern) ...":
            "Scanning all drives (this may take a while) ...",
        "Scanne Temp-Ordner ...": "Scanning temp folders ...",
        "Loesche Temp-Dateien ...": "Deleting temp files ...",
        "Durchsuche alle Laufwerke nach grossen Dateien (dauert) ...":
            "Searching all drives for large files (takes a while) ...",
        "Suche Cache-Ordner ...": "Searching cache folders ...",
        "Leere Caches ...": "Emptying caches ...",
        "Scanne Windows-Update-Cache ...": "Scanning Windows Update cache ...",
        "Stoppe Dienste und leere Cache ...":
            "Stopping services and emptying cache ...",
        "Pruefe Windows.old (Groesse berechnen kann dauern) ...":
            "Checking Windows.old (calculating size may take a while) ...",
        "Kein Windows.old gefunden.": "No Windows.old found.",
        "Kein 'Windows.old' vorhanden - nichts zu tun. :)":
            "No 'Windows.old' present - nothing to do. :)",
        "Ruhezustand-Status geprueft.": "Hibernation status checked.",
        "DISM analysiert den Komponentenspeicher ...":
            "DISM is analyzing the component store ...",
        "DISM bereinigt den Komponentenspeicher ...":
            "DISM is cleaning the component store ...",
        "DISM fertig.": "DISM finished.",
        "DISM meldete einen Fehler.": "DISM reported an error.",
        "Papierkorb geleert.": "Recycle Bin emptied.",
        "Papierkorb war leer oder konnte nicht geleert werden.":
            "Recycle Bin was empty or could not be emptied.",
        "unbekannt": "unknown",
        "heute": "today",
        "Geschuetzter System-/Wurzelordner": "Protected system/root folder",
        "Das ist eine Laufwerks-Wurzel": "This is a drive root",
        "Liegt im Windows-Systemordner": "Located in the Windows system folder",
        "Steht auf der Schutzliste (geschuetzter Name)":
            "On the protection list (protected name)",
        "Pfad existiert nicht (mehr)": "Path no longer exists",
        "Kein Ordner": "Not a folder",
        "Datei existiert nicht (mehr)": "File no longer exists",
        "System-/Auslagerungsdatei": "System/paging file",
        "SEHR GROSS - erst pruefen, ob aktives Spiel/Programm!":
            "VERY LARGE - check first whether it's an active game/program!",
        "GROSS - evtl. aktives Programm (Steam/Epic?), bitte pruefen":
            "LARGE - possibly an active program (Steam/Epic?), please check",
        "ja": "yes",
        "nein (zum Leeren noetig)": "no (required to empty)",
        "Erfolgreich.": "Successful.",
        "Fehler.": "Error.",
        # lange Hinweise
        "Temp-Dateien werden ENDGUELTIG geloescht (nicht in den Papierkorb), "
        "damit der Platz wirklich frei wird. Gesperrte Dateien bleiben "
        "unangetastet.":
            "Temp files are deleted PERMANENTLY (not to the Recycle Bin) so the "
            "space is actually freed. Locked files are left untouched.",
        "Findet die groessten Einzeldateien (z.B. alte Videos, ISO-Dateien). "
        "Amber = kuerzlich genutzt (evtl. aktives Spiel/Programm). Loeschen geht "
        "in den Papierkorb.":
            "Finds the largest individual files (e.g. old videos, ISO files). "
            "Amber = recently used (possibly an active game/program). Deletion "
            "goes to the Recycle Bin.",
        "Heruntergeladene Windows-Update-Pakete (SoftwareDistribution\\Download) "
        "sind nach der Installation nutzlos. Sie werden ENDGUELTIG geloescht "
        "und von Windows bei Bedarf neu angelegt.":
            "Downloaded Windows Update packages (SoftwareDistribution\\Download) "
            "are useless after installation. They are deleted PERMANENTLY and "
            "recreated by Windows when needed.",
        "Raeumt alte, durch Updates ersetzte Windows-Komponenten gruendlicher "
        "auf als die Datentraegerbereinigung. '/ResetBase' entfernt auch "
        "ersetzte Versionen endgueltig - danach lassen sich installierte Updates "
        "aber NICHT mehr deinstallieren. Braucht Admin und kann einige Minuten "
        "dauern.":
            "Cleans up old Windows components superseded by updates more "
            "thoroughly than Disk Cleanup. '/ResetBase' also removes superseded "
            "versions permanently - after that installed updates can NO longer "
            "be uninstalled. Requires admin and may take a few minutes.",
        "WICHTIG: WinSxS bleibt IMMER mehrere GB gross (vieles ist mit Windows "
        "geteilt) - das ist normal. Und 'empfohlen: Ja' steht schon ab 1 "
        "ersetzten Paket - auf einem aktuellen Windows fast immer. Massgeblich "
        "ist die Anzahl 'bereinigbarer Pakete' (0-2 = gesund), NICHT die "
        "'empfohlen'-Zeile.":
            "IMPORTANT: WinSxS is ALWAYS several GB (much is shared with "
            "Windows) - that's normal. And 'recommended: Yes' shows from just 1 "
            "superseded package - almost always the case on an up-to-date "
            "Windows. What matters is the number of 'reclaimable packages' "
            "(0-2 = healthy), NOT the 'recommended' line.",
        "'Windows.old' enthaelt die vorherige Windows-Version nach einem Upgrade "
        "(oft 20-70 GB). Es laesst sich NICHT normal loeschen, weil es dem "
        "System gehoert (TrustedInstaller-Sperre). Der sichere Weg ist die "
        "Windows-Datenträgerbereinigung: dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "'Windows.old' contains the previous Windows version after an "
            "upgrade (often 20-70 GB). It can NOT be deleted normally because it "
            "belongs to the system (TrustedInstaller lock). The safe way is "
            "Windows Disk Cleanup: tick 'Previous Windows installation(s)' there.",
        "Cache-Ordner von Browsern und Apps. Werden automatisch neu aufgebaut "
        "und daher ENDGUELTIG geleert. Fuer das beste Ergebnis die jeweilige App "
        "vorher schliessen (gesperrte Dateien werden sonst uebersprungen).":
            "Cache folders of browsers and apps. They are rebuilt automatically "
            "and are therefore emptied PERMANENTLY. For best results, close the "
            "respective app first (locked files are skipped otherwise).",
        "CleanSweep verschiebt Ordner/Dateien in den Papierkorb. Der Platz wird "
        "erst frei, wenn er geleert wird.":
            "CleanSweep moves folders/files to the Recycle Bin. The space is "
            "only freed once it is emptied.",
        "Der Ruhezustand belegt eine Datei so gross wie dein RAM (oft 8-32 GB). "
        "Abschalten gibt diesen Platz frei - danach gibt es keinen Ruhezustand/"
        "Schnellstart mehr (jederzeit umkehrbar). Braucht Admin-Rechte.":
            "Hibernation uses a file as large as your RAM (often 8-32 GB). "
            "Disabling frees this space - afterwards there is no hibernation/fast "
            "startup (reversible at any time). Requires admin rights.",
        # Vorlagen
        "Fehler: {err}": "Error: {err}",
        "Hinweis: Zum Leeren werden Administrator-Rechte benoetigt. ":
            "Note: administrator rights are required to empty. ",
        "... und {n} weitere": "... and {n} more",
        "{n} Kandidaten  |  potentiell {size} frei. Zeilen auswaehlen (Strg/Shift).":
            "{n} candidates  |  potentially {size} free. Select rows (Ctrl/Shift).",
        "\n\nACHTUNG: Mindestens ein grosser Ordner koennte ein aktives\n"
        "Spiel/Programm sein!":
            "\n\nWARNING: At least one large folder could be an active\n"
            "game/program!",
        "{n} Ordner -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} folders -> RECYCLE BIN (recoverable).\nFrees: {size}.\n\n"
            "{preview}{warn}\n\nContinue?",
        "{ok} Ordner in den Papierkorb verschoben, {size} frei. Protokoll: {log}":
            "{ok} folders moved to the Recycle Bin, {size} free. Log: {log}",
        "Temp gesamt: {size}. 'Temp leeren' gibt diesen Platz frei.":
            "Temp total: {size}. 'Empty temp' frees this space.",
        "\n(nur Dateien aelter als {days} Tage)":
            "\n(only files older than {days} days)",
        "Temporaere Dateien werden ENDGUELTIG geloescht (NICHT in den "
        "Papierkorb).{age}\n\nGeschaetzt frei: bis zu {size}.\nGesperrte/benutzte "
        "Dateien werden uebersprungen.\n\nFortfahren?":
            "Temporary files are deleted PERMANENTLY (NOT to the Recycle "
            "Bin).{age}\n\nEstimated free: up to {size}.\nLocked/in-use files are "
            "skipped.\n\nContinue?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt/zu jung).":
            "{n} files deleted, {size} freed.\n{skip} skipped (locked/too recent).",
        "{n} grosse Dateien  |  zusammen {size}. Amber = kuerzlich genutzt.":
            "{n} large files  |  total {size}. Amber = recently used.",
        "\n\nACHTUNG: Mindestens eine Datei wurde kuerzlich genutzt -\n"
        "evtl. ein aktives Spiel/Programm!":
            "\n\nWARNING: At least one file was recently used -\n"
            "possibly an active game/program!",
        "{n} Dateien -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} files -> RECYCLE BIN (recoverable).\nFrees: {size}.\n\n"
            "{preview}{warn}\n\nContinue?",
        "{ok} Dateien in den Papierkorb verschoben, {size} frei.":
            "{ok} files moved to the Recycle Bin, {size} free.",
        "Ordner nicht vorhanden:\n{path}": "Folder does not exist:\n{path}",
        "Groesse:  {size}   ({n} Dateien)\nOrdner:   {path}\nAdmin:    {admin}":
            "Size:   {size}   ({n} files)\nFolder: {path}\nAdmin:  {admin}",
        "Update-Cache: {size}.": "Update cache: {size}.",
        "Dienste wurden gestoppt und neu gestartet.":
            "Services were stopped and restarted.",
        "Hinweis: Dienste konnten nicht gestoppt werden - gesperrte Dateien "
        "wurden uebersprungen.":
            "Note: services could not be stopped - locked files were skipped.",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen.\n\n{svc}":
            "{n} files deleted, {size} freed.\n{skip} skipped.\n\n{svc}",
        "Windows.old gefunden:  {size}\nPfad:  {drive}\\Windows.old\n\nKlicke "
        "'Mit Datenträgerbereinigung entfernen' und hake dort\n'Vorherige "
        "Windows-Installation(en)' an.":
            "Windows.old found:  {size}\nPath:  {drive}\\Windows.old\n\nClick "
            "'Open Disk Cleanup' and tick\n'Previous Windows installation(s)' "
            "there.",
        "Windows.old: {size} - ueber die Datenträgerbereinigung entfernbar.":
            "Windows.old: {size} - removable via Disk Cleanup.",
        "{n} Programme mit Cache  |  zusammen {size}. Zeilen auswaehlen (Strg/Shift).":
            "{n} programs with cache  |  total {size}. Select rows (Ctrl/Shift).",
        "Caches von: {names}\n\nbis zu {size} werden ENDGUELTIG geleert (nicht in "
        "den Papierkorb).\n\nFortfahren?":
            "Caches of: {names}\n\nup to {size} will be emptied PERMANENTLY (not "
            "to the Recycle Bin).\n\nContinue?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt - App offen?).":
            "{n} files deleted, {size} freed.\n{skip} skipped (locked - app open?).",
        "Papierkorb: {size} in {n} Objekten": "Recycle Bin: {size} in {n} items",
        "Papierkorb: {size}.": "Recycle Bin: {size}.",
        "Ruhezustand: AKTIV  (hiberfil.sys: {size})":
            "Hibernation: ACTIVE  (hiberfil.sys: {size})",
        "Ruhezustand: AUS (keine hiberfil.sys)":
            "Hibernation: OFF (no hiberfil.sys)",
        "hiberfil.sys ({size}) wird geloescht. Ruhezustand und Schnellstart sind "
        "danach aus (umkehrbar).\n\nFortfahren?":
            "hiberfil.sys ({size}) will be deleted. Hibernation and fast startup "
            "are then off (reversible).\n\nContinue?",
        "Ruhezustand abgeschaltet, Platz freigegeben.":
            "Hibernation disabled, space freed.",
        "Ruhezustand wieder eingeschaltet.": "Hibernation re-enabled.",
        "Fehler: {msg}": "Error: {msg}",
        "Der Pfad existiert nicht mehr:\n{path}":
            "The path no longer exists:\n{path}",
        "Konnte nicht oeffnen:\n{exc}": "Could not open:\n{exc}",
        "Wirklich {n} Ordner ({size}) in den Papierkorb verschieben?":
            "Really move {n} folders ({size}) to the Recycle Bin?",
        "Wirklich {n} Dateien ({size}) in den Papierkorb?":
            "Really move {n} files ({size}) to the Recycle Bin?",
        "DISM braucht Administrator-Rechte.\n\nJetzt als Administrator neu starten?":
            "DISM requires administrator rights.\n\nRestart as administrator now?",
        "Diese Aktion braucht Administrator-Rechte.\n\nJetzt als Administrator "
        "neu starten?":
            "This action requires administrator rights.\n\nRestart as "
            "administrator now?",
        "Das Programm laeuft bereits mit Admin-Rechten.":
            "The program is already running with admin rights.",
        "Neustart als Administrator wurde abgebrochen oder ist fehlgeschlagen.":
            "Restart as administrator was cancelled or failed.",
        "Zum Leeren des Update-Caches sind Administrator-Rechte noetig.\nBitte "
        "'Als Administrator neu starten' verwenden.":
            "Administrator rights are required to empty the update cache.\nPlease "
            "use 'Restart as administrator'.",
        "Es fehlten Administrator-Rechte. Bitte als Administrator neu starten.":
            "Administrator rights were missing. Please restart as administrator.",
        "Heruntergeladene Update-Pakete werden ENDGUELTIG geloescht.\nDie "
        "Update-Dienste werden kurz angehalten und danach wieder gestartet.\n\n"
        "Fortfahren?":
            "Downloaded update packages are deleted PERMANENTLY.\nThe update "
            "services are briefly stopped and then restarted.\n\nContinue?",
        "Update-Cache wirklich endgueltig leeren?":
            "Really empty the update cache permanently?",
        "Temp-Dateien wirklich endgueltig loeschen?":
            "Really delete temp files permanently?",
        "Ausgewaehlte Caches wirklich leeren?":
            "Really empty the selected caches?",
        "Der gesamte Papierkorb wird ENDGUELTIG geleert (alle Laufwerke). "
        "Danach ist eine Wiederherstellung nicht mehr moeglich.\n\nFortfahren?":
            "The entire Recycle Bin is emptied PERMANENTLY (all drives). After "
            "that, recovery is no longer possible.\n\nContinue?",
        "Es wird die Windows-Datenträgerbereinigung (cleanmgr) mit "
        "Administrator-Rechten gestartet.\n\nDort 'Vorherige Windows-"
        "Installation(en)' anhaken und auf OK klicken - Windows entfernt "
        "Windows.old dann sicher selbst.\n\nTipp: Hier lassen sich auch weitere "
        "Systemreste anhaken (Absturz-Dumps, Delivery-Optimization, "
        "Update-Bereinigung).\n\nFortfahren?":
            "Windows Disk Cleanup (cleanmgr) is started with administrator "
            "rights.\n\nTick 'Previous Windows installation(s)' there and click "
            "OK - Windows then safely removes Windows.old itself.\n\nTip: You can "
            "also tick further system leftovers here (crash dumps, delivery "
            "optimization, update cleanup).\n\nContinue?",
        "Konnte die Datenträgerbereinigung nicht starten (evtl. UAC "
        "abgebrochen). Alternativ ueber 'Speicher-Einstellungen'.":
            "Could not start Disk Cleanup (UAC may have been cancelled). "
            "Alternatively use 'Storage settings'.",
        "Datenträgerbereinigung gestartet - bitte dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "Disk Cleanup started - please tick 'Previous Windows "
            "installation(s)' there.",
        "Analysiere Komponentenspeicher ... bitte warten.\n\nSolange die blaue "
        "Anzeige sich bewegt, laeuft der Vorgang - das Fenster bitte NICHT "
        "schliessen.":
            "Analyzing component store ... please wait.\n\nWhile the blue bar is "
            "moving, the operation is running - please do NOT close the window.",
        "Bereinige Komponentenspeicher ... das kann 10-20 Minuten dauern.\n\n"
        "Solange die blaue Anzeige sich bewegt, laeuft der Vorgang - das Fenster "
        "bitte NICHT schliessen und warten. Es ist NICHT eingefroren.":
            "Cleaning component store ... this can take 10-20 minutes.\n\nWhile "
            "the blue bar is moving, the operation is running - please do NOT "
            "close the window and wait. It is NOT frozen.",
        "vor {n} Tagen": "{n} days ago",
        "vor {n} Monaten": "{n} months ago",
        "vor {n} Jahren": "{n} years ago",
        "\n\nACHTUNG ResetBase: installierte Updates lassen sich danach NICHT "
        "mehr deinstallieren.":
            "\n\nWARNING ResetBase: installed updates can NO longer be "
            "uninstalled afterwards.",
        "DISM raeumt jetzt den WinSxS-Speicher auf.\n\nWICHTIG: Das kann 10-20 "
        "Minuten dauern und zeigt KEINEN Fortschritt in Prozent. Das Fenster "
        "bitte offen lassen und warten - es ist nicht eingefroren.{extra}\n\n"
        "Fortfahren?":
            "DISM will now clean up the WinSxS store.\n\nIMPORTANT: This can take "
            "10-20 minutes and shows NO progress in percent. Please leave the "
            "window open and wait - it is not frozen.{extra}\n\nContinue?",
    },

    "es": {
        "CleanSweep  -  Speicherplatz aufraeumen": "CleanSweep  -  Liberar espacio en disco",
        "Speicherplatz finden und sicher freigeben": "Encontrar y liberar espacio de forma segura",
        "Bereit.": "Listo.",
        "Sprache": "Idioma",
        "Beginner": "Principiante",
        "Expert": "Experto",
        "Modus:": "Modo:",
        "♥ Unterstuetzen": "♥ Apoyar",
        "Entwicklung mit einer PayPal-Spende unterstuetzen":
            "Apoya el desarrollo con una donación de PayPal",
        "Spendenlink ist noch nicht eingetragen.\n\nBitte in gui.py die Variable "
        "DONATE_URL setzen.":
            "El enlace de donación aún no está configurado.\n\nConfigure la "
            "variable DONATE_URL en gui.py.",
        "  Verwaiste Ordner  ": "  Carpetas huérfanas  ",
        "  Temp-Dateien  ": "  Archivos temporales  ",
        "  Grosse Dateien  ": "  Archivos grandes  ",
        "  Windows-Update  ": "  Windows Update  ",
        "  Windows.old  ": "  Windows.old  ",
        "  Caches  ": "  Cachés  ",
        "  System  ": "  Sistema  ",
        "Scan starten": "Iniciar análisis",
        "Auswahl in Papierkorb": "Selección a la papelera",
        "Mindest-Sicherheit:": "Confianza mín.:",
        "ungenutzt seit (Monate):": "sin usar desde (meses):",
        "Temp scannen": "Analizar temp.",
        "Temp leeren (endgueltig)": "Vaciar temp. (definitivo)",
        "nur aelter als (Tage):": "solo más antiguos que (días):",
        "Grosse Dateien suchen": "Buscar archivos grandes",
        "ab Groesse (MB):": "tamaño mín. (MB):",
        "Update-Cache scannen": "Analizar caché de Update",
        "Update-Cache leeren": "Vaciar caché de Update",
        "Als Administrator neu starten": "Reiniciar como administrador",
        "Analysieren": "Analizar",
        "Bereinigen": "Limpiar",
        "ResetBase (gruendlicher)": "ResetBase (más a fondo)",
        "Windows.old pruefen": "Comprobar Windows.old",
        "Datenträgerbereinigung oeffnen (Windows.old u.a. Systemreste)":
            "Abrir Liberador de espacio (Windows.old y otros restos)",
        "Speicher-Einstellungen": "Ajustes de almacenamiento",
        "Caches suchen": "Buscar cachés",
        "Auswahl leeren (endgueltig)": "Vaciar selección (definitivo)",
        "Papierkorb pruefen": "Comprobar papelera",
        "Papierkorb leeren": "Vaciar papelera",
        "Status pruefen": "Comprobar estado",
        "Ruhezustand abschalten": "Desactivar hibernación",
        "Ruhezustand einschalten": "Activar hibernación",
        "Sicher": "Conf.",
        "Groesse": "Tamaño",
        "Zuletzt genutzt": "Último uso",
        "Kategorie": "Categoría",
        "Ordner": "Carpeta",
        "Warnung": "Aviso",
        "Dateien": "Archivos",
        "Temp-Ordner": "Carpeta temporal",
        "Datei": "Archivo",
        "Anzahl": "Cantidad",
        "Programm": "Programa",
        "Beispielpfad": "Ruta de ejemplo",
        "Springe in den Ordner": "Ir a la carpeta",
        "Komponentenspeicher (WinSxS) - DISM": "Almacén de componentes (WinSxS) - DISM",
        "Papierkorb": "Papelera de reciclaje",
        "Ruhezustand (hiberfil.sys)": "Hibernación (hiberfil.sys)",
        "Vorgang laeuft - bitte warten (die Anzeige bewegt sich):":
            "Operación en curso - espere (la barra se mueve):",
        "Keine Auswahl": "Sin selección",
        "Abgelehnt": "Rechazado",
        "Nicht gefunden": "No encontrado",
        "Fehler": "Error",
        "Fertig": "Hecho",
        "Sind Sie sicher?": "¿Está seguro?",
        "In den Papierkorb verschieben?": "¿Mover a la papelera?",
        "Administrator noetig": "Se requiere administrador",
        "Bereits Administrator": "Ya es administrador",
        "Fehlgeschlagen": "Error",
        "Komponentenspeicher bereinigen?": "¿Limpiar el almacén de componentes?",
        "Update-Cache leeren?": "¿Vaciar la caché de Update?",
        "Temp-Dateien endgueltig loeschen?": "¿Eliminar definitivamente los archivos temporales?",
        "Caches endgueltig leeren?": "¿Vaciar definitivamente las cachés?",
        "Papierkorb leeren?": "¿Vaciar la papelera?",
        "Datenträgerbereinigung starten?": "¿Iniciar el Liberador de espacio?",
        "Ruhezustand abschalten?": "¿Desactivar la hibernación?",
        "Bitte zuerst Zeilen auswaehlen.": "Seleccione primero algunas filas.",
        "Bitte zuerst Dateien auswaehlen.": "Seleccione primero algunos archivos.",
        "Nichts Sicheres ausgewaehlt.": "Nada seguro seleccionado.",
        "Abgebrochen.": "Cancelado.",
        "Nicht bestaetigt.": "No confirmado.",
        "Diese werden NICHT geloescht:\n\n": "Estos NO se eliminarán:\n\n",
        "Scanne alle Laufwerke (das kann eine Weile dauern) ...":
            "Analizando todas las unidades (puede tardar) ...",
        "Scanne Temp-Ordner ...": "Analizando carpetas temporales ...",
        "Loesche Temp-Dateien ...": "Eliminando archivos temporales ...",
        "Durchsuche alle Laufwerke nach grossen Dateien (dauert) ...":
            "Buscando archivos grandes en todas las unidades (tarda) ...",
        "Suche Cache-Ordner ...": "Buscando carpetas de caché ...",
        "Leere Caches ...": "Vaciando cachés ...",
        "Scanne Windows-Update-Cache ...": "Analizando la caché de Windows Update ...",
        "Stoppe Dienste und leere Cache ...":
            "Deteniendo servicios y vaciando la caché ...",
        "Pruefe Windows.old (Groesse berechnen kann dauern) ...":
            "Comprobando Windows.old (calcular el tamaño puede tardar) ...",
        "Kein Windows.old gefunden.": "No se encontró Windows.old.",
        "Kein 'Windows.old' vorhanden - nichts zu tun. :)":
            "No hay 'Windows.old' - nada que hacer. :)",
        "Ruhezustand-Status geprueft.": "Estado de hibernación comprobado.",
        "DISM analysiert den Komponentenspeicher ...":
            "DISM está analizando el almacén de componentes ...",
        "DISM bereinigt den Komponentenspeicher ...":
            "DISM está limpiando el almacén de componentes ...",
        "DISM fertig.": "DISM finalizado.",
        "DISM meldete einen Fehler.": "DISM informó de un error.",
        "Papierkorb geleert.": "Papelera vaciada.",
        "Papierkorb war leer oder konnte nicht geleert werden.":
            "La papelera estaba vacía o no se pudo vaciar.",
        "unbekannt": "desconocido",
        "heute": "hoy",
        "Geschuetzter System-/Wurzelordner": "Carpeta protegida del sistema/raíz",
        "Das ist eine Laufwerks-Wurzel": "Es la raíz de una unidad",
        "Liegt im Windows-Systemordner": "Está en la carpeta del sistema de Windows",
        "Steht auf der Schutzliste (geschuetzter Name)":
            "En la lista de protección (nombre protegido)",
        "Pfad existiert nicht (mehr)": "La ruta ya no existe",
        "Kein Ordner": "No es una carpeta",
        "Datei existiert nicht (mehr)": "El archivo ya no existe",
        "System-/Auslagerungsdatei": "Archivo de sistema/paginación",
        "SEHR GROSS - erst pruefen, ob aktives Spiel/Programm!":
            "MUY GRANDE - ¡compruebe primero si es un juego/programa activo!",
        "GROSS - evtl. aktives Programm (Steam/Epic?), bitte pruefen":
            "GRANDE - posible programa activo (¿Steam/Epic?), compruebe",
        "ja": "sí",
        "nein (zum Leeren noetig)": "no (necesario para vaciar)",
        "Erfolgreich.": "Correcto.",
        "Fehler.": "Error.",
        "Temp-Dateien werden ENDGUELTIG geloescht (nicht in den Papierkorb), "
        "damit der Platz wirklich frei wird. Gesperrte Dateien bleiben "
        "unangetastet.":
            "Los archivos temporales se eliminan DEFINITIVAMENTE (no a la "
            "papelera) para liberar espacio realmente. Los archivos bloqueados "
            "no se tocan.",
        "Findet die groessten Einzeldateien (z.B. alte Videos, ISO-Dateien). "
        "Amber = kuerzlich genutzt (evtl. aktives Spiel/Programm). Loeschen geht "
        "in den Papierkorb.":
            "Encuentra los archivos individuales más grandes (p. ej. vídeos "
            "antiguos, archivos ISO). Ámbar = usado recientemente (posible "
            "juego/programa activo). La eliminación va a la papelera.",
        "Heruntergeladene Windows-Update-Pakete (SoftwareDistribution\\Download) "
        "sind nach der Installation nutzlos. Sie werden ENDGUELTIG geloescht "
        "und von Windows bei Bedarf neu angelegt.":
            "Los paquetes de Windows Update descargados "
            "(SoftwareDistribution\\Download) son inútiles tras la instalación. "
            "Se eliminan DEFINITIVAMENTE y Windows los vuelve a crear si es "
            "necesario.",
        "Raeumt alte, durch Updates ersetzte Windows-Komponenten gruendlicher "
        "auf als die Datentraegerbereinigung. '/ResetBase' entfernt auch "
        "ersetzte Versionen endgueltig - danach lassen sich installierte Updates "
        "aber NICHT mehr deinstallieren. Braucht Admin und kann einige Minuten "
        "dauern.":
            "Limpia los componentes de Windows antiguos sustituidos por "
            "actualizaciones más a fondo que el Liberador de espacio. "
            "'/ResetBase' también elimina definitivamente las versiones "
            "sustituidas; después las actualizaciones instaladas ya NO se pueden "
            "desinstalar. Requiere administrador y puede tardar varios minutos.",
        "WICHTIG: WinSxS bleibt IMMER mehrere GB gross (vieles ist mit Windows "
        "geteilt) - das ist normal. Und 'empfohlen: Ja' steht schon ab 1 "
        "ersetzten Paket - auf einem aktuellen Windows fast immer. Massgeblich "
        "ist die Anzahl 'bereinigbarer Pakete' (0-2 = gesund), NICHT die "
        "'empfohlen'-Zeile.":
            "IMPORTANTE: WinSxS SIEMPRE ocupa varios GB (mucho se comparte con "
            "Windows); es normal. Y 'recomendado: Sí' aparece ya con 1 paquete "
            "sustituido, casi siempre en un Windows actualizado. Lo relevante es "
            "el número de 'paquetes recuperables' (0-2 = sano), NO la línea "
            "'recomendado'.",
        "'Windows.old' enthaelt die vorherige Windows-Version nach einem Upgrade "
        "(oft 20-70 GB). Es laesst sich NICHT normal loeschen, weil es dem "
        "System gehoert (TrustedInstaller-Sperre). Der sichere Weg ist die "
        "Windows-Datenträgerbereinigung: dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "'Windows.old' contiene la versión anterior de Windows tras una "
            "actualización (a menudo 20-70 GB). NO se puede eliminar de forma "
            "normal porque pertenece al sistema (bloqueo de TrustedInstaller). La "
            "vía segura es el Liberador de espacio de Windows: marque ahí "
            "'Instalación(es) anterior(es) de Windows'.",
        "Cache-Ordner von Browsern und Apps. Werden automatisch neu aufgebaut "
        "und daher ENDGUELTIG geleert. Fuer das beste Ergebnis die jeweilige App "
        "vorher schliessen (gesperrte Dateien werden sonst uebersprungen).":
            "Carpetas de caché de navegadores y aplicaciones. Se reconstruyen "
            "automáticamente, por eso se vacían DEFINITIVAMENTE. Para el mejor "
            "resultado, cierre antes la aplicación correspondiente (de lo "
            "contrario se omiten los archivos bloqueados).",
        "CleanSweep verschiebt Ordner/Dateien in den Papierkorb. Der Platz wird "
        "erst frei, wenn er geleert wird.":
            "CleanSweep mueve carpetas/archivos a la papelera. El espacio solo se "
            "libera cuando se vacía.",
        "Der Ruhezustand belegt eine Datei so gross wie dein RAM (oft 8-32 GB). "
        "Abschalten gibt diesen Platz frei - danach gibt es keinen Ruhezustand/"
        "Schnellstart mehr (jederzeit umkehrbar). Braucht Admin-Rechte.":
            "La hibernación usa un archivo tan grande como tu RAM (a menudo 8-32 "
            "GB). Desactivarla libera ese espacio; después no hay "
            "hibernación/inicio rápido (reversible en cualquier momento). "
            "Requiere permisos de administrador.",
        "Fehler: {err}": "Error: {err}",
        "Hinweis: Zum Leeren werden Administrator-Rechte benoetigt. ":
            "Nota: se requieren permisos de administrador para vaciar. ",
        "... und {n} weitere": "... y {n} más",
        "{n} Kandidaten  |  potentiell {size} frei. Zeilen auswaehlen (Strg/Shift).":
            "{n} candidatos  |  potencialmente {size} libres. Seleccione filas (Ctrl/Mayús).",
        "\n\nACHTUNG: Mindestens ein grosser Ordner koennte ein aktives\n"
        "Spiel/Programm sein!":
            "\n\nATENCIÓN: ¡Al menos una carpeta grande podría ser un\n"
            "juego/programa activo!",
        "{n} Ordner -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} carpetas -> PAPELERA (recuperable).\nSe liberan: {size}.\n\n"
            "{preview}{warn}\n\n¿Continuar?",
        "{ok} Ordner in den Papierkorb verschoben, {size} frei. Protokoll: {log}":
            "{ok} carpetas movidas a la papelera, {size} libres. Registro: {log}",
        "Temp gesamt: {size}. 'Temp leeren' gibt diesen Platz frei.":
            "Temp. total: {size}. 'Vaciar temp.' libera este espacio.",
        "\n(nur Dateien aelter als {days} Tage)":
            "\n(solo archivos de más de {days} días)",
        "Temporaere Dateien werden ENDGUELTIG geloescht (NICHT in den "
        "Papierkorb).{age}\n\nGeschaetzt frei: bis zu {size}.\nGesperrte/benutzte "
        "Dateien werden uebersprungen.\n\nFortfahren?":
            "Los archivos temporales se eliminan DEFINITIVAMENTE (NO a la "
            "papelera).{age}\n\nLiberación estimada: hasta {size}.\nLos archivos "
            "bloqueados/en uso se omiten.\n\n¿Continuar?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt/zu jung).":
            "{n} archivos eliminados, {size} liberados.\n{skip} omitidos "
            "(bloqueados/demasiado recientes).",
        "{n} grosse Dateien  |  zusammen {size}. Amber = kuerzlich genutzt.":
            "{n} archivos grandes  |  en total {size}. Ámbar = uso reciente.",
        "\n\nACHTUNG: Mindestens eine Datei wurde kuerzlich genutzt -\n"
        "evtl. ein aktives Spiel/Programm!":
            "\n\nATENCIÓN: Al menos un archivo se usó recientemente -\n"
            "¡posible juego/programa activo!",
        "{n} Dateien -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} archivos -> PAPELERA (recuperable).\nSe liberan: {size}.\n\n"
            "{preview}{warn}\n\n¿Continuar?",
        "{ok} Dateien in den Papierkorb verschoben, {size} frei.":
            "{ok} archivos movidos a la papelera, {size} libres.",
        "Ordner nicht vorhanden:\n{path}": "La carpeta no existe:\n{path}",
        "Groesse:  {size}   ({n} Dateien)\nOrdner:   {path}\nAdmin:    {admin}":
            "Tamaño:  {size}   ({n} archivos)\nCarpeta: {path}\nAdmin:   {admin}",
        "Update-Cache: {size}.": "Caché de Update: {size}.",
        "Dienste wurden gestoppt und neu gestartet.":
            "Los servicios se detuvieron y reiniciaron.",
        "Hinweis: Dienste konnten nicht gestoppt werden - gesperrte Dateien "
        "wurden uebersprungen.":
            "Nota: no se pudieron detener los servicios; se omitieron los "
            "archivos bloqueados.",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen.\n\n{svc}":
            "{n} archivos eliminados, {size} liberados.\n{skip} omitidos.\n\n{svc}",
        "Windows.old gefunden:  {size}\nPfad:  {drive}\\Windows.old\n\nKlicke "
        "'Mit Datenträgerbereinigung entfernen' und hake dort\n'Vorherige "
        "Windows-Installation(en)' an.":
            "Windows.old encontrado:  {size}\nRuta:  {drive}\\Windows.old\n\nHaga "
            "clic en 'Abrir Liberador de espacio' y marque\n'Instalación(es) "
            "anterior(es) de Windows'.",
        "Windows.old: {size} - ueber die Datenträgerbereinigung entfernbar.":
            "Windows.old: {size} - eliminable con el Liberador de espacio.",
        "{n} Programme mit Cache  |  zusammen {size}. Zeilen auswaehlen (Strg/Shift).":
            "{n} programas con caché  |  en total {size}. Seleccione filas (Ctrl/Mayús).",
        "Caches von: {names}\n\nbis zu {size} werden ENDGUELTIG geleert (nicht in "
        "den Papierkorb).\n\nFortfahren?":
            "Cachés de: {names}\n\nse vaciarán DEFINITIVAMENTE hasta {size} (no a "
            "la papelera).\n\n¿Continuar?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt - App offen?).":
            "{n} archivos eliminados, {size} liberados.\n{skip} omitidos "
            "(bloqueados - ¿app abierta?).",
        "Papierkorb: {size} in {n} Objekten": "Papelera: {size} en {n} objetos",
        "Papierkorb: {size}.": "Papelera: {size}.",
        "Ruhezustand: AKTIV  (hiberfil.sys: {size})":
            "Hibernación: ACTIVA  (hiberfil.sys: {size})",
        "Ruhezustand: AUS (keine hiberfil.sys)":
            "Hibernación: DESACTIVADA (sin hiberfil.sys)",
        "hiberfil.sys ({size}) wird geloescht. Ruhezustand und Schnellstart sind "
        "danach aus (umkehrbar).\n\nFortfahren?":
            "Se eliminará hiberfil.sys ({size}). La hibernación y el inicio "
            "rápido quedarán desactivados (reversible).\n\n¿Continuar?",
        "Ruhezustand abgeschaltet, Platz freigegeben.":
            "Hibernación desactivada, espacio liberado.",
        "Ruhezustand wieder eingeschaltet.": "Hibernación reactivada.",
        "Fehler: {msg}": "Error: {msg}",
        "Der Pfad existiert nicht mehr:\n{path}": "La ruta ya no existe:\n{path}",
        "Konnte nicht oeffnen:\n{exc}": "No se pudo abrir:\n{exc}",
        "Wirklich {n} Ordner ({size}) in den Papierkorb verschieben?":
            "¿Mover realmente {n} carpetas ({size}) a la papelera?",
        "Wirklich {n} Dateien ({size}) in den Papierkorb?":
            "¿Mover realmente {n} archivos ({size}) a la papelera?",
        "DISM braucht Administrator-Rechte.\n\nJetzt als Administrator neu starten?":
            "DISM requiere permisos de administrador.\n\n¿Reiniciar como "
            "administrador ahora?",
        "Diese Aktion braucht Administrator-Rechte.\n\nJetzt als Administrator "
        "neu starten?":
            "Esta acción requiere permisos de administrador.\n\n¿Reiniciar como "
            "administrador ahora?",
        "Das Programm laeuft bereits mit Admin-Rechten.":
            "El programa ya se ejecuta con permisos de administrador.",
        "Neustart als Administrator wurde abgebrochen oder ist fehlgeschlagen.":
            "El reinicio como administrador se canceló o falló.",
        "Zum Leeren des Update-Caches sind Administrator-Rechte noetig.\nBitte "
        "'Als Administrator neu starten' verwenden.":
            "Se requieren permisos de administrador para vaciar la caché de "
            "Update.\nUse 'Reiniciar como administrador'.",
        "Es fehlten Administrator-Rechte. Bitte als Administrator neu starten.":
            "Faltaban permisos de administrador. Reinicie como administrador.",
        "Heruntergeladene Update-Pakete werden ENDGUELTIG geloescht.\nDie "
        "Update-Dienste werden kurz angehalten und danach wieder gestartet.\n\n"
        "Fortfahren?":
            "Los paquetes de actualización descargados se eliminan "
            "DEFINITIVAMENTE.\nLos servicios de Update se detienen brevemente y "
            "luego se reinician.\n\n¿Continuar?",
        "Update-Cache wirklich endgueltig leeren?":
            "¿Vaciar definitivamente la caché de Update?",
        "Temp-Dateien wirklich endgueltig loeschen?":
            "¿Eliminar definitivamente los archivos temporales?",
        "Ausgewaehlte Caches wirklich leeren?":
            "¿Vaciar realmente las cachés seleccionadas?",
        "Der gesamte Papierkorb wird ENDGUELTIG geleert (alle Laufwerke). "
        "Danach ist eine Wiederherstellung nicht mehr moeglich.\n\nFortfahren?":
            "Toda la papelera se vacía DEFINITIVAMENTE (todas las unidades). "
            "Después ya no es posible la recuperación.\n\n¿Continuar?",
        "Es wird die Windows-Datenträgerbereinigung (cleanmgr) mit "
        "Administrator-Rechten gestartet.\n\nDort 'Vorherige Windows-"
        "Installation(en)' anhaken und auf OK klicken - Windows entfernt "
        "Windows.old dann sicher selbst.\n\nTipp: Hier lassen sich auch weitere "
        "Systemreste anhaken (Absturz-Dumps, Delivery-Optimization, "
        "Update-Bereinigung).\n\nFortfahren?":
            "Se inicia el Liberador de espacio de Windows (cleanmgr) con permisos "
            "de administrador.\n\nMarque ahí 'Instalación(es) anterior(es) de "
            "Windows' y haga clic en Aceptar; Windows eliminará Windows.old de "
            "forma segura.\n\nConsejo: aquí también puede marcar otros restos del "
            "sistema (volcados de memoria, Delivery Optimization, limpieza de "
            "Update).\n\n¿Continuar?",
        "Konnte die Datenträgerbereinigung nicht starten (evtl. UAC "
        "abgebrochen). Alternativ ueber 'Speicher-Einstellungen'.":
            "No se pudo iniciar el Liberador de espacio (¿UAC cancelado?). "
            "Alternativamente, use 'Ajustes de almacenamiento'.",
        "Datenträgerbereinigung gestartet - bitte dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "Liberador de espacio iniciado - marque ahí 'Instalación(es) "
            "anterior(es) de Windows'.",
        "Analysiere Komponentenspeicher ... bitte warten.\n\nSolange die blaue "
        "Anzeige sich bewegt, laeuft der Vorgang - das Fenster bitte NICHT "
        "schliessen.":
            "Analizando el almacén de componentes ... espere.\n\nMientras la "
            "barra azul se mueva, la operación está en curso - no cierre la "
            "ventana.",
        "Bereinige Komponentenspeicher ... das kann 10-20 Minuten dauern.\n\n"
        "Solange die blaue Anzeige sich bewegt, laeuft der Vorgang - das Fenster "
        "bitte NICHT schliessen und warten. Es ist NICHT eingefroren.":
            "Limpiando el almacén de componentes ... puede tardar 10-20 "
            "minutos.\n\nMientras la barra azul se mueva, la operación está en "
            "curso - no cierre la ventana y espere. NO está bloqueada.",
        "vor {n} Tagen": "hace {n} días",
        "vor {n} Monaten": "hace {n} meses",
        "vor {n} Jahren": "hace {n} años",
        "\n\nACHTUNG ResetBase: installierte Updates lassen sich danach NICHT "
        "mehr deinstallieren.":
            "\n\nATENCIÓN ResetBase: las actualizaciones instaladas ya NO se "
            "podrán desinstalar después.",
        "DISM raeumt jetzt den WinSxS-Speicher auf.\n\nWICHTIG: Das kann 10-20 "
        "Minuten dauern und zeigt KEINEN Fortschritt in Prozent. Das Fenster "
        "bitte offen lassen und warten - es ist nicht eingefroren.{extra}\n\n"
        "Fortfahren?":
            "DISM limpiará ahora el almacén WinSxS.\n\nIMPORTANTE: puede tardar "
            "10-20 minutos y NO muestra progreso en porcentaje. Deje la ventana "
            "abierta y espere - no está bloqueada.{extra}\n\n¿Continuar?",
    },

    "pl": {
        "CleanSweep  -  Speicherplatz aufraeumen": "CleanSweep  -  Zwolnij miejsce na dysku",
        "Speicherplatz finden und sicher freigeben": "Znajdź i bezpiecznie zwolnij miejsce",
        "Bereit.": "Gotowe.",
        "Sprache": "Język",
        "Beginner": "Początkujący",
        "Expert": "Ekspert",
        "Modus:": "Tryb:",
        "♥ Unterstuetzen": "♥ Wesprzyj",
        "Entwicklung mit einer PayPal-Spende unterstuetzen":
            "Wesprzyj rozwój darowizną przez PayPal",
        "Spendenlink ist noch nicht eingetragen.\n\nBitte in gui.py die Variable "
        "DONATE_URL setzen.":
            "Link do darowizny nie jest jeszcze ustawiony.\n\nUstaw zmienną "
            "DONATE_URL w gui.py.",
        "  Verwaiste Ordner  ": "  Osierocone foldery  ",
        "  Temp-Dateien  ": "  Pliki tymczasowe  ",
        "  Grosse Dateien  ": "  Duże pliki  ",
        "  Windows-Update  ": "  Windows Update  ",
        "  Windows.old  ": "  Windows.old  ",
        "  Caches  ": "  Pamięci podręczne  ",
        "  System  ": "  System  ",
        "Scan starten": "Rozpocznij skanowanie",
        "Auswahl in Papierkorb": "Zaznaczone do kosza",
        "Mindest-Sicherheit:": "Min. pewność:",
        "ungenutzt seit (Monate):": "nieużywane od (miesięcy):",
        "Temp scannen": "Skanuj tymczasowe",
        "Temp leeren (endgueltig)": "Wyczyść tymczasowe (trwale)",
        "nur aelter als (Tage):": "tylko starsze niż (dni):",
        "Grosse Dateien suchen": "Znajdź duże pliki",
        "ab Groesse (MB):": "min. rozmiar (MB):",
        "Update-Cache scannen": "Skanuj pamięć Update",
        "Update-Cache leeren": "Wyczyść pamięć Update",
        "Als Administrator neu starten": "Uruchom ponownie jako administrator",
        "Analysieren": "Analizuj",
        "Bereinigen": "Wyczyść",
        "ResetBase (gruendlicher)": "ResetBase (dokładniej)",
        "Windows.old pruefen": "Sprawdź Windows.old",
        "Datenträgerbereinigung oeffnen (Windows.old u.a. Systemreste)":
            "Otwórz Oczyszczanie dysku (Windows.old i inne pozostałości)",
        "Speicher-Einstellungen": "Ustawienia pamięci",
        "Caches suchen": "Znajdź pamięci podręczne",
        "Auswahl leeren (endgueltig)": "Wyczyść zaznaczone (trwale)",
        "Papierkorb pruefen": "Sprawdź kosz",
        "Papierkorb leeren": "Opróżnij kosz",
        "Status pruefen": "Sprawdź stan",
        "Ruhezustand abschalten": "Wyłącz hibernację",
        "Ruhezustand einschalten": "Włącz hibernację",
        "Sicher": "Pewn.",
        "Groesse": "Rozmiar",
        "Zuletzt genutzt": "Ostatnio używane",
        "Kategorie": "Kategoria",
        "Ordner": "Folder",
        "Warnung": "Ostrzeżenie",
        "Dateien": "Pliki",
        "Temp-Ordner": "Folder tymczasowy",
        "Datei": "Plik",
        "Anzahl": "Liczba",
        "Programm": "Program",
        "Beispielpfad": "Przykładowa ścieżka",
        "Springe in den Ordner": "Przejdź do folderu",
        "Komponentenspeicher (WinSxS) - DISM": "Magazyn składników (WinSxS) - DISM",
        "Papierkorb": "Kosz",
        "Ruhezustand (hiberfil.sys)": "Hibernacja (hiberfil.sys)",
        "Vorgang laeuft - bitte warten (die Anzeige bewegt sich):":
            "Operacja w toku - proszę czekać (pasek się porusza):",
        "Keine Auswahl": "Brak zaznaczenia",
        "Abgelehnt": "Odrzucono",
        "Nicht gefunden": "Nie znaleziono",
        "Fehler": "Błąd",
        "Fertig": "Gotowe",
        "Sind Sie sicher?": "Czy na pewno?",
        "In den Papierkorb verschieben?": "Przenieść do kosza?",
        "Administrator noetig": "Wymagany administrator",
        "Bereits Administrator": "Już administrator",
        "Fehlgeschlagen": "Niepowodzenie",
        "Komponentenspeicher bereinigen?": "Wyczyścić magazyn składników?",
        "Update-Cache leeren?": "Wyczyścić pamięć Update?",
        "Temp-Dateien endgueltig loeschen?": "Trwale usunąć pliki tymczasowe?",
        "Caches endgueltig leeren?": "Trwale wyczyścić pamięci podręczne?",
        "Papierkorb leeren?": "Opróżnić kosz?",
        "Datenträgerbereinigung starten?": "Uruchomić Oczyszczanie dysku?",
        "Ruhezustand abschalten?": "Wyłączyć hibernację?",
        "Bitte zuerst Zeilen auswaehlen.": "Najpierw zaznacz wiersze.",
        "Bitte zuerst Dateien auswaehlen.": "Najpierw zaznacz pliki.",
        "Nichts Sicheres ausgewaehlt.": "Nie wybrano niczego bezpiecznego.",
        "Abgebrochen.": "Anulowano.",
        "Nicht bestaetigt.": "Nie potwierdzono.",
        "Diese werden NICHT geloescht:\n\n": "Te NIE zostaną usunięte:\n\n",
        "Scanne alle Laufwerke (das kann eine Weile dauern) ...":
            "Skanowanie wszystkich dysków (może chwilę potrwać) ...",
        "Scanne Temp-Ordner ...": "Skanowanie folderów tymczasowych ...",
        "Loesche Temp-Dateien ...": "Usuwanie plików tymczasowych ...",
        "Durchsuche alle Laufwerke nach grossen Dateien (dauert) ...":
            "Przeszukiwanie wszystkich dysków w poszukiwaniu dużych plików (trwa) ...",
        "Suche Cache-Ordner ...": "Wyszukiwanie folderów pamięci podręcznej ...",
        "Leere Caches ...": "Czyszczenie pamięci podręcznych ...",
        "Scanne Windows-Update-Cache ...": "Skanowanie pamięci Windows Update ...",
        "Stoppe Dienste und leere Cache ...":
            "Zatrzymywanie usług i czyszczenie pamięci ...",
        "Pruefe Windows.old (Groesse berechnen kann dauern) ...":
            "Sprawdzanie Windows.old (obliczanie rozmiaru może potrwać) ...",
        "Kein Windows.old gefunden.": "Nie znaleziono Windows.old.",
        "Kein 'Windows.old' vorhanden - nichts zu tun. :)":
            "Brak 'Windows.old' - nic do zrobienia. :)",
        "Ruhezustand-Status geprueft.": "Sprawdzono stan hibernacji.",
        "DISM analysiert den Komponentenspeicher ...":
            "DISM analizuje magazyn składników ...",
        "DISM bereinigt den Komponentenspeicher ...":
            "DISM czyści magazyn składników ...",
        "DISM fertig.": "DISM zakończony.",
        "DISM meldete einen Fehler.": "DISM zgłosił błąd.",
        "Papierkorb geleert.": "Kosz opróżniony.",
        "Papierkorb war leer oder konnte nicht geleert werden.":
            "Kosz był pusty lub nie udało się go opróżnić.",
        "unbekannt": "nieznane",
        "heute": "dzisiaj",
        "Geschuetzter System-/Wurzelordner": "Chroniony folder systemowy/główny",
        "Das ist eine Laufwerks-Wurzel": "To jest katalog główny dysku",
        "Liegt im Windows-Systemordner": "Znajduje się w folderze systemowym Windows",
        "Steht auf der Schutzliste (geschuetzter Name)":
            "Na liście ochrony (chroniona nazwa)",
        "Pfad existiert nicht (mehr)": "Ścieżka już nie istnieje",
        "Kein Ordner": "To nie folder",
        "Datei existiert nicht (mehr)": "Plik już nie istnieje",
        "System-/Auslagerungsdatei": "Plik systemowy/wymiany",
        "SEHR GROSS - erst pruefen, ob aktives Spiel/Programm!":
            "BARDZO DUŻY - najpierw sprawdź, czy to aktywna gra/program!",
        "GROSS - evtl. aktives Programm (Steam/Epic?), bitte pruefen":
            "DUŻY - być może aktywny program (Steam/Epic?), sprawdź",
        "ja": "tak",
        "nein (zum Leeren noetig)": "nie (wymagane do opróżnienia)",
        "Erfolgreich.": "Powodzenie.",
        "Fehler.": "Błąd.",
        "Temp-Dateien werden ENDGUELTIG geloescht (nicht in den Papierkorb), "
        "damit der Platz wirklich frei wird. Gesperrte Dateien bleiben "
        "unangetastet.":
            "Pliki tymczasowe są usuwane TRWALE (nie do kosza), aby naprawdę "
            "zwolnić miejsce. Zablokowane pliki pozostają nietknięte.",
        "Findet die groessten Einzeldateien (z.B. alte Videos, ISO-Dateien). "
        "Amber = kuerzlich genutzt (evtl. aktives Spiel/Programm). Loeschen geht "
        "in den Papierkorb.":
            "Znajduje największe pojedyncze pliki (np. stare filmy, pliki ISO). "
            "Bursztynowy = niedawno używany (możliwa aktywna gra/program). "
            "Usuwanie trafia do kosza.",
        "Heruntergeladene Windows-Update-Pakete (SoftwareDistribution\\Download) "
        "sind nach der Installation nutzlos. Sie werden ENDGUELTIG geloescht "
        "und von Windows bei Bedarf neu angelegt.":
            "Pobrane pakiety Windows Update (SoftwareDistribution\\Download) są "
            "bezużyteczne po instalacji. Są usuwane TRWALE, a Windows odtwarza je "
            "w razie potrzeby.",
        "Raeumt alte, durch Updates ersetzte Windows-Komponenten gruendlicher "
        "auf als die Datentraegerbereinigung. '/ResetBase' entfernt auch "
        "ersetzte Versionen endgueltig - danach lassen sich installierte Updates "
        "aber NICHT mehr deinstallieren. Braucht Admin und kann einige Minuten "
        "dauern.":
            "Czyści stare składniki Windows zastąpione przez aktualizacje "
            "dokładniej niż Oczyszczanie dysku. '/ResetBase' usuwa też trwale "
            "zastąpione wersje - po tym zainstalowanych aktualizacji NIE można "
            "już odinstalować. Wymaga administratora i może potrwać kilka minut.",
        "WICHTIG: WinSxS bleibt IMMER mehrere GB gross (vieles ist mit Windows "
        "geteilt) - das ist normal. Und 'empfohlen: Ja' steht schon ab 1 "
        "ersetzten Paket - auf einem aktuellen Windows fast immer. Massgeblich "
        "ist die Anzahl 'bereinigbarer Pakete' (0-2 = gesund), NICHT die "
        "'empfohlen'-Zeile.":
            "WAŻNE: WinSxS ZAWSZE zajmuje kilka GB (wiele jest współdzielone z "
            "Windows) - to normalne. A 'zalecane: Tak' pojawia się już przy 1 "
            "zastąpionym pakiecie - na aktualnym Windows niemal zawsze. Istotna "
            "jest liczba 'pakietów do odzyskania' (0-2 = zdrowo), a NIE wiersz "
            "'zalecane'.",
        "'Windows.old' enthaelt die vorherige Windows-Version nach einem Upgrade "
        "(oft 20-70 GB). Es laesst sich NICHT normal loeschen, weil es dem "
        "System gehoert (TrustedInstaller-Sperre). Der sichere Weg ist die "
        "Windows-Datenträgerbereinigung: dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "'Windows.old' zawiera poprzednią wersję Windows po aktualizacji "
            "(często 20-70 GB). NIE można go usunąć normalnie, bo należy do "
            "systemu (blokada TrustedInstaller). Bezpieczna droga to Oczyszczanie "
            "dysku Windows: zaznacz tam 'Poprzednie instalacje systemu Windows'.",
        "Cache-Ordner von Browsern und Apps. Werden automatisch neu aufgebaut "
        "und daher ENDGUELTIG geleert. Fuer das beste Ergebnis die jeweilige App "
        "vorher schliessen (gesperrte Dateien werden sonst uebersprungen).":
            "Foldery pamięci podręcznej przeglądarek i aplikacji. Są odtwarzane "
            "automatycznie, dlatego czyszczone TRWALE. Dla najlepszego efektu "
            "zamknij wcześniej daną aplikację (w przeciwnym razie zablokowane "
            "pliki są pomijane).",
        "CleanSweep verschiebt Ordner/Dateien in den Papierkorb. Der Platz wird "
        "erst frei, wenn er geleert wird.":
            "CleanSweep przenosi foldery/pliki do kosza. Miejsce zwalnia się "
            "dopiero po jego opróżnieniu.",
        "Der Ruhezustand belegt eine Datei so gross wie dein RAM (oft 8-32 GB). "
        "Abschalten gibt diesen Platz frei - danach gibt es keinen Ruhezustand/"
        "Schnellstart mehr (jederzeit umkehrbar). Braucht Admin-Rechte.":
            "Hibernacja zajmuje plik wielkości RAM (często 8-32 GB). Wyłączenie "
            "zwalnia to miejsce - potem nie ma hibernacji/szybkiego rozruchu "
            "(odwracalne w każdej chwili). Wymaga uprawnień administratora.",
        "Fehler: {err}": "Błąd: {err}",
        "Hinweis: Zum Leeren werden Administrator-Rechte benoetigt. ":
            "Uwaga: do opróżnienia wymagane są uprawnienia administratora. ",
        "... und {n} weitere": "... i jeszcze {n}",
        "{n} Kandidaten  |  potentiell {size} frei. Zeilen auswaehlen (Strg/Shift).":
            "{n} kandydatów  |  potencjalnie {size} wolne. Zaznacz wiersze (Ctrl/Shift).",
        "\n\nACHTUNG: Mindestens ein grosser Ordner koennte ein aktives\n"
        "Spiel/Programm sein!":
            "\n\nUWAGA: Co najmniej jeden duży folder może być aktywną\n"
            "grą/programem!",
        "{n} Ordner -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} folderów -> KOSZ (do odzyskania).\nZwolni się: {size}.\n\n"
            "{preview}{warn}\n\nKontynuować?",
        "{ok} Ordner in den Papierkorb verschoben, {size} frei. Protokoll: {log}":
            "{ok} folderów przeniesiono do kosza, {size} wolne. Dziennik: {log}",
        "Temp gesamt: {size}. 'Temp leeren' gibt diesen Platz frei.":
            "Tymczasowe łącznie: {size}. 'Wyczyść tymczasowe' zwalnia to miejsce.",
        "\n(nur Dateien aelter als {days} Tage)":
            "\n(tylko pliki starsze niż {days} dni)",
        "Temporaere Dateien werden ENDGUELTIG geloescht (NICHT in den "
        "Papierkorb).{age}\n\nGeschaetzt frei: bis zu {size}.\nGesperrte/benutzte "
        "Dateien werden uebersprungen.\n\nFortfahren?":
            "Pliki tymczasowe zostaną usunięte TRWALE (NIE do kosza).{age}\n\n"
            "Szacowane zwolnienie: do {size}.\nZablokowane/używane pliki są "
            "pomijane.\n\nKontynuować?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt/zu jung).":
            "Usunięto {n} plików, zwolniono {size}.\n{skip} pominięto "
            "(zablokowane/zbyt nowe).",
        "{n} grosse Dateien  |  zusammen {size}. Amber = kuerzlich genutzt.":
            "{n} dużych plików  |  łącznie {size}. Bursztynowy = niedawno używane.",
        "\n\nACHTUNG: Mindestens eine Datei wurde kuerzlich genutzt -\n"
        "evtl. ein aktives Spiel/Programm!":
            "\n\nUWAGA: Co najmniej jeden plik był niedawno używany -\n"
            "być może aktywna gra/program!",
        "{n} Dateien -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} plików -> KOSZ (do odzyskania).\nZwolni się: {size}.\n\n"
            "{preview}{warn}\n\nKontynuować?",
        "{ok} Dateien in den Papierkorb verschoben, {size} frei.":
            "{ok} plików przeniesiono do kosza, {size} wolne.",
        "Ordner nicht vorhanden:\n{path}": "Folder nie istnieje:\n{path}",
        "Groesse:  {size}   ({n} Dateien)\nOrdner:   {path}\nAdmin:    {admin}":
            "Rozmiar: {size}   ({n} plików)\nFolder:  {path}\nAdmin:   {admin}",
        "Update-Cache: {size}.": "Pamięć Update: {size}.",
        "Dienste wurden gestoppt und neu gestartet.":
            "Usługi zostały zatrzymane i uruchomione ponownie.",
        "Hinweis: Dienste konnten nicht gestoppt werden - gesperrte Dateien "
        "wurden uebersprungen.":
            "Uwaga: nie udało się zatrzymać usług - zablokowane pliki pominięto.",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen.\n\n{svc}":
            "Usunięto {n} plików, zwolniono {size}.\n{skip} pominięto.\n\n{svc}",
        "Windows.old gefunden:  {size}\nPfad:  {drive}\\Windows.old\n\nKlicke "
        "'Mit Datenträgerbereinigung entfernen' und hake dort\n'Vorherige "
        "Windows-Installation(en)' an.":
            "Znaleziono Windows.old:  {size}\nŚcieżka:  {drive}\\Windows.old\n\n"
            "Kliknij 'Otwórz Oczyszczanie dysku' i zaznacz\n'Poprzednie "
            "instalacje systemu Windows'.",
        "Windows.old: {size} - ueber die Datenträgerbereinigung entfernbar.":
            "Windows.old: {size} - usuwalny przez Oczyszczanie dysku.",
        "{n} Programme mit Cache  |  zusammen {size}. Zeilen auswaehlen (Strg/Shift).":
            "{n} programów z pamięcią podręczną  |  łącznie {size}. Zaznacz wiersze (Ctrl/Shift).",
        "Caches von: {names}\n\nbis zu {size} werden ENDGUELTIG geleert (nicht in "
        "den Papierkorb).\n\nFortfahren?":
            "Pamięci podręczne: {names}\n\nzostanie TRWALE wyczyszczone do {size} "
            "(nie do kosza).\n\nKontynuować?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt - App offen?).":
            "Usunięto {n} plików, zwolniono {size}.\n{skip} pominięto "
            "(zablokowane - aplikacja otwarta?).",
        "Papierkorb: {size} in {n} Objekten": "Kosz: {size} w {n} obiektach",
        "Papierkorb: {size}.": "Kosz: {size}.",
        "Ruhezustand: AKTIV  (hiberfil.sys: {size})":
            "Hibernacja: AKTYWNA  (hiberfil.sys: {size})",
        "Ruhezustand: AUS (keine hiberfil.sys)":
            "Hibernacja: WYŁĄCZONA (brak hiberfil.sys)",
        "hiberfil.sys ({size}) wird geloescht. Ruhezustand und Schnellstart sind "
        "danach aus (umkehrbar).\n\nFortfahren?":
            "hiberfil.sys ({size}) zostanie usunięty. Hibernacja i szybki rozruch "
            "będą potem wyłączone (odwracalne).\n\nKontynuować?",
        "Ruhezustand abgeschaltet, Platz freigegeben.":
            "Hibernacja wyłączona, miejsce zwolnione.",
        "Ruhezustand wieder eingeschaltet.": "Hibernacja ponownie włączona.",
        "Fehler: {msg}": "Błąd: {msg}",
        "Der Pfad existiert nicht mehr:\n{path}": "Ścieżka już nie istnieje:\n{path}",
        "Konnte nicht oeffnen:\n{exc}": "Nie udało się otworzyć:\n{exc}",
        "Wirklich {n} Ordner ({size}) in den Papierkorb verschieben?":
            "Czy na pewno przenieść {n} folderów ({size}) do kosza?",
        "Wirklich {n} Dateien ({size}) in den Papierkorb?":
            "Czy na pewno przenieść {n} plików ({size}) do kosza?",
        "DISM braucht Administrator-Rechte.\n\nJetzt als Administrator neu starten?":
            "DISM wymaga uprawnień administratora.\n\nUruchomić ponownie jako "
            "administrator?",
        "Diese Aktion braucht Administrator-Rechte.\n\nJetzt als Administrator "
        "neu starten?":
            "Ta akcja wymaga uprawnień administratora.\n\nUruchomić ponownie jako "
            "administrator?",
        "Das Programm laeuft bereits mit Admin-Rechten.":
            "Program już działa z uprawnieniami administratora.",
        "Neustart als Administrator wurde abgebrochen oder ist fehlgeschlagen.":
            "Ponowne uruchomienie jako administrator anulowano lub nie powiodło się.",
        "Zum Leeren des Update-Caches sind Administrator-Rechte noetig.\nBitte "
        "'Als Administrator neu starten' verwenden.":
            "Do opróżnienia pamięci Update wymagane są uprawnienia "
            "administratora.\nUżyj 'Uruchom ponownie jako administrator'.",
        "Es fehlten Administrator-Rechte. Bitte als Administrator neu starten.":
            "Brakowało uprawnień administratora. Uruchom ponownie jako administrator.",
        "Heruntergeladene Update-Pakete werden ENDGUELTIG geloescht.\nDie "
        "Update-Dienste werden kurz angehalten und danach wieder gestartet.\n\n"
        "Fortfahren?":
            "Pobrane pakiety aktualizacji zostaną usunięte TRWALE.\nUsługi Update "
            "zostaną na chwilę zatrzymane i ponownie uruchomione.\n\nKontynuować?",
        "Update-Cache wirklich endgueltig leeren?":
            "Na pewno trwale wyczyścić pamięć Update?",
        "Temp-Dateien wirklich endgueltig loeschen?":
            "Na pewno trwale usunąć pliki tymczasowe?",
        "Ausgewaehlte Caches wirklich leeren?":
            "Na pewno wyczyścić wybrane pamięci podręczne?",
        "Der gesamte Papierkorb wird ENDGUELTIG geleert (alle Laufwerke). "
        "Danach ist eine Wiederherstellung nicht mehr moeglich.\n\nFortfahren?":
            "Cały kosz zostanie TRWALE opróżniony (wszystkie dyski). Potem "
            "odzyskanie nie będzie możliwe.\n\nKontynuować?",
        "Es wird die Windows-Datenträgerbereinigung (cleanmgr) mit "
        "Administrator-Rechten gestartet.\n\nDort 'Vorherige Windows-"
        "Installation(en)' anhaken und auf OK klicken - Windows entfernt "
        "Windows.old dann sicher selbst.\n\nTipp: Hier lassen sich auch weitere "
        "Systemreste anhaken (Absturz-Dumps, Delivery-Optimization, "
        "Update-Bereinigung).\n\nFortfahren?":
            "Zostanie uruchomione Oczyszczanie dysku Windows (cleanmgr) z "
            "uprawnieniami administratora.\n\nZaznacz tam 'Poprzednie instalacje "
            "systemu Windows' i kliknij OK - Windows bezpiecznie usunie "
            "Windows.old.\n\nWskazówka: możesz tu też zaznaczyć inne pozostałości "
            "systemu (zrzuty awaryjne, Delivery Optimization, czyszczenie "
            "Update).\n\nKontynuować?",
        "Konnte die Datenträgerbereinigung nicht starten (evtl. UAC "
        "abgebrochen). Alternativ ueber 'Speicher-Einstellungen'.":
            "Nie udało się uruchomić Oczyszczania dysku (anulowano UAC?). "
            "Alternatywnie użyj 'Ustawienia pamięci'.",
        "Datenträgerbereinigung gestartet - bitte dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "Uruchomiono Oczyszczanie dysku - zaznacz tam 'Poprzednie instalacje "
            "systemu Windows'.",
        "Analysiere Komponentenspeicher ... bitte warten.\n\nSolange die blaue "
        "Anzeige sich bewegt, laeuft der Vorgang - das Fenster bitte NICHT "
        "schliessen.":
            "Analizowanie magazynu składników ... proszę czekać.\n\nDopóki "
            "niebieski pasek się porusza, operacja trwa - nie zamykaj okna.",
        "Bereinige Komponentenspeicher ... das kann 10-20 Minuten dauern.\n\n"
        "Solange die blaue Anzeige sich bewegt, laeuft der Vorgang - das Fenster "
        "bitte NICHT schliessen und warten. Es ist NICHT eingefroren.":
            "Czyszczenie magazynu składników ... może potrwać 10-20 minut.\n\n"
            "Dopóki niebieski pasek się porusza, operacja trwa - nie zamykaj okna "
            "i czekaj. Program NIE jest zawieszony.",
        "vor {n} Tagen": "{n} dni temu",
        "vor {n} Monaten": "{n} mies. temu",
        "vor {n} Jahren": "{n} lat temu",
        "\n\nACHTUNG ResetBase: installierte Updates lassen sich danach NICHT "
        "mehr deinstallieren.":
            "\n\nUWAGA ResetBase: zainstalowanych aktualizacji NIE będzie już "
            "można odinstalować.",
        "DISM raeumt jetzt den WinSxS-Speicher auf.\n\nWICHTIG: Das kann 10-20 "
        "Minuten dauern und zeigt KEINEN Fortschritt in Prozent. Das Fenster "
        "bitte offen lassen und warten - es ist nicht eingefroren.{extra}\n\n"
        "Fortfahren?":
            "DISM wyczyści teraz magazyn WinSxS.\n\nWAŻNE: może to potrwać 10-20 "
            "minut i NIE pokazuje postępu w procentach. Zostaw okno otwarte i "
            "czekaj - nie jest zawieszone.{extra}\n\nKontynuować?",
    },

    "fr": {
        "CleanSweep  -  Speicherplatz aufraeumen": "CleanSweep  -  Libérer de l'espace disque",
        "Speicherplatz finden und sicher freigeben": "Trouver et libérer de l'espace en toute sécurité",
        "Bereit.": "Prêt.",
        "Sprache": "Langue",
        "Beginner": "Débutant",
        "Expert": "Expert",
        "Modus:": "Mode :",
        "♥ Unterstuetzen": "♥ Soutenir",
        "Entwicklung mit einer PayPal-Spende unterstuetzen":
            "Soutenez le développement avec un don PayPal",
        "Spendenlink ist noch nicht eingetragen.\n\nBitte in gui.py die Variable "
        "DONATE_URL setzen.":
            "Le lien de don n'est pas encore défini.\n\nVeuillez définir la "
            "variable DONATE_URL dans gui.py.",
        "  Verwaiste Ordner  ": "  Dossiers orphelins  ",
        "  Temp-Dateien  ": "  Fichiers temporaires  ",
        "  Grosse Dateien  ": "  Gros fichiers  ",
        "  Windows-Update  ": "  Windows Update  ",
        "  Windows.old  ": "  Windows.old  ",
        "  Caches  ": "  Caches  ",
        "  System  ": "  Système  ",
        "Scan starten": "Lancer l'analyse",
        "Auswahl in Papierkorb": "Sélection vers la corbeille",
        "Mindest-Sicherheit:": "Confiance min. :",
        "ungenutzt seit (Monate):": "inutilisé depuis (mois) :",
        "Temp scannen": "Analyser temp.",
        "Temp leeren (endgueltig)": "Vider temp. (définitif)",
        "nur aelter als (Tage):": "seulement plus vieux que (jours) :",
        "Grosse Dateien suchen": "Trouver les gros fichiers",
        "ab Groesse (MB):": "taille min. (Mo) :",
        "Update-Cache scannen": "Analyser le cache Update",
        "Update-Cache leeren": "Vider le cache Update",
        "Als Administrator neu starten": "Redémarrer en administrateur",
        "Analysieren": "Analyser",
        "Bereinigen": "Nettoyer",
        "ResetBase (gruendlicher)": "ResetBase (plus complet)",
        "Windows.old pruefen": "Vérifier Windows.old",
        "Datenträgerbereinigung oeffnen (Windows.old u.a. Systemreste)":
            "Ouvrir le Nettoyage de disque (Windows.old et autres résidus)",
        "Speicher-Einstellungen": "Paramètres de stockage",
        "Caches suchen": "Trouver les caches",
        "Auswahl leeren (endgueltig)": "Vider la sélection (définitif)",
        "Papierkorb pruefen": "Vérifier la corbeille",
        "Papierkorb leeren": "Vider la corbeille",
        "Status pruefen": "Vérifier l'état",
        "Ruhezustand abschalten": "Désactiver la veille prolongée",
        "Ruhezustand einschalten": "Activer la veille prolongée",
        "Sicher": "Conf.",
        "Groesse": "Taille",
        "Zuletzt genutzt": "Dernière utilisation",
        "Kategorie": "Catégorie",
        "Ordner": "Dossier",
        "Warnung": "Avertissement",
        "Dateien": "Fichiers",
        "Temp-Ordner": "Dossier temporaire",
        "Datei": "Fichier",
        "Anzahl": "Nombre",
        "Programm": "Programme",
        "Beispielpfad": "Chemin d'exemple",
        "Springe in den Ordner": "Aller au dossier",
        "Komponentenspeicher (WinSxS) - DISM": "Magasin de composants (WinSxS) - DISM",
        "Papierkorb": "Corbeille",
        "Ruhezustand (hiberfil.sys)": "Veille prolongée (hiberfil.sys)",
        "Vorgang laeuft - bitte warten (die Anzeige bewegt sich):":
            "Opération en cours - veuillez patienter (la barre bouge) :",
        "Keine Auswahl": "Aucune sélection",
        "Abgelehnt": "Refusé",
        "Nicht gefunden": "Introuvable",
        "Fehler": "Erreur",
        "Fertig": "Terminé",
        "Sind Sie sicher?": "Êtes-vous sûr ?",
        "In den Papierkorb verschieben?": "Déplacer vers la corbeille ?",
        "Administrator noetig": "Administrateur requis",
        "Bereits Administrator": "Déjà administrateur",
        "Fehlgeschlagen": "Échec",
        "Komponentenspeicher bereinigen?": "Nettoyer le magasin de composants ?",
        "Update-Cache leeren?": "Vider le cache Update ?",
        "Temp-Dateien endgueltig loeschen?": "Supprimer définitivement les fichiers temporaires ?",
        "Caches endgueltig leeren?": "Vider définitivement les caches ?",
        "Papierkorb leeren?": "Vider la corbeille ?",
        "Datenträgerbereinigung starten?": "Lancer le Nettoyage de disque ?",
        "Ruhezustand abschalten?": "Désactiver la veille prolongée ?",
        "Bitte zuerst Zeilen auswaehlen.": "Veuillez d'abord sélectionner des lignes.",
        "Bitte zuerst Dateien auswaehlen.": "Veuillez d'abord sélectionner des fichiers.",
        "Nichts Sicheres ausgewaehlt.": "Rien de sûr sélectionné.",
        "Abgebrochen.": "Annulé.",
        "Nicht bestaetigt.": "Non confirmé.",
        "Diese werden NICHT geloescht:\n\n": "Ceux-ci ne seront PAS supprimés :\n\n",
        "Scanne alle Laufwerke (das kann eine Weile dauern) ...":
            "Analyse de tous les lecteurs (cela peut prendre du temps) ...",
        "Scanne Temp-Ordner ...": "Analyse des dossiers temporaires ...",
        "Loesche Temp-Dateien ...": "Suppression des fichiers temporaires ...",
        "Durchsuche alle Laufwerke nach grossen Dateien (dauert) ...":
            "Recherche de gros fichiers sur tous les lecteurs (cela dure) ...",
        "Suche Cache-Ordner ...": "Recherche des dossiers de cache ...",
        "Leere Caches ...": "Vidage des caches ...",
        "Scanne Windows-Update-Cache ...": "Analyse du cache Windows Update ...",
        "Stoppe Dienste und leere Cache ...":
            "Arrêt des services et vidage du cache ...",
        "Pruefe Windows.old (Groesse berechnen kann dauern) ...":
            "Vérification de Windows.old (le calcul de la taille peut durer) ...",
        "Kein Windows.old gefunden.": "Aucun Windows.old trouvé.",
        "Kein 'Windows.old' vorhanden - nichts zu tun. :)":
            "Pas de 'Windows.old' - rien à faire. :)",
        "Ruhezustand-Status geprueft.": "État de la veille prolongée vérifié.",
        "DISM analysiert den Komponentenspeicher ...":
            "DISM analyse le magasin de composants ...",
        "DISM bereinigt den Komponentenspeicher ...":
            "DISM nettoie le magasin de composants ...",
        "DISM fertig.": "DISM terminé.",
        "DISM meldete einen Fehler.": "DISM a signalé une erreur.",
        "Papierkorb geleert.": "Corbeille vidée.",
        "Papierkorb war leer oder konnte nicht geleert werden.":
            "La corbeille était vide ou n'a pas pu être vidée.",
        "unbekannt": "inconnu",
        "heute": "aujourd'hui",
        "Geschuetzter System-/Wurzelordner": "Dossier système/racine protégé",
        "Das ist eine Laufwerks-Wurzel": "C'est la racine d'un lecteur",
        "Liegt im Windows-Systemordner": "Se trouve dans le dossier système Windows",
        "Steht auf der Schutzliste (geschuetzter Name)":
            "Dans la liste de protection (nom protégé)",
        "Pfad existiert nicht (mehr)": "Le chemin n'existe plus",
        "Kein Ordner": "Pas un dossier",
        "Datei existiert nicht (mehr)": "Le fichier n'existe plus",
        "System-/Auslagerungsdatei": "Fichier système/d'échange",
        "SEHR GROSS - erst pruefen, ob aktives Spiel/Programm!":
            "TRÈS GROS - vérifiez d'abord s'il s'agit d'un jeu/programme actif !",
        "GROSS - evtl. aktives Programm (Steam/Epic?), bitte pruefen":
            "GROS - peut-être un programme actif (Steam/Epic ?), à vérifier",
        "ja": "oui",
        "nein (zum Leeren noetig)": "non (requis pour vider)",
        "Erfolgreich.": "Réussi.",
        "Fehler.": "Erreur.",
        "Temp-Dateien werden ENDGUELTIG geloescht (nicht in den Papierkorb), "
        "damit der Platz wirklich frei wird. Gesperrte Dateien bleiben "
        "unangetastet.":
            "Les fichiers temporaires sont supprimés DÉFINITIVEMENT (pas vers la "
            "corbeille) afin de libérer réellement l'espace. Les fichiers "
            "verrouillés ne sont pas touchés.",
        "Findet die groessten Einzeldateien (z.B. alte Videos, ISO-Dateien). "
        "Amber = kuerzlich genutzt (evtl. aktives Spiel/Programm). Loeschen geht "
        "in den Papierkorb.":
            "Trouve les plus gros fichiers individuels (p. ex. vieilles vidéos, "
            "fichiers ISO). Ambre = utilisé récemment (jeu/programme actif "
            "possible). La suppression va vers la corbeille.",
        "Heruntergeladene Windows-Update-Pakete (SoftwareDistribution\\Download) "
        "sind nach der Installation nutzlos. Sie werden ENDGUELTIG geloescht "
        "und von Windows bei Bedarf neu angelegt.":
            "Les paquets Windows Update téléchargés "
            "(SoftwareDistribution\\Download) sont inutiles après l'installation. "
            "Ils sont supprimés DÉFINITIVEMENT et recréés par Windows si "
            "nécessaire.",
        "Raeumt alte, durch Updates ersetzte Windows-Komponenten gruendlicher "
        "auf als die Datentraegerbereinigung. '/ResetBase' entfernt auch "
        "ersetzte Versionen endgueltig - danach lassen sich installierte Updates "
        "aber NICHT mehr deinstallieren. Braucht Admin und kann einige Minuten "
        "dauern.":
            "Nettoie les anciens composants Windows remplacés par des mises à "
            "jour plus en profondeur que le Nettoyage de disque. '/ResetBase' "
            "supprime aussi définitivement les versions remplacées - ensuite les "
            "mises à jour installées ne peuvent PLUS être désinstallées. "
            "Nécessite l'administrateur et peut durer quelques minutes.",
        "WICHTIG: WinSxS bleibt IMMER mehrere GB gross (vieles ist mit Windows "
        "geteilt) - das ist normal. Und 'empfohlen: Ja' steht schon ab 1 "
        "ersetzten Paket - auf einem aktuellen Windows fast immer. Massgeblich "
        "ist die Anzahl 'bereinigbarer Pakete' (0-2 = gesund), NICHT die "
        "'empfohlen'-Zeile.":
            "IMPORTANT : WinSxS fait TOUJOURS plusieurs Go (beaucoup est partagé "
            "avec Windows) - c'est normal. Et 'recommandé : Oui' apparaît dès 1 "
            "paquet remplacé - presque toujours sur un Windows à jour. Ce qui "
            "compte, c'est le nombre de 'paquets récupérables' (0-2 = sain), PAS "
            "la ligne 'recommandé'.",
        "'Windows.old' enthaelt die vorherige Windows-Version nach einem Upgrade "
        "(oft 20-70 GB). Es laesst sich NICHT normal loeschen, weil es dem "
        "System gehoert (TrustedInstaller-Sperre). Der sichere Weg ist die "
        "Windows-Datenträgerbereinigung: dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "'Windows.old' contient la version précédente de Windows après une "
            "mise à niveau (souvent 20-70 Go). Il ne peut PAS être supprimé "
            "normalement car il appartient au système (verrou TrustedInstaller). "
            "La voie sûre est le Nettoyage de disque Windows : cochez-y "
            "'Installation(s) Windows précédente(s)'.",
        "Cache-Ordner von Browsern und Apps. Werden automatisch neu aufgebaut "
        "und daher ENDGUELTIG geleert. Fuer das beste Ergebnis die jeweilige App "
        "vorher schliessen (gesperrte Dateien werden sonst uebersprungen).":
            "Dossiers de cache des navigateurs et applications. Ils sont "
            "reconstruits automatiquement, c'est pourquoi ils sont vidés "
            "DÉFINITIVEMENT. Pour un meilleur résultat, fermez d'abord "
            "l'application concernée (sinon les fichiers verrouillés sont "
            "ignorés).",
        "CleanSweep verschiebt Ordner/Dateien in den Papierkorb. Der Platz wird "
        "erst frei, wenn er geleert wird.":
            "CleanSweep déplace les dossiers/fichiers vers la corbeille. "
            "L'espace n'est libéré qu'une fois la corbeille vidée.",
        "Der Ruhezustand belegt eine Datei so gross wie dein RAM (oft 8-32 GB). "
        "Abschalten gibt diesen Platz frei - danach gibt es keinen Ruhezustand/"
        "Schnellstart mehr (jederzeit umkehrbar). Braucht Admin-Rechte.":
            "La veille prolongée occupe un fichier aussi grand que votre RAM "
            "(souvent 8-32 Go). La désactiver libère cet espace - ensuite il n'y "
            "a plus de veille prolongée/démarrage rapide (réversible à tout "
            "moment). Nécessite des droits administrateur.",
        "Fehler: {err}": "Erreur : {err}",
        "Hinweis: Zum Leeren werden Administrator-Rechte benoetigt. ":
            "Remarque : des droits administrateur sont requis pour vider. ",
        "... und {n} weitere": "... et {n} de plus",
        "{n} Kandidaten  |  potentiell {size} frei. Zeilen auswaehlen (Strg/Shift).":
            "{n} candidats  |  potentiellement {size} libres. Sélectionnez des lignes (Ctrl/Maj).",
        "\n\nACHTUNG: Mindestens ein grosser Ordner koennte ein aktives\n"
        "Spiel/Programm sein!":
            "\n\nATTENTION : au moins un gros dossier pourrait être un\n"
            "jeu/programme actif !",
        "{n} Ordner -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} dossiers -> CORBEILLE (récupérable).\nLibéré : {size}.\n\n"
            "{preview}{warn}\n\nContinuer ?",
        "{ok} Ordner in den Papierkorb verschoben, {size} frei. Protokoll: {log}":
            "{ok} dossiers déplacés vers la corbeille, {size} libres. Journal : {log}",
        "Temp gesamt: {size}. 'Temp leeren' gibt diesen Platz frei.":
            "Temp. total : {size}. 'Vider temp.' libère cet espace.",
        "\n(nur Dateien aelter als {days} Tage)":
            "\n(seulement les fichiers de plus de {days} jours)",
        "Temporaere Dateien werden ENDGUELTIG geloescht (NICHT in den "
        "Papierkorb).{age}\n\nGeschaetzt frei: bis zu {size}.\nGesperrte/benutzte "
        "Dateien werden uebersprungen.\n\nFortfahren?":
            "Les fichiers temporaires sont supprimés DÉFINITIVEMENT (PAS vers la "
            "corbeille).{age}\n\nLibération estimée : jusqu'à {size}.\nLes "
            "fichiers verrouillés/en cours d'utilisation sont ignorés.\n\n"
            "Continuer ?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt/zu jung).":
            "{n} fichiers supprimés, {size} libérés.\n{skip} ignorés "
            "(verrouillés/trop récents).",
        "{n} grosse Dateien  |  zusammen {size}. Amber = kuerzlich genutzt.":
            "{n} gros fichiers  |  au total {size}. Ambre = utilisé récemment.",
        "\n\nACHTUNG: Mindestens eine Datei wurde kuerzlich genutzt -\n"
        "evtl. ein aktives Spiel/Programm!":
            "\n\nATTENTION : au moins un fichier a été utilisé récemment -\n"
            "peut-être un jeu/programme actif !",
        "{n} Dateien -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} fichiers -> CORBEILLE (récupérable).\nLibéré : {size}.\n\n"
            "{preview}{warn}\n\nContinuer ?",
        "{ok} Dateien in den Papierkorb verschoben, {size} frei.":
            "{ok} fichiers déplacés vers la corbeille, {size} libres.",
        "Ordner nicht vorhanden:\n{path}": "Le dossier n'existe pas :\n{path}",
        "Groesse:  {size}   ({n} Dateien)\nOrdner:   {path}\nAdmin:    {admin}":
            "Taille : {size}   ({n} fichiers)\nDossier : {path}\nAdmin :  {admin}",
        "Update-Cache: {size}.": "Cache Update : {size}.",
        "Dienste wurden gestoppt und neu gestartet.":
            "Les services ont été arrêtés et redémarrés.",
        "Hinweis: Dienste konnten nicht gestoppt werden - gesperrte Dateien "
        "wurden uebersprungen.":
            "Remarque : les services n'ont pas pu être arrêtés - les fichiers "
            "verrouillés ont été ignorés.",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen.\n\n{svc}":
            "{n} fichiers supprimés, {size} libérés.\n{skip} ignorés.\n\n{svc}",
        "Windows.old gefunden:  {size}\nPfad:  {drive}\\Windows.old\n\nKlicke "
        "'Mit Datenträgerbereinigung entfernen' und hake dort\n'Vorherige "
        "Windows-Installation(en)' an.":
            "Windows.old trouvé :  {size}\nChemin :  {drive}\\Windows.old\n\n"
            "Cliquez sur 'Ouvrir le Nettoyage de disque' et cochez\n"
            "'Installation(s) Windows précédente(s)'.",
        "Windows.old: {size} - ueber die Datenträgerbereinigung entfernbar.":
            "Windows.old : {size} - supprimable via le Nettoyage de disque.",
        "{n} Programme mit Cache  |  zusammen {size}. Zeilen auswaehlen (Strg/Shift).":
            "{n} programmes avec cache  |  au total {size}. Sélectionnez des lignes (Ctrl/Maj).",
        "Caches von: {names}\n\nbis zu {size} werden ENDGUELTIG geleert (nicht in "
        "den Papierkorb).\n\nFortfahren?":
            "Caches de : {names}\n\njusqu'à {size} seront vidés DÉFINITIVEMENT "
            "(pas vers la corbeille).\n\nContinuer ?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt - App offen?).":
            "{n} fichiers supprimés, {size} libérés.\n{skip} ignorés "
            "(verrouillés - appli ouverte ?).",
        "Papierkorb: {size} in {n} Objekten": "Corbeille : {size} dans {n} éléments",
        "Papierkorb: {size}.": "Corbeille : {size}.",
        "Ruhezustand: AKTIV  (hiberfil.sys: {size})":
            "Veille prolongée : ACTIVE  (hiberfil.sys : {size})",
        "Ruhezustand: AUS (keine hiberfil.sys)":
            "Veille prolongée : DÉSACTIVÉE (pas de hiberfil.sys)",
        "hiberfil.sys ({size}) wird geloescht. Ruhezustand und Schnellstart sind "
        "danach aus (umkehrbar).\n\nFortfahren?":
            "hiberfil.sys ({size}) sera supprimé. La veille prolongée et le "
            "démarrage rapide seront alors désactivés (réversible).\n\nContinuer ?",
        "Ruhezustand abgeschaltet, Platz freigegeben.":
            "Veille prolongée désactivée, espace libéré.",
        "Ruhezustand wieder eingeschaltet.": "Veille prolongée réactivée.",
        "Fehler: {msg}": "Erreur : {msg}",
        "Der Pfad existiert nicht mehr:\n{path}": "Le chemin n'existe plus :\n{path}",
        "Konnte nicht oeffnen:\n{exc}": "Impossible d'ouvrir :\n{exc}",
        "Wirklich {n} Ordner ({size}) in den Papierkorb verschieben?":
            "Déplacer vraiment {n} dossiers ({size}) vers la corbeille ?",
        "Wirklich {n} Dateien ({size}) in den Papierkorb?":
            "Déplacer vraiment {n} fichiers ({size}) vers la corbeille ?",
        "DISM braucht Administrator-Rechte.\n\nJetzt als Administrator neu starten?":
            "DISM nécessite des droits administrateur.\n\nRedémarrer en "
            "administrateur maintenant ?",
        "Diese Aktion braucht Administrator-Rechte.\n\nJetzt als Administrator "
        "neu starten?":
            "Cette action nécessite des droits administrateur.\n\nRedémarrer en "
            "administrateur maintenant ?",
        "Das Programm laeuft bereits mit Admin-Rechten.":
            "Le programme s'exécute déjà avec des droits administrateur.",
        "Neustart als Administrator wurde abgebrochen oder ist fehlgeschlagen.":
            "Le redémarrage en administrateur a été annulé ou a échoué.",
        "Zum Leeren des Update-Caches sind Administrator-Rechte noetig.\nBitte "
        "'Als Administrator neu starten' verwenden.":
            "Des droits administrateur sont requis pour vider le cache Update.\n"
            "Utilisez 'Redémarrer en administrateur'.",
        "Es fehlten Administrator-Rechte. Bitte als Administrator neu starten.":
            "Des droits administrateur manquaient. Redémarrez en administrateur.",
        "Heruntergeladene Update-Pakete werden ENDGUELTIG geloescht.\nDie "
        "Update-Dienste werden kurz angehalten und danach wieder gestartet.\n\n"
        "Fortfahren?":
            "Les paquets de mise à jour téléchargés sont supprimés "
            "DÉFINITIVEMENT.\nLes services Update sont brièvement arrêtés puis "
            "redémarrés.\n\nContinuer ?",
        "Update-Cache wirklich endgueltig leeren?":
            "Vider définitivement le cache Update ?",
        "Temp-Dateien wirklich endgueltig loeschen?":
            "Supprimer définitivement les fichiers temporaires ?",
        "Ausgewaehlte Caches wirklich leeren?":
            "Vider vraiment les caches sélectionnés ?",
        "Der gesamte Papierkorb wird ENDGUELTIG geleert (alle Laufwerke). "
        "Danach ist eine Wiederherstellung nicht mehr moeglich.\n\nFortfahren?":
            "Toute la corbeille est vidée DÉFINITIVEMENT (tous les lecteurs). "
            "Ensuite, la récupération n'est plus possible.\n\nContinuer ?",
        "Es wird die Windows-Datenträgerbereinigung (cleanmgr) mit "
        "Administrator-Rechten gestartet.\n\nDort 'Vorherige Windows-"
        "Installation(en)' anhaken und auf OK klicken - Windows entfernt "
        "Windows.old dann sicher selbst.\n\nTipp: Hier lassen sich auch weitere "
        "Systemreste anhaken (Absturz-Dumps, Delivery-Optimization, "
        "Update-Bereinigung).\n\nFortfahren?":
            "Le Nettoyage de disque de Windows (cleanmgr) va démarrer avec des "
            "droits administrateur.\n\nCochez-y 'Installation(s) Windows "
            "précédente(s)' et cliquez sur OK - Windows supprimera alors "
            "Windows.old en toute sécurité.\n\nAstuce : vous pouvez aussi cocher "
            "ici d'autres résidus système (vidages mémoire, Delivery "
            "Optimization, nettoyage de Update).\n\nContinuer ?",
        "Konnte die Datenträgerbereinigung nicht starten (evtl. UAC "
        "abgebrochen). Alternativ ueber 'Speicher-Einstellungen'.":
            "Impossible de démarrer le Nettoyage de disque (UAC annulé ?). "
            "Sinon, utilisez 'Paramètres de stockage'.",
        "Datenträgerbereinigung gestartet - bitte dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "Nettoyage de disque démarré - cochez-y 'Installation(s) Windows "
            "précédente(s)'.",
        "Analysiere Komponentenspeicher ... bitte warten.\n\nSolange die blaue "
        "Anzeige sich bewegt, laeuft der Vorgang - das Fenster bitte NICHT "
        "schliessen.":
            "Analyse du magasin de composants ... veuillez patienter.\n\nTant que "
            "la barre bleue bouge, l'opération est en cours - ne fermez pas la "
            "fenêtre.",
        "Bereinige Komponentenspeicher ... das kann 10-20 Minuten dauern.\n\n"
        "Solange die blaue Anzeige sich bewegt, laeuft der Vorgang - das Fenster "
        "bitte NICHT schliessen und warten. Es ist NICHT eingefroren.":
            "Nettoyage du magasin de composants ... cela peut prendre 10-20 "
            "minutes.\n\nTant que la barre bleue bouge, l'opération est en cours "
            "- ne fermez pas la fenêtre et patientez. Elle n'est PAS figée.",
        "vor {n} Tagen": "il y a {n} jours",
        "vor {n} Monaten": "il y a {n} mois",
        "vor {n} Jahren": "il y a {n} ans",
        "\n\nACHTUNG ResetBase: installierte Updates lassen sich danach NICHT "
        "mehr deinstallieren.":
            "\n\nATTENTION ResetBase : les mises à jour installées ne pourront "
            "PLUS être désinstallées ensuite.",
        "DISM raeumt jetzt den WinSxS-Speicher auf.\n\nWICHTIG: Das kann 10-20 "
        "Minuten dauern und zeigt KEINEN Fortschritt in Prozent. Das Fenster "
        "bitte offen lassen und warten - es ist nicht eingefroren.{extra}\n\n"
        "Fortfahren?":
            "DISM va maintenant nettoyer le magasin WinSxS.\n\nIMPORTANT : cela "
            "peut prendre 10-20 minutes et n'affiche AUCUNE progression en "
            "pourcentage. Laissez la fenêtre ouverte et patientez - elle n'est "
            "pas figée.{extra}\n\nContinuer ?",
    },

    "uk": {
        "CleanSweep  -  Speicherplatz aufraeumen": "CleanSweep  -  Звільнення місця на диску",
        "Speicherplatz finden und sicher freigeben": "Знаходьте та безпечно звільняйте місце",
        "Bereit.": "Готово.",
        "Sprache": "Мова",
        "Beginner": "Початківець",
        "Expert": "Експерт",
        "Modus:": "Режим:",
        "♥ Unterstuetzen": "♥ Підтримати",
        "Entwicklung mit einer PayPal-Spende unterstuetzen":
            "Підтримайте розробку донатом через PayPal",
        "Spendenlink ist noch nicht eingetragen.\n\nBitte in gui.py die Variable "
        "DONATE_URL setzen.":
            "Посилання для донату ще не вказано.\n\nВкажіть змінну DONATE_URL у "
            "файлі gui.py.",
        "  Verwaiste Ordner  ": "  Залишкові папки  ",
        "  Temp-Dateien  ": "  Тимчасові файли  ",
        "  Grosse Dateien  ": "  Великі файли  ",
        "  Windows-Update  ": "  Windows Update  ",
        "  Windows.old  ": "  Windows.old  ",
        "  Caches  ": "  Кеші  ",
        "  System  ": "  Система  ",
        "Scan starten": "Почати сканування",
        "Auswahl in Papierkorb": "Вибране до кошика",
        "Mindest-Sicherheit:": "Мін. впевненість:",
        "ungenutzt seit (Monate):": "не використовується (місяців):",
        "Temp scannen": "Сканувати тимчасові",
        "Temp leeren (endgueltig)": "Очистити тимчасові (назавжди)",
        "nur aelter als (Tage):": "лише старші за (днів):",
        "Grosse Dateien suchen": "Знайти великі файли",
        "ab Groesse (MB):": "від розміру (МБ):",
        "Update-Cache scannen": "Сканувати кеш Update",
        "Update-Cache leeren": "Очистити кеш Update",
        "Als Administrator neu starten": "Перезапустити як адміністратор",
        "Analysieren": "Аналізувати",
        "Bereinigen": "Очистити",
        "ResetBase (gruendlicher)": "ResetBase (ретельніше)",
        "Windows.old pruefen": "Перевірити Windows.old",
        "Datenträgerbereinigung oeffnen (Windows.old u.a. Systemreste)":
            "Відкрити Очищення диска (Windows.old та інші залишки)",
        "Speicher-Einstellungen": "Параметри сховища",
        "Caches suchen": "Знайти кеші",
        "Auswahl leeren (endgueltig)": "Очистити вибране (назавжди)",
        "Papierkorb pruefen": "Перевірити кошик",
        "Papierkorb leeren": "Очистити кошик",
        "Status pruefen": "Перевірити стан",
        "Ruhezustand abschalten": "Вимкнути режим сну",
        "Ruhezustand einschalten": "Увімкнути режим сну",
        "Sicher": "Впевн.",
        "Groesse": "Розмір",
        "Zuletzt genutzt": "Останнє використання",
        "Kategorie": "Категорія",
        "Ordner": "Папка",
        "Warnung": "Попередження",
        "Dateien": "Файли",
        "Temp-Ordner": "Тимчасова папка",
        "Datei": "Файл",
        "Anzahl": "Кількість",
        "Programm": "Програма",
        "Beispielpfad": "Приклад шляху",
        "Springe in den Ordner": "Перейти до папки",
        "Komponentenspeicher (WinSxS) - DISM": "Сховище компонентів (WinSxS) - DISM",
        "Papierkorb": "Кошик",
        "Ruhezustand (hiberfil.sys)": "Режим сну (hiberfil.sys)",
        "Vorgang laeuft - bitte warten (die Anzeige bewegt sich):":
            "Операція триває - зачекайте (індикатор рухається):",
        "Keine Auswahl": "Нічого не вибрано",
        "Abgelehnt": "Відхилено",
        "Nicht gefunden": "Не знайдено",
        "Fehler": "Помилка",
        "Fertig": "Готово",
        "Sind Sie sicher?": "Ви впевнені?",
        "In den Papierkorb verschieben?": "Перемістити до кошика?",
        "Administrator noetig": "Потрібні права адміністратора",
        "Bereits Administrator": "Уже адміністратор",
        "Fehlgeschlagen": "Не вдалося",
        "Komponentenspeicher bereinigen?": "Очистити сховище компонентів?",
        "Update-Cache leeren?": "Очистити кеш Update?",
        "Temp-Dateien endgueltig loeschen?": "Назавжди видалити тимчасові файли?",
        "Caches endgueltig leeren?": "Назавжди очистити кеші?",
        "Papierkorb leeren?": "Очистити кошик?",
        "Datenträgerbereinigung starten?": "Запустити Очищення диска?",
        "Ruhezustand abschalten?": "Вимкнути режим сну?",
        "Bitte zuerst Zeilen auswaehlen.": "Спочатку виберіть рядки.",
        "Bitte zuerst Dateien auswaehlen.": "Спочатку виберіть файли.",
        "Nichts Sicheres ausgewaehlt.": "Не вибрано нічого безпечного.",
        "Abgebrochen.": "Скасовано.",
        "Nicht bestaetigt.": "Не підтверджено.",
        "Diese werden NICHT geloescht:\n\n": "Це НЕ буде видалено:\n\n",
        "Scanne alle Laufwerke (das kann eine Weile dauern) ...":
            "Сканування всіх дисків (це може зайняти час) ...",
        "Scanne Temp-Ordner ...": "Сканування тимчасових папок ...",
        "Loesche Temp-Dateien ...": "Видалення тимчасових файлів ...",
        "Durchsuche alle Laufwerke nach grossen Dateien (dauert) ...":
            "Пошук великих файлів на всіх дисках (триває) ...",
        "Suche Cache-Ordner ...": "Пошук папок кешу ...",
        "Leere Caches ...": "Очищення кешів ...",
        "Scanne Windows-Update-Cache ...": "Сканування кешу Windows Update ...",
        "Stoppe Dienste und leere Cache ...":
            "Зупинка служб і очищення кешу ...",
        "Pruefe Windows.old (Groesse berechnen kann dauern) ...":
            "Перевірка Windows.old (обчислення розміру може зайняти час) ...",
        "Kein Windows.old gefunden.": "Windows.old не знайдено.",
        "Kein 'Windows.old' vorhanden - nichts zu tun. :)":
            "Немає 'Windows.old' - нічого робити. :)",
        "Ruhezustand-Status geprueft.": "Стан режиму сну перевірено.",
        "DISM analysiert den Komponentenspeicher ...":
            "DISM аналізує сховище компонентів ...",
        "DISM bereinigt den Komponentenspeicher ...":
            "DISM очищає сховище компонентів ...",
        "DISM fertig.": "DISM завершено.",
        "DISM meldete einen Fehler.": "DISM повідомив про помилку.",
        "Papierkorb geleert.": "Кошик очищено.",
        "Papierkorb war leer oder konnte nicht geleert werden.":
            "Кошик був порожній або його не вдалося очистити.",
        "unbekannt": "невідомо",
        "heute": "сьогодні",
        "Geschuetzter System-/Wurzelordner": "Захищена системна/коренева папка",
        "Das ist eine Laufwerks-Wurzel": "Це корінь диска",
        "Liegt im Windows-Systemordner": "Розташовано в системній папці Windows",
        "Steht auf der Schutzliste (geschuetzter Name)":
            "У списку захисту (захищена назва)",
        "Pfad existiert nicht (mehr)": "Шлях більше не існує",
        "Kein Ordner": "Не папка",
        "Datei existiert nicht (mehr)": "Файл більше не існує",
        "System-/Auslagerungsdatei": "Системний файл / файл підкачки",
        "SEHR GROSS - erst pruefen, ob aktives Spiel/Programm!":
            "ДУЖЕ ВЕЛИКИЙ - спершу перевірте, чи це активна гра/програма!",
        "GROSS - evtl. aktives Programm (Steam/Epic?), bitte pruefen":
            "ВЕЛИКИЙ - можливо, активна програма (Steam/Epic?), перевірте",
        "ja": "так",
        "nein (zum Leeren noetig)": "ні (потрібно для очищення)",
        "Erfolgreich.": "Успішно.",
        "Fehler.": "Помилка.",
        "Temp-Dateien werden ENDGUELTIG geloescht (nicht in den Papierkorb), "
        "damit der Platz wirklich frei wird. Gesperrte Dateien bleiben "
        "unangetastet.":
            "Тимчасові файли видаляються НАЗАВЖДИ (не до кошика), щоб справді "
            "звільнити місце. Заблоковані файли не чіпаються.",
        "Findet die groessten Einzeldateien (z.B. alte Videos, ISO-Dateien). "
        "Amber = kuerzlich genutzt (evtl. aktives Spiel/Programm). Loeschen geht "
        "in den Papierkorb.":
            "Знаходить найбільші окремі файли (напр., старі відео, файли ISO). "
            "Бурштиновий = нещодавно використовувався (можливо, активна "
            "гра/програма). Видалення йде до кошика.",
        "Heruntergeladene Windows-Update-Pakete (SoftwareDistribution\\Download) "
        "sind nach der Installation nutzlos. Sie werden ENDGUELTIG geloescht "
        "und von Windows bei Bedarf neu angelegt.":
            "Завантажені пакети Windows Update (SoftwareDistribution\\Download) "
            "непотрібні після встановлення. Вони видаляються НАЗАВЖДИ, і Windows "
            "створює їх знову за потреби.",
        "Raeumt alte, durch Updates ersetzte Windows-Komponenten gruendlicher "
        "auf als die Datentraegerbereinigung. '/ResetBase' entfernt auch "
        "ersetzte Versionen endgueltig - danach lassen sich installierte Updates "
        "aber NICHT mehr deinstallieren. Braucht Admin und kann einige Minuten "
        "dauern.":
            "Очищає старі компоненти Windows, замінені оновленнями, ретельніше, "
            "ніж Очищення диска. '/ResetBase' також назавжди видаляє замінені "
            "версії - після цього встановлені оновлення вже НЕ можна видалити. "
            "Потрібні права адміністратора, може тривати кілька хвилин.",
        "WICHTIG: WinSxS bleibt IMMER mehrere GB gross (vieles ist mit Windows "
        "geteilt) - das ist normal. Und 'empfohlen: Ja' steht schon ab 1 "
        "ersetzten Paket - auf einem aktuellen Windows fast immer. Massgeblich "
        "ist die Anzahl 'bereinigbarer Pakete' (0-2 = gesund), NICHT die "
        "'empfohlen'-Zeile.":
            "ВАЖЛИВО: WinSxS ЗАВЖДИ займає кілька ГБ (багато що спільне з "
            "Windows) - це нормально. А 'рекомендовано: Так' зʼявляється вже з 1 "
            "заміненим пакетом - майже завжди на актуальній Windows. Важлива "
            "кількість 'пакетів для відновлення' (0-2 = здорово), а НЕ рядок "
            "'рекомендовано'.",
        "'Windows.old' enthaelt die vorherige Windows-Version nach einem Upgrade "
        "(oft 20-70 GB). Es laesst sich NICHT normal loeschen, weil es dem "
        "System gehoert (TrustedInstaller-Sperre). Der sichere Weg ist die "
        "Windows-Datenträgerbereinigung: dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "'Windows.old' містить попередню версію Windows після оновлення "
            "(часто 20-70 ГБ). Його НЕ можна видалити звичайним способом, бо він "
            "належить системі (блокування TrustedInstaller). Безпечний шлях - "
            "Очищення диска Windows: позначте там 'Попередні встановлення "
            "Windows'.",
        "Cache-Ordner von Browsern und Apps. Werden automatisch neu aufgebaut "
        "und daher ENDGUELTIG geleert. Fuer das beste Ergebnis die jeweilige App "
        "vorher schliessen (gesperrte Dateien werden sonst uebersprungen).":
            "Папки кешу браузерів і застосунків. Вони відновлюються автоматично, "
            "тому очищаються НАЗАВЖДИ. Для найкращого результату спершу закрийте "
            "відповідний застосунок (інакше заблоковані файли пропускаються).",
        "CleanSweep verschiebt Ordner/Dateien in den Papierkorb. Der Platz wird "
        "erst frei, wenn er geleert wird.":
            "CleanSweep переміщує папки/файли до кошика. Місце звільняється лише "
            "після його очищення.",
        "Der Ruhezustand belegt eine Datei so gross wie dein RAM (oft 8-32 GB). "
        "Abschalten gibt diesen Platz frei - danach gibt es keinen Ruhezustand/"
        "Schnellstart mehr (jederzeit umkehrbar). Braucht Admin-Rechte.":
            "Режим сну займає файл розміром з вашу оперативну памʼять (часто 8-32 "
            "ГБ). Вимкнення звільняє це місце - після цього немає режиму сну/"
            "швидкого запуску (можна повернути будь-коли). Потрібні права "
            "адміністратора.",
        "Fehler: {err}": "Помилка: {err}",
        "Hinweis: Zum Leeren werden Administrator-Rechte benoetigt. ":
            "Примітка: для очищення потрібні права адміністратора. ",
        "... und {n} weitere": "... та ще {n}",
        "{n} Kandidaten  |  potentiell {size} frei. Zeilen auswaehlen (Strg/Shift).":
            "{n} кандидатів  |  потенційно {size} вільно. Виберіть рядки (Ctrl/Shift).",
        "\n\nACHTUNG: Mindestens ein grosser Ordner koennte ein aktives\n"
        "Spiel/Programm sein!":
            "\n\nУВАГА: щонайменше одна велика папка може бути активною\n"
            "грою/програмою!",
        "{n} Ordner -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} папок -> КОШИК (з можливістю відновлення).\nЗвільниться: {size}."
            "\n\n{preview}{warn}\n\nПродовжити?",
        "{ok} Ordner in den Papierkorb verschoben, {size} frei. Protokoll: {log}":
            "{ok} папок переміщено до кошика, {size} вільно. Журнал: {log}",
        "Temp gesamt: {size}. 'Temp leeren' gibt diesen Platz frei.":
            "Тимчасові разом: {size}. 'Очистити тимчасові' звільняє це місце.",
        "\n(nur Dateien aelter als {days} Tage)":
            "\n(лише файли, старші за {days} днів)",
        "Temporaere Dateien werden ENDGUELTIG geloescht (NICHT in den "
        "Papierkorb).{age}\n\nGeschaetzt frei: bis zu {size}.\nGesperrte/benutzte "
        "Dateien werden uebersprungen.\n\nFortfahren?":
            "Тимчасові файли будуть видалені НАЗАВЖДИ (НЕ до кошика).{age}\n\n"
            "Орієнтовно звільниться: до {size}.\nЗаблоковані/використовувані файли "
            "пропускаються.\n\nПродовжити?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt/zu jung).":
            "Видалено {n} файлів, звільнено {size}.\n{skip} пропущено "
            "(заблоковані/занадто нові).",
        "{n} grosse Dateien  |  zusammen {size}. Amber = kuerzlich genutzt.":
            "{n} великих файлів  |  разом {size}. Бурштиновий = нещодавно "
            "використовувалися.",
        "\n\nACHTUNG: Mindestens eine Datei wurde kuerzlich genutzt -\n"
        "evtl. ein aktives Spiel/Programm!":
            "\n\nУВАГА: щонайменше один файл нещодавно використовувався -\n"
            "можливо, активна гра/програма!",
        "{n} Dateien -> PAPIERKORB (wiederherstellbar).\nFrei werden: {size}.\n\n"
        "{preview}{warn}\n\nFortfahren?":
            "{n} файлів -> КОШИК (з можливістю відновлення).\nЗвільниться: {size}."
            "\n\n{preview}{warn}\n\nПродовжити?",
        "{ok} Dateien in den Papierkorb verschoben, {size} frei.":
            "{ok} файлів переміщено до кошика, {size} вільно.",
        "Ordner nicht vorhanden:\n{path}": "Папка не існує:\n{path}",
        "Groesse:  {size}   ({n} Dateien)\nOrdner:   {path}\nAdmin:    {admin}":
            "Розмір: {size}   ({n} файлів)\nПапка:  {path}\nАдмін:  {admin}",
        "Update-Cache: {size}.": "Кеш Update: {size}.",
        "Dienste wurden gestoppt und neu gestartet.":
            "Служби зупинено та перезапущено.",
        "Hinweis: Dienste konnten nicht gestoppt werden - gesperrte Dateien "
        "wurden uebersprungen.":
            "Примітка: не вдалося зупинити служби - заблоковані файли пропущено.",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen.\n\n{svc}":
            "Видалено {n} файлів, звільнено {size}.\n{skip} пропущено.\n\n{svc}",
        "Windows.old gefunden:  {size}\nPfad:  {drive}\\Windows.old\n\nKlicke "
        "'Mit Datenträgerbereinigung entfernen' und hake dort\n'Vorherige "
        "Windows-Installation(en)' an.":
            "Знайдено Windows.old:  {size}\nШлях:  {drive}\\Windows.old\n\n"
            "Натисніть 'Відкрити Очищення диска' та позначте\n'Попередні "
            "встановлення Windows'.",
        "Windows.old: {size} - ueber die Datenträgerbereinigung entfernbar.":
            "Windows.old: {size} - можна видалити через Очищення диска.",
        "{n} Programme mit Cache  |  zusammen {size}. Zeilen auswaehlen (Strg/Shift).":
            "{n} програм із кешем  |  разом {size}. Виберіть рядки (Ctrl/Shift).",
        "Caches von: {names}\n\nbis zu {size} werden ENDGUELTIG geleert (nicht in "
        "den Papierkorb).\n\nFortfahren?":
            "Кеші: {names}\n\nдо {size} буде очищено НАЗАВЖДИ (не до кошика).\n\n"
            "Продовжити?",
        "{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
        "(gesperrt - App offen?).":
            "Видалено {n} файлів, звільнено {size}.\n{skip} пропущено "
            "(заблоковані - застосунок відкритий?).",
        "Papierkorb: {size} in {n} Objekten": "Кошик: {size} у {n} обʼєктах",
        "Papierkorb: {size}.": "Кошик: {size}.",
        "Ruhezustand: AKTIV  (hiberfil.sys: {size})":
            "Режим сну: УВІМКНЕНО  (hiberfil.sys: {size})",
        "Ruhezustand: AUS (keine hiberfil.sys)":
            "Режим сну: ВИМКНЕНО (немає hiberfil.sys)",
        "hiberfil.sys ({size}) wird geloescht. Ruhezustand und Schnellstart sind "
        "danach aus (umkehrbar).\n\nFortfahren?":
            "hiberfil.sys ({size}) буде видалено. Режим сну та швидкий запуск "
            "після цього вимкнено (можна повернути).\n\nПродовжити?",
        "Ruhezustand abgeschaltet, Platz freigegeben.":
            "Режим сну вимкнено, місце звільнено.",
        "Ruhezustand wieder eingeschaltet.": "Режим сну знову увімкнено.",
        "Fehler: {msg}": "Помилка: {msg}",
        "Der Pfad existiert nicht mehr:\n{path}": "Шлях більше не існує:\n{path}",
        "Konnte nicht oeffnen:\n{exc}": "Не вдалося відкрити:\n{exc}",
        "Wirklich {n} Ordner ({size}) in den Papierkorb verschieben?":
            "Справді перемістити {n} папок ({size}) до кошика?",
        "Wirklich {n} Dateien ({size}) in den Papierkorb?":
            "Справді перемістити {n} файлів ({size}) до кошика?",
        "DISM braucht Administrator-Rechte.\n\nJetzt als Administrator neu starten?":
            "DISM потребує прав адміністратора.\n\nПерезапустити як адміністратор "
            "зараз?",
        "Diese Aktion braucht Administrator-Rechte.\n\nJetzt als Administrator "
        "neu starten?":
            "Ця дія потребує прав адміністратора.\n\nПерезапустити як "
            "адміністратор зараз?",
        "Das Programm laeuft bereits mit Admin-Rechten.":
            "Програма вже працює з правами адміністратора.",
        "Neustart als Administrator wurde abgebrochen oder ist fehlgeschlagen.":
            "Перезапуск як адміністратор скасовано або не вдався.",
        "Zum Leeren des Update-Caches sind Administrator-Rechte noetig.\nBitte "
        "'Als Administrator neu starten' verwenden.":
            "Для очищення кешу Update потрібні права адміністратора.\n"
            "Використайте 'Перезапустити як адміністратор'.",
        "Es fehlten Administrator-Rechte. Bitte als Administrator neu starten.":
            "Бракувало прав адміністратора. Перезапустіть як адміністратор.",
        "Heruntergeladene Update-Pakete werden ENDGUELTIG geloescht.\nDie "
        "Update-Dienste werden kurz angehalten und danach wieder gestartet.\n\n"
        "Fortfahren?":
            "Завантажені пакети оновлень будуть видалені НАЗАВЖДИ.\nСлужби Update "
            "буде ненадовго зупинено й потім перезапущено.\n\nПродовжити?",
        "Update-Cache wirklich endgueltig leeren?":
            "Справді очистити кеш Update назавжди?",
        "Temp-Dateien wirklich endgueltig loeschen?":
            "Справді видалити тимчасові файли назавжди?",
        "Ausgewaehlte Caches wirklich leeren?":
            "Справді очистити вибрані кеші?",
        "Der gesamte Papierkorb wird ENDGUELTIG geleert (alle Laufwerke). "
        "Danach ist eine Wiederherstellung nicht mehr moeglich.\n\nFortfahren?":
            "Увесь кошик буде очищено НАЗАВЖДИ (усі диски). Після цього "
            "відновлення буде неможливим.\n\nПродовжити?",
        "Es wird die Windows-Datenträgerbereinigung (cleanmgr) mit "
        "Administrator-Rechten gestartet.\n\nDort 'Vorherige Windows-"
        "Installation(en)' anhaken und auf OK klicken - Windows entfernt "
        "Windows.old dann sicher selbst.\n\nTipp: Hier lassen sich auch weitere "
        "Systemreste anhaken (Absturz-Dumps, Delivery-Optimization, "
        "Update-Bereinigung).\n\nFortfahren?":
            "Запуститься Очищення диска Windows (cleanmgr) з правами "
            "адміністратора.\n\nПозначте там 'Попередні встановлення Windows' та "
            "натисніть OK - Windows безпечно видалить Windows.old.\n\nПорада: тут "
            "також можна позначити інші системні залишки (аварійні дампи, Delivery "
            "Optimization, очищення Update).\n\nПродовжити?",
        "Konnte die Datenträgerbereinigung nicht starten (evtl. UAC "
        "abgebrochen). Alternativ ueber 'Speicher-Einstellungen'.":
            "Не вдалося запустити Очищення диска (UAC скасовано?). Як "
            "альтернатива - 'Параметри сховища'.",
        "Datenträgerbereinigung gestartet - bitte dort 'Vorherige Windows-"
        "Installation(en)' anhaken.":
            "Очищення диска запущено - позначте там 'Попередні встановлення "
            "Windows'.",
        "Analysiere Komponentenspeicher ... bitte warten.\n\nSolange die blaue "
        "Anzeige sich bewegt, laeuft der Vorgang - das Fenster bitte NICHT "
        "schliessen.":
            "Аналіз сховища компонентів ... зачекайте.\n\nПоки блакитний "
            "індикатор рухається, операція триває - не закривайте вікно.",
        "Bereinige Komponentenspeicher ... das kann 10-20 Minuten dauern.\n\n"
        "Solange die blaue Anzeige sich bewegt, laeuft der Vorgang - das Fenster "
        "bitte NICHT schliessen und warten. Es ist NICHT eingefroren.":
            "Очищення сховища компонентів ... це може тривати 10-20 хвилин.\n\n"
            "Поки блакитний індикатор рухається, операція триває - не закривайте "
            "вікно й зачекайте. Воно НЕ зависло.",
        "vor {n} Tagen": "{n} дн. тому",
        "vor {n} Monaten": "{n} міс. тому",
        "vor {n} Jahren": "{n} р. тому",
        "\n\nACHTUNG ResetBase: installierte Updates lassen sich danach NICHT "
        "mehr deinstallieren.":
            "\n\nУВАГА ResetBase: встановлені оновлення після цього вже НЕ можна "
            "буде видалити.",
        "DISM raeumt jetzt den WinSxS-Speicher auf.\n\nWICHTIG: Das kann 10-20 "
        "Minuten dauern und zeigt KEINEN Fortschritt in Prozent. Das Fenster "
        "bitte offen lassen und warten - es ist nicht eingefroren.{extra}\n\n"
        "Fortfahren?":
            "DISM зараз очистить сховище WinSxS.\n\nВАЖЛИВО: це може тривати 10-20 "
            "хвилин і НЕ показує прогрес у відсотках. Залиште вікно відкритим і "
            "зачекайте - воно не зависло.{extra}\n\nПродовжити?",
    },
}
