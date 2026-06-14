"""
main.py  -  CleanSweep (Analyse-Modus)
======================================
Startpunkt des Tools. Aktuell rein analysierend (READ-ONLY):
es scannt ALLE festen Laufwerke, gleicht ab und ZEIGT moegliche verwaiste
Ordner an. Es wird in dieser Version NICHTS geloescht oder veraendert.

Aufruf:
    python main.py                          # Bericht in der Konsole
    python main.py --min-confidence 60      # nur sicherere Kandidaten
    python main.py --csv bericht.csv        # zusaetzlich als CSV speichern
"""

from __future__ import annotations

import argparse
import csv
import sys

from registry_scan import get_installed_programs
from folder_scan import (
    scan_program_folders, human_size, human_age, get_fixed_drives,
    get_scan_locations,
)
from orphan_finder import find_orphans, OrphanCandidate
from cleaner import is_safe_to_delete, delete_candidates, DEFAULT_LOG


def print_header(title: str) -> None:
    print()
    print("=" * 78)
    print(f"  {title}")
    print("=" * 78)


def run_report(min_confidence: int, csv_path: str | None) -> None:
    print_header("CleanSweep  -  Analyse (es wird NICHTS geloescht)")

    drives = get_fixed_drives()
    locations = get_scan_locations()
    print(f"\nFeste Laufwerke: {', '.join(str(d) for d in drives)}")
    print(f"Scan-Orte: {len(locations)}")

    # --- Schritt 1: installierte Programme -------------------------------
    programs = get_installed_programs()
    print(f"\n[1/3] Installierte Programme laut Registry: {len(programs)}")

    # --- Schritt 2: Ordner scannen ---------------------------------------
    print("[2/3] Scanne Ordner und berechne Groessen (das kann dauern) ...")
    folders = scan_program_folders(compute_sizes=True, progress=True)
    total_size = sum(f.size_bytes for f in folders)
    print(f"      Gefundene Ordner: {len(folders)} "
          f"(gesamt {human_size(total_size)})")

    # --- Schritt 3: verwaiste Ordner -------------------------------------
    print("[3/3] Suche verwaiste Ordner (ohne zugehoeriges Programm) ...")
    orphans = find_orphans(min_confidence=min_confidence)
    orphan_size = sum(o.folder.size_bytes for o in orphans)

    print_header(
        f"Moegliche Reste: {len(orphans)} Ordner  "
        f"(potentiell {human_size(orphan_size)} frei)"
    )

    if not orphans:
        print("\n  Keine verwaisten Ordner gefunden. Sauberes System! :)\n")
        return

    print(f"\n  {'Sicher':>6}  {'Groesse':>10}  {'Zuletzt':>14}  {'Kategorie':16}  Ordner")
    print(f"  {'-'*6}  {'-'*10}  {'-'*14}  {'-'*16}  {'-'*30}")
    for o in orphans:
        print(f"  {o.confidence:>5}%  {human_size(o.folder.size_bytes):>10}  "
              f"{human_age(o.folder.last_modified):>14}  "
              f"{o.folder.category:16}  {o.folder.path}")
        if o.warning:
            print(f"  {'':6}  {'':10}  {'':14}  {'':16}  /!\\ {o.warning}")

    print("\n  Hinweis: 'Sicher' schaetzt, OB es ein Rest ist - nicht, ob")
    print("  Loeschen gefahrlos ist. Eintraege mit /!\\ (grosse Ordner) koennen")
    print("  aktive Spiele/Programme sein - vor dem Loeschen unbedingt pruefen.")
    print("  Es wird NICHTS geloescht.")
    print()

    # --- Optional: CSV-Export --------------------------------------------
    if csv_path:
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.writer(fh, delimiter=";")
            writer.writerow(["Sicherheit_%", "Kategorie", "Groesse_Bytes",
                             "Groesse_lesbar", "Zuletzt_genutzt", "Pfad",
                             "Begruendung"])
            for o in orphans:
                writer.writerow([
                    o.confidence,
                    o.folder.category,
                    o.folder.size_bytes,
                    human_size(o.folder.size_bytes),
                    human_age(o.folder.last_modified),
                    str(o.folder.path),
                    o.reason,
                ])
        print(f"  CSV-Bericht gespeichert: {csv_path}\n")


def parse_selection(text: str, count: int) -> list[int]:
    """Wandelt eine Nutzereingabe in eine Liste von Indizes (0-basiert).

    Erlaubt: 'alle', einzelne Nummern, Listen ('1 3 5' / '1,3,5') und
    Bereiche ('1-4'). Ungueltiges wird ignoriert. Leere Eingabe -> nichts.
    """
    text = text.strip().lower()
    if not text:
        return []
    if text in ("alle", "all", "*"):
        return list(range(count))

    chosen: set[int] = set()
    for part in text.replace(",", " ").split():
        if "-" in part:
            a, _, b = part.partition("-")
            if a.isdigit() and b.isdigit():
                for n in range(int(a), int(b) + 1):
                    if 1 <= n <= count:
                        chosen.add(n - 1)
        elif part.isdigit():
            n = int(part)
            if 1 <= n <= count:
                chosen.add(n - 1)
    return sorted(chosen)


def _ask(prompt: str) -> str:
    """input() mit sicherem Abbruch, falls keine Eingabe moeglich ist."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return ""


def run_delete(min_confidence: int) -> None:
    """Interaktiver Lösch-Ablauf: Auswahl -> Vorschau -> Bestätigung -> Papierkorb."""
    print_header("CleanSweep  -  LOESCH-Modus (Papierkorb, umkehrbar)")
    print("\nZuerst scanne ich wie gewohnt ...")

    orphans = find_orphans(min_confidence=min_confidence)
    if not orphans:
        print("\n  Keine verwaisten Ordner gefunden. Nichts zu tun.\n")
        return

    # --- Liste mit Nummern anzeigen --------------------------------------
    print(f"\n  Gefundene Kandidaten ({len(orphans)}):\n")
    print(f"  {'Nr':>3}  {'Sicher':>6}  {'Groesse':>10}  {'Kategorie':16}  Ordner")
    print(f"  {'-'*3}  {'-'*6}  {'-'*10}  {'-'*16}  {'-'*30}")
    for i, o in enumerate(orphans, start=1):
        print(f"  {i:>3}  {o.confidence:>5}%  {human_size(o.folder.size_bytes):>10}  "
              f"{o.folder.category:16}  {o.folder.path}")
        if o.warning:
            print(f"  {'':3}  {'':6}  {'':10}  {'':16}  /!\\ {o.warning}")

    # --- Auswahl ---------------------------------------------------------
    print("\n  Welche Ordner in den Papierkorb verschieben?")
    print("  Beispiele: '1 3 5'  oder  '1-4'  oder  'alle'  (leer = abbrechen)")
    selection = parse_selection(_ask("  Auswahl: "), len(orphans))
    if not selection:
        print("\n  Abgebrochen. Es wurde NICHTS geloescht.\n")
        return

    # --- Sicherheitspruefung der Auswahl ---------------------------------
    approved: list[OrphanCandidate] = []
    rejected: list[tuple[OrphanCandidate, str]] = []
    for idx in selection:
        cand = orphans[idx]
        safe, reason = is_safe_to_delete(cand.folder)
        (approved.append(cand) if safe else rejected.append((cand, reason)))

    if rejected:
        print("\n  Folgende Auswahl wurde aus Sicherheitsgruenden ABGELEHNT:")
        for cand, reason in rejected:
            print(f"    - {cand.folder.path}  ({reason})")

    if not approved:
        print("\n  Nichts Sicheres uebrig. Es wird NICHTS geloescht.\n")
        return

    # --- Vorschau --------------------------------------------------------
    total = sum(c.folder.size_bytes for c in approved)
    print_header(f"VORSCHAU: {len(approved)} Ordner -> Papierkorb "
                 f"({human_size(total)} werden frei)")
    has_warning = False
    for c in approved:
        mark = "  /!\\" if c.warning else "     "
        print(f"  {mark} {human_size(c.folder.size_bytes):>10}  {c.folder.path}")
        if c.warning:
            has_warning = True
    if has_warning:
        print("\n  ACHTUNG: Mit /!\\ markierte Ordner koennten AKTIVE Spiele/")
        print("  Programme sein. Bitte ganz sicher sein, bevor du fortfaehrst!")

    # --- Bestätigung -----------------------------------------------------
    print("\n  Alles wird in den PAPIERKORB verschoben (wiederherstellbar).")
    confirm = _ask("  Zum Bestaetigen 'LOESCHEN' eingeben: ")
    if confirm.strip().upper() != "LOESCHEN":
        print("\n  Nicht bestaetigt. Es wurde NICHTS geloescht.\n")
        return

    # --- Ausführen -------------------------------------------------------
    print("\n  Verschiebe in den Papierkorb ...")
    results = delete_candidates(approved)
    freed = sum(r.size_bytes for r in results if r.success)
    ok = sum(1 for r in results if r.success)
    fail = len(results) - ok

    print_header(f"Fertig: {ok} verschoben, {fail} fehlgeschlagen "
                 f"({human_size(freed)} freigegeben)")
    for r in results:
        status = "OK  " if r.success else "FEHL"
        print(f"  [{status}] {r.path}  -  {r.message}")
    print(f"\n  Protokoll: {DEFAULT_LOG}")
    print("  Wiederherstellung: alles liegt im Windows-Papierkorb.\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="CleanSweep - findet verwaiste Programm-Ordner (read-only)."
    )
    parser.add_argument(
        "--min-confidence", type=int, default=0, metavar="0-100",
        help="Nur Kandidaten ab dieser Sicherheit anzeigen (Standard: 0).",
    )
    parser.add_argument(
        "--csv", metavar="DATEI",
        help="Zusaetzlich als CSV-Datei speichern.",
    )
    parser.add_argument(
        "--delete", action="store_true",
        help="LOESCH-Modus: Kandidaten interaktiv in den Papierkorb verschieben "
             "(mit Vorschau + Bestaetigung, umkehrbar).",
    )
    args = parser.parse_args(argv)

    if args.delete:
        run_delete(min_confidence=args.min_confidence)
    else:
        run_report(min_confidence=args.min_confidence, csv_path=args.csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
