"""
gui.py  -  CleanSweep grafische Oberflaeche
===========================================
Dark-Mode-Oberflaeche mit marineblauer Schrift fuer CleanSweep.

Mehrsprachig (Deutsch/Englisch) - umschaltbar ueber die Flaggen oben rechts.
Alle sichtbaren Texte laufen ueber i18n.t(); Deutsch ist die Quellsprache.

Sieben Tabs: Verwaiste Ordner, Temp-Dateien, Grosse Dateien, Windows-Update,
Windows.old, Caches, System.

Start:  python gui.py   (oder Doppelklick auf "CleanSweep starten.bat")
"""

from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import ttk, messagebox

# ===========================================================================
# HIER DEINEN PAYPAL-SPENDENLINK EINTRAGEN (als Text, z.B. von PayPal.Me):
#   DONATE_URL = "https://www.paypal.com/paypalme/DeinName"
# Leer lassen ("") deaktiviert den Spenden-Knopf.
# ===========================================================================
DONATE_URL = "https://www.paypal.com/qrcodes/p2pqrc/KUB2AYSPY8F9G"

import i18n
from i18n import t
from folder_scan import human_size, human_age, age_days, get_fixed_drives
from orphan_finder import find_orphans, OrphanCandidate
from cleaner import is_safe_to_delete, delete_candidates, trash_path, DEFAULT_LOG
from temp_cleaner import scan_temp, clean_temp
from big_files import find_large_files, is_safe_to_delete_file
from update_cleaner import (
    scan_update_cache, clean_update_cache, is_admin, relaunch_as_admin,
)
from windows_old import scan_windows_old, launch_disk_cleanup, open_storage_settings
from cache_cleaner import scan_caches, clean_caches
from recycle_bin import query_recycle_bin, empty_recycle_bin
from hibernation import (
    hibernation_enabled, hiberfile_size, disable_hibernation, enable_hibernation,
)
from dism_cleanup import (
    analyze_component_store, start_component_cleanup, summarize_analysis,
)


# --- Farbpalette: Dark Mode mit marineblauer Schrift ----------------------
BG_DARK = "#13161c"
BG_PANEL = "#1c212b"
BG_INPUT = "#232a36"
MARINE = "#2e5e8c"
MARINE_BRIGHT = "#4f8fc0"
MARINE_TEXT = "#6fa8dc"
AMBER = "#e0a458"
TEXT_DIM = "#8a9bb0"


class CleanSweepGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.orphans: list[OrphanCandidate] = []
        self.temp_locs = []
        self.big = []
        self.caches = []
        self.mode = "beginner"   # "beginner" | "expert"

        root.geometry("1240x760")
        root.configure(bg=BG_DARK)
        root.minsize(1080, 640)
        self._set_window_icon()

        self._setup_style()
        # Alles in einen Container, damit ein Sprachwechsel sauber neu aufbauen kann.
        self.container = tk.Frame(root, bg=BG_DARK)
        self.container.pack(fill="both", expand=True)
        self._build_ui()

    def set_language(self, lang: str) -> None:
        """Schaltet die Sprache um und baut die Oberflaeche neu auf."""
        if lang == i18n.get_language():
            return
        i18n.set_language(lang)
        i18n.save_language(lang)   # fuer den naechsten Start merken
        self._rebuild()

    def set_mode(self, mode: str) -> None:
        """Schaltet zwischen Beginner/Expert um (gibt 2 Reiter frei) + Neuaufbau."""
        if mode == self.mode:
            return
        self.mode = mode
        self._rebuild()

    def _rebuild(self) -> None:
        for w in self.container.winfo_children():
            w.destroy()
        self._build_ui()

    def _open_donate(self) -> None:
        """Oeffnet den PayPal-Spendenlink im Browser."""
        if not DONATE_URL:
            messagebox.showinfo(
                t("♥ Unterstuetzen"),
                t("Spendenlink ist noch nicht eingetragen.\n\nBitte in gui.py "
                  "die Variable DONATE_URL setzen."))
            return
        webbrowser.open(DONATE_URL)

    def _set_window_icon(self) -> None:
        """Setzt das Fenster-/Taskleisten-Icon (cleansweep.ico), falls vorhanden."""
        if getattr(sys, "frozen", False):
            # In der gepackten exe liegt die .ico im Bundle-Verzeichnis.
            base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
            ico = os.path.join(base, "cleansweep.ico")
        else:
            # Entwicklung: <projekt>\installer\cleansweep.ico
            proj = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ico = os.path.join(proj, "installer", "cleansweep.ico")
        try:
            if os.path.exists(ico):
                self.root.iconbitmap(ico)
        except tk.TclError:
            pass  # Icon optional - kein Abbruch, falls es nicht ladbar ist

    def _build_ui(self) -> None:
        self.root.title(t("CleanSweep  -  Speicherplatz aufraeumen"))
        self._build_header()
        self._build_statusbar()   # zuerst unten verankern
        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(8, 4))
        # "Verwaiste Ordner" und "Grosse Dateien" sind nur im Expert-Modus sichtbar.
        if self.mode == "expert":
            self._build_orphan_tab()
            self._build_bigfiles_tab()
        self._build_temp_tab()
        self._build_update_tab()
        self._build_winold_tab()
        self._build_caches_tab()
        self._build_system_tab()

    # ---------------------------------------------------------------- Style
    def _setup_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview", background=BG_INPUT, fieldbackground=BG_INPUT,
                        foreground=MARINE_TEXT, rowheight=26, borderwidth=0)
        style.configure("Treeview.Heading", background=BG_PANEL,
                        foreground=MARINE_BRIGHT, borderwidth=0, relief="flat",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", MARINE)],
                  foreground=[("selected", "#ffffff")])
        style.map("Treeview.Heading", background=[("active", BG_INPUT)])

        style.configure("Marine.TButton", background=MARINE, foreground="#ffffff",
                        borderwidth=0, focuscolor=MARINE,
                        font=("Segoe UI", 10, "bold"), padding=(14, 8))
        style.map("Marine.TButton",
                  background=[("active", MARINE_BRIGHT), ("disabled", BG_PANEL)],
                  foreground=[("disabled", TEXT_DIM)])

        style.configure("TSpinbox", fieldbackground=BG_INPUT, foreground=MARINE_TEXT,
                        background=BG_PANEL, arrowcolor=MARINE_BRIGHT, borderwidth=0)

        style.configure("Marine.Horizontal.TProgressbar",
                        troughcolor=BG_INPUT, background=MARINE_BRIGHT,
                        borderwidth=0, lightcolor=MARINE_BRIGHT,
                        darkcolor=MARINE, thickness=22)

        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_PANEL, foreground=TEXT_DIM,
                        padding=(18, 8), font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", BG_INPUT)],
                  foreground=[("selected", MARINE_BRIGHT)])

    # --------------------------------------------------------------- Header
    def _build_header(self) -> None:
        header = tk.Frame(self.container, bg=BG_PANEL)
        header.pack(fill="x")
        tk.Label(header, text="CleanSweep", bg=BG_PANEL, fg=MARINE_BRIGHT,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=16, pady=12)
        tk.Label(header, text=t("Speicherplatz finden und sicher freigeben"),
                 bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Segoe UI", 10)).pack(side="left", pady=12)

        # --- Flaggen oben rechts (Sprachauswahl) ---
        flags = tk.Frame(header, bg=BG_PANEL)
        flags.pack(side="right", padx=12)
        # Reihenfolge von links nach rechts: DE EN FR ES PL.
        self._flag(flags, "de", self._draw_de_flag)
        self._flag(flags, "en", self._draw_uk_flag)
        self._flag(flags, "fr", self._draw_fr_flag)
        self._flag(flags, "es", self._draw_es_flag)
        self._flag(flags, "pl", self._draw_pl_flag)
        self._flag(flags, "uk", self._draw_uk_ua_flag)

        # --- Spenden-Knopf (links neben den Flaggen) ---
        donate = tk.Label(header, text=t("♥ Unterstuetzen"), bg=AMBER,
                          fg="#1c212b", font=("Segoe UI", 10, "bold"),
                          padx=12, pady=6, cursor="hand2")
        donate.pack(side="right", padx=(0, 6), pady=10)
        donate.bind("<Button-1>", lambda e: self._open_donate())

        # --- Beginner/Expert-Umschalter oben mittig ---
        # expand=True ohne fill -> zentriert sich im verbleibenden Platz.
        center = tk.Frame(header, bg=BG_PANEL)
        center.pack(side="left", expand=True)
        tk.Label(center, text=t("Modus:"), bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 8))
        switch = tk.Frame(center, bg=BG_INPUT)
        switch.pack(side="left")
        for mode, label in (("beginner", "Beginner"), ("expert", "Expert")):
            active = (self.mode == mode)
            chip = tk.Label(switch, text=t(label),
                            bg=(MARINE if active else BG_INPUT),
                            fg=("#ffffff" if active else TEXT_DIM),
                            font=("Segoe UI", 10, "bold"),
                            padx=16, pady=6, cursor="hand2")
            chip.pack(side="left", padx=1, pady=1)
            chip.bind("<Button-1>", lambda e, m=mode: self.set_mode(m))

    def _flag(self, parent, lang: str, drawer) -> None:
        active = (i18n.get_language() == lang)
        cv = tk.Canvas(parent, width=34, height=22, bg=BG_PANEL,
                       highlightthickness=2, cursor="hand2",
                       highlightbackground=(MARINE_BRIGHT if active else BG_PANEL))
        drawer(cv)
        cv.pack(side="left", padx=4, pady=10)
        cv.bind("<Button-1>", lambda e, l=lang: self.set_language(l))

    @staticmethod
    def _draw_de_flag(cv: tk.Canvas) -> None:
        # Drei waagerechte Streifen: schwarz / rot / gold.
        w, h = 32, 20
        cv.create_rectangle(1, 1, w + 1, h / 3 + 1, fill="#000000", outline="")
        cv.create_rectangle(1, h / 3 + 1, w + 1, 2 * h / 3 + 1, fill="#DD0000",
                            outline="")
        cv.create_rectangle(1, 2 * h / 3 + 1, w + 1, h + 1, fill="#FFCE00",
                            outline="")

    @staticmethod
    def _draw_uk_flag(cv: tk.Canvas) -> None:
        # Vereinfachter Union Jack.
        w, h = 32, 20
        ox, oy = 1, 1
        cv.create_rectangle(ox, oy, ox + w, oy + h, fill="#012169", outline="")
        # weisse Diagonalen, darueber rote (duenner)
        cv.create_line(ox, oy, ox + w, oy + h, fill="white", width=4)
        cv.create_line(ox + w, oy, ox, oy + h, fill="white", width=4)
        cv.create_line(ox, oy, ox + w, oy + h, fill="#C8102E", width=2)
        cv.create_line(ox + w, oy, ox, oy + h, fill="#C8102E", width=2)
        # weisses Kreuz, darueber rotes (duenner)
        cv.create_rectangle(ox + w / 2 - 4, oy, ox + w / 2 + 4, oy + h,
                            fill="white", outline="")
        cv.create_rectangle(ox, oy + h / 2 - 3, ox + w, oy + h / 2 + 3,
                            fill="white", outline="")
        cv.create_rectangle(ox + w / 2 - 2, oy, ox + w / 2 + 2, oy + h,
                            fill="#C8102E", outline="")
        cv.create_rectangle(ox, oy + h / 2 - 2, ox + w, oy + h / 2 + 2,
                            fill="#C8102E", outline="")

    @staticmethod
    def _draw_es_flag(cv: tk.Canvas) -> None:
        # Spanien: rot / gelb (doppelt hoch) / rot.
        w, h = 32, 20
        cv.create_rectangle(1, 1, w + 1, h + 1, fill="#AA151B", outline="")
        cv.create_rectangle(1, h / 4 + 1, w + 1, 3 * h / 4 + 1, fill="#F1BF00",
                            outline="")

    @staticmethod
    def _draw_pl_flag(cv: tk.Canvas) -> None:
        # Polen: weiss oben, rot unten.
        w, h = 32, 20
        cv.create_rectangle(1, 1, w + 1, h / 2 + 1, fill="#FFFFFF", outline="")
        cv.create_rectangle(1, h / 2 + 1, w + 1, h + 1, fill="#DC143C", outline="")

    @staticmethod
    def _draw_fr_flag(cv: tk.Canvas) -> None:
        # Frankreich: blau / weiss / rot (senkrecht).
        w, h = 32, 20
        cv.create_rectangle(1, 1, w / 3 + 1, h + 1, fill="#0055A4", outline="")
        cv.create_rectangle(w / 3 + 1, 1, 2 * w / 3 + 1, h + 1, fill="#FFFFFF",
                            outline="")
        cv.create_rectangle(2 * w / 3 + 1, 1, w + 1, h + 1, fill="#EF4135",
                            outline="")

    @staticmethod
    def _draw_uk_ua_flag(cv: tk.Canvas) -> None:
        # Ukraine: blau oben, gelb unten.
        w, h = 32, 20
        cv.create_rectangle(1, 1, w + 1, h / 2 + 1, fill="#0057B7", outline="")
        cv.create_rectangle(1, h / 2 + 1, w + 1, h + 1, fill="#FFD700", outline="")

    # ------------------------------------------------------------ Statusbar
    def _build_statusbar(self) -> None:
        self.status = tk.StringVar(value=t("Bereit."))
        bar = tk.Frame(self.container, bg=BG_PANEL)
        bar.pack(fill="x", side="bottom")
        tk.Label(bar, textvariable=self.status, bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=16, pady=6)

    def _make_tree(self, parent, columns: list[tuple[str, str, int, str]]):
        """Hilfsfunktion: Treeview mit Scrollbar. columns: (id, text, breite, anchor)."""
        wrap = tk.Frame(parent, bg=BG_DARK)
        wrap.pack(fill="both", expand=True, padx=12, pady=8)
        tree = ttk.Treeview(wrap, columns=[c[0] for c in columns],
                            show="headings", selectmode="extended")
        for cid, text, width, anchor in columns:
            tree.heading(cid, text=text)
            stretch = (cid == "path")
            tree.column(cid, width=width, anchor=anchor, stretch=stretch)
        tree.tag_configure("warn", foreground=AMBER)
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._attach_context_menu(tree)
        tree.bind("<Double-1>", lambda e, tr=tree: self._open_in_explorer(tr))
        return tree

    def _attach_context_menu(self, tree) -> None:
        """Haengt ein Rechtsklick-Menue 'springe in den Ordner' an eine Tabelle."""
        menu = tk.Menu(tree, tearoff=0, bg=BG_PANEL, fg=MARINE_TEXT,
                       activebackground=MARINE, activeforeground="#ffffff",
                       borderwidth=0)
        menu.add_command(label=t("Springe in den Ordner"),
                         command=lambda: self._open_in_explorer(tree))

        def popup(event):
            row = tree.identify_row(event.y)
            if not row:
                return
            if row not in tree.selection():
                tree.selection_set(row)
            menu.tk_popup(event.x_root, event.y_root)

        tree.bind("<Button-3>", popup)

    def _open_in_explorer(self, tree) -> None:
        """Oeffnet den Pfad der ausgewaehlten Zeile im Windows-Explorer."""
        sel = tree.selection()
        if not sel:
            return
        cols = list(tree["columns"])
        if "path" not in cols:
            return
        values = tree.item(sel[0], "values")
        path = Path(values[cols.index("path")])
        try:
            if path.is_file():
                subprocess.Popen(f'explorer /select,"{path}"')
            elif path.is_dir():
                os.startfile(str(path))
            elif path.parent.is_dir():
                os.startfile(str(path.parent))
            else:
                messagebox.showinfo(t("Nicht gefunden"),
                                    t("Der Pfad existiert nicht mehr:\n{path}")
                                    .format(path=path))
        except OSError as exc:
            messagebox.showerror(t("Fehler"),
                                 t("Konnte nicht oeffnen:\n{exc}").format(exc=exc))

    # =================================================== Hintergrund-Helfer
    def _run_bg(self, work, on_done, status_msg: str) -> None:
        """Fuehrt work() im Thread aus und ruft danach on_done(ergebnis) im UI-Thread."""
        self.status.set(status_msg)
        q: queue.Queue = queue.Queue()

        def wrapped():
            try:
                q.put(("ok", work()))
            except Exception as exc:  # noqa: BLE001
                q.put(("error", exc))

        threading.Thread(target=wrapped, daemon=True).start()

        def poll():
            try:
                kind, payload = q.get_nowait()
            except queue.Empty:
                self.root.after(150, poll)
                return
            if kind == "error":
                self.status.set(t("Fehler: {err}").format(err=payload))
                messagebox.showerror(t("Fehler"), str(payload))
                on_done(None)
            else:
                on_done(payload)

        self.root.after(150, poll)

    # ===================================================== TAB 1: Verwaiste Ordner
    def _build_orphan_tab(self) -> None:
        tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(tab, text=t("  Verwaiste Ordner  "))

        bar = tk.Frame(tab, bg=BG_DARK)
        bar.pack(fill="x", padx=12, pady=(10, 0))
        self.o_scan = ttk.Button(bar, text=t("Scan starten"), style="Marine.TButton",
                                 command=self.scan_orphans)
        self.o_scan.pack(side="left")
        self.o_del = ttk.Button(bar, text=t("Auswahl in Papierkorb"),
                                style="Marine.TButton", state="disabled",
                                command=self.delete_orphans)
        self.o_del.pack(side="left", padx=(10, 0))
        tk.Label(bar, text=t("Mindest-Sicherheit:"), bg=BG_DARK,
                 fg=MARINE_TEXT).pack(side="left", padx=(24, 6))
        self.min_conf = tk.IntVar(value=50)
        ttk.Spinbox(bar, from_=0, to=100, increment=5, width=5,
                    textvariable=self.min_conf).pack(side="left")
        tk.Label(bar, text="%", bg=BG_DARK, fg=MARINE_TEXT).pack(side="left")
        tk.Label(bar, text=t("ungenutzt seit (Monate):"), bg=BG_DARK,
                 fg=MARINE_TEXT).pack(side="left", padx=(20, 6))
        self.o_months = tk.IntVar(value=6)
        ttk.Spinbox(bar, from_=0, to=120, increment=1, width=5,
                    textvariable=self.o_months).pack(side="left")

        self.o_tree = self._make_tree(tab, [
            ("conf", t("Sicher"), 60, "center"),
            ("size", t("Groesse"), 90, "e"),
            ("age", t("Zuletzt genutzt"), 120, "center"),
            ("cat", t("Kategorie"), 120, "w"),
            ("path", t("Ordner"), 320, "w"),
            ("warn", t("Warnung"), 200, "w"),
        ])

    def scan_orphans(self) -> None:
        self.o_scan.config(state="disabled")
        self.o_del.config(state="disabled")
        self.o_tree.delete(*self.o_tree.get_children())
        mc = self.min_conf.get()
        min_age = self.o_months.get() * 30
        self._run_bg(lambda: find_orphans(min_confidence=mc, min_age_days=min_age),
                     self._orphans_done,
                     t("Scanne alle Laufwerke (das kann eine Weile dauern) ..."))

    def _orphans_done(self, result) -> None:
        self.o_scan.config(state="normal")
        if result is None:
            return
        self.orphans = result
        total = sum(c.folder.size_bytes for c in result)
        for i, c in enumerate(result):
            tags = ("warn",) if c.warning else ()
            self.o_tree.insert("", "end", iid=str(i), tags=tags, values=(
                f"{c.confidence}%", human_size(c.folder.size_bytes),
                human_age(c.folder.last_modified), c.folder.category,
                str(c.folder.path), t(c.warning) if c.warning else ""))
        self.o_del.config(state="normal" if result else "disabled")
        self.status.set(
            t("{n} Kandidaten  |  potentiell {size} frei. Zeilen auswaehlen "
              "(Strg/Shift).").format(n=len(result), size=human_size(total)))

    def delete_orphans(self) -> None:
        ids = self.o_tree.selection()
        if not ids:
            messagebox.showinfo(t("Keine Auswahl"), t("Bitte zuerst Zeilen auswaehlen."))
            return
        chosen = [self.orphans[int(i)] for i in ids]
        approved, rejected = [], []
        for c in chosen:
            safe, reason = is_safe_to_delete(c.folder)
            (approved.append(c) if safe else rejected.append((c, reason)))
        if rejected:
            msg = "\n".join(f"- {c.folder.path}\n   ({t(r)})" for c, r in rejected)
            messagebox.showwarning(t("Abgelehnt"),
                                   t("Diese werden NICHT geloescht:\n\n") + msg)
        if not approved:
            self.status.set(t("Nichts Sicheres ausgewaehlt."))
            return

        total = sum(c.folder.size_bytes for c in approved)
        has_warn = any(c.warning for c in approved)
        preview = "\n".join(f"- {human_size(c.folder.size_bytes):>9}  {c.folder.path}"
                            for c in approved[:20])
        if len(approved) > 20:
            preview += "\n" + t("... und {n} weitere").format(n=len(approved) - 20)
        warn = t("\n\nACHTUNG: Mindestens ein grosser Ordner koennte ein aktives\n"
                 "Spiel/Programm sein!") if has_warn else ""
        if not messagebox.askyesno(
                t("In den Papierkorb verschieben?"),
                t("{n} Ordner -> PAPIERKORB (wiederherstellbar).\nFrei werden: "
                  "{size}.\n\n{preview}{warn}\n\nFortfahren?").format(
                    n=len(approved), size=human_size(total), preview=preview,
                    warn=warn)):
            self.status.set(t("Abgebrochen."))
            return
        if not messagebox.askyesno(
                t("Sind Sie sicher?"),
                t("Wirklich {n} Ordner ({size}) in den Papierkorb verschieben?")
                .format(n=len(approved), size=human_size(total)),
                icon="warning", default="no"):
            self.status.set(t("Nicht bestaetigt."))
            return

        results = delete_candidates(approved)
        freed = sum(r.size_bytes for r in results if r.success)
        ok = sum(1 for r in results if r.success)
        done = {str(r.path) for r in results if r.success}
        self.orphans = [c for c in self.orphans if str(c.folder.path) not in done]
        self.o_tree.delete(*self.o_tree.get_children())
        self._orphans_done(self.orphans)
        self.status.set(
            t("{ok} Ordner in den Papierkorb verschoben, {size} frei. "
              "Protokoll: {log}").format(ok=ok, size=human_size(freed),
                                         log=DEFAULT_LOG))

    # ===================================================== TAB 2: Temp-Dateien
    def _build_temp_tab(self) -> None:
        tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(tab, text=t("  Temp-Dateien  "))

        bar = tk.Frame(tab, bg=BG_DARK)
        bar.pack(fill="x", padx=12, pady=(10, 0))
        self.t_scan = ttk.Button(bar, text=t("Temp scannen"), style="Marine.TButton",
                                 command=self.scan_temp_files)
        self.t_scan.pack(side="left")
        self.t_clean = ttk.Button(bar, text=t("Temp leeren (endgueltig)"),
                                  style="Marine.TButton", state="disabled",
                                  command=self.clean_temp_files)
        self.t_clean.pack(side="left", padx=(10, 0))
        tk.Label(bar, text=t("nur aelter als (Tage):"), bg=BG_DARK,
                 fg=MARINE_TEXT).pack(side="left", padx=(24, 6))
        self.temp_age = tk.IntVar(value=0)
        ttk.Spinbox(bar, from_=0, to=365, increment=1, width=5,
                    textvariable=self.temp_age).pack(side="left")

        tk.Label(tab, text=t("Temp-Dateien werden ENDGUELTIG geloescht (nicht in "
                             "den Papierkorb), damit der Platz wirklich frei wird. "
                             "Gesperrte Dateien bleiben unangetastet."),
                 bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(fill="x", padx=14, pady=(8, 0))

        self.t_tree = self._make_tree(tab, [
            ("size", t("Groesse"), 120, "e"),
            ("count", t("Dateien"), 100, "center"),
            ("path", t("Temp-Ordner"), 600, "w"),
        ])

    def scan_temp_files(self) -> None:
        self.t_scan.config(state="disabled")
        self.t_clean.config(state="disabled")
        self.t_tree.delete(*self.t_tree.get_children())
        self._run_bg(scan_temp, self._temp_done, t("Scanne Temp-Ordner ..."))

    def _temp_done(self, result) -> None:
        self.t_scan.config(state="normal")
        if result is None:
            return
        self.temp_locs = result
        total = sum(l.size_bytes for l in result)
        for l in result:
            self.t_tree.insert("", "end", values=(
                human_size(l.size_bytes), f"{l.file_count}", str(l.path)))
        self.t_clean.config(state="normal" if total else "disabled")
        self.status.set(t("Temp gesamt: {size}. 'Temp leeren' gibt diesen Platz "
                          "frei.").format(size=human_size(total)))

    def clean_temp_files(self) -> None:
        total = sum(l.size_bytes for l in self.temp_locs)
        days = self.temp_age.get()
        age_txt = (t("\n(nur Dateien aelter als {days} Tage)").format(days=days)
                   if days else "")
        if not messagebox.askyesno(
                t("Temp-Dateien endgueltig loeschen?"),
                t("Temporaere Dateien werden ENDGUELTIG geloescht (NICHT in den "
                  "Papierkorb).{age}\n\nGeschaetzt frei: bis zu {size}.\n"
                  "Gesperrte/benutzte Dateien werden uebersprungen.\n\nFortfahren?")
                .format(age=age_txt, size=human_size(total)),
                icon="warning", default="no"):
            self.status.set(t("Abgebrochen."))
            return
        if not messagebox.askyesno(t("Sind Sie sicher?"),
                                   t("Temp-Dateien wirklich endgueltig loeschen?"),
                                   icon="warning", default="no"):
            self.status.set(t("Nicht bestaetigt."))
            return
        self.t_clean.config(state="disabled")
        self.t_scan.config(state="disabled")
        self._run_bg(lambda: clean_temp(min_age_days=days),
                     self._temp_cleaned, t("Loesche Temp-Dateien ..."))

    def _temp_cleaned(self, result) -> None:
        self.t_scan.config(state="normal")
        if result is None:
            return
        messagebox.showinfo(
            t("Fertig"),
            t("{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
              "(gesperrt/zu jung).").format(
                n=result.deleted_files, size=human_size(result.freed_bytes),
                skip=result.skipped_files))
        self.scan_temp_files()

    # ===================================================== TAB 3: Grosse Dateien
    def _build_bigfiles_tab(self) -> None:
        tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(tab, text=t("  Grosse Dateien  "))

        bar = tk.Frame(tab, bg=BG_DARK)
        bar.pack(fill="x", padx=12, pady=(10, 0))
        self.b_scan = ttk.Button(bar, text=t("Grosse Dateien suchen"),
                                 style="Marine.TButton", command=self.scan_big_files)
        self.b_scan.pack(side="left")
        self.b_del = ttk.Button(bar, text=t("Auswahl in Papierkorb"),
                                style="Marine.TButton", state="disabled",
                                command=self.delete_big_files)
        self.b_del.pack(side="left", padx=(10, 0))
        tk.Label(bar, text=t("ab Groesse (MB):"), bg=BG_DARK, fg=MARINE_TEXT).pack(
            side="left", padx=(24, 6))
        self.big_min = tk.IntVar(value=500)
        ttk.Spinbox(bar, from_=50, to=20000, increment=50, width=7,
                    textvariable=self.big_min).pack(side="left")
        tk.Label(bar, text=t("ungenutzt seit (Monate):"), bg=BG_DARK,
                 fg=MARINE_TEXT).pack(side="left", padx=(20, 6))
        self.big_months = tk.IntVar(value=6)
        ttk.Spinbox(bar, from_=0, to=120, increment=1, width=5,
                    textvariable=self.big_months).pack(side="left")

        tk.Label(tab, text=t("Findet die groessten Einzeldateien (z.B. alte Videos, "
                             "ISO-Dateien). Amber = kuerzlich genutzt (evtl. aktives "
                             "Spiel/Programm). Loeschen geht in den Papierkorb."),
                 bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(fill="x", padx=14, pady=(8, 0))

        self.b_tree = self._make_tree(tab, [
            ("size", t("Groesse"), 110, "e"),
            ("age", t("Zuletzt genutzt"), 130, "center"),
            ("path", t("Datei"), 660, "w"),
        ])

    def scan_big_files(self) -> None:
        self.b_scan.config(state="disabled")
        self.b_del.config(state="disabled")
        self.b_tree.delete(*self.b_tree.get_children())
        min_bytes = self.big_min.get() * 1_000_000
        min_age = self.big_months.get() * 30
        self._run_bg(
            lambda: find_large_files(top_n=60, min_size_bytes=min_bytes,
                                     min_age_days=min_age),
            self._big_done,
            t("Durchsuche alle Laufwerke nach grossen Dateien (dauert) ..."))

    def _big_done(self, result) -> None:
        self.b_scan.config(state="normal")
        if result is None:
            return
        self.big = result
        total = sum(b.size_bytes for b in result)
        for i, b in enumerate(result):
            recent = 0 <= age_days(b.last_modified) < 30
            tags = ("warn",) if recent else ()
            self.b_tree.insert("", "end", iid=str(i), tags=tags, values=(
                human_size(b.size_bytes), human_age(b.last_modified), str(b.path)))
        self.b_del.config(state="normal" if result else "disabled")
        self.status.set(t("{n} grosse Dateien  |  zusammen {size}. Amber = "
                          "kuerzlich genutzt.").format(n=len(result),
                                                       size=human_size(total)))

    def delete_big_files(self) -> None:
        ids = self.b_tree.selection()
        if not ids:
            messagebox.showinfo(t("Keine Auswahl"), t("Bitte zuerst Dateien auswaehlen."))
            return
        chosen = [self.big[int(i)] for i in ids]
        approved, rejected = [], []
        for b in chosen:
            safe, reason = is_safe_to_delete_file(b.path)
            (approved.append(b) if safe else rejected.append((b, reason)))
        if rejected:
            msg = "\n".join(f"- {b.path}\n   ({t(r)})" for b, r in rejected)
            messagebox.showwarning(t("Abgelehnt"),
                                   t("Diese werden NICHT geloescht:\n\n") + msg)
        if not approved:
            self.status.set(t("Nichts Sicheres ausgewaehlt."))
            return
        total = sum(b.size_bytes for b in approved)
        recent = any(0 <= age_days(b.last_modified) < 30 for b in approved)
        preview = "\n".join(f"- {human_size(b.size_bytes):>9}  {b.path}"
                            for b in approved[:20])
        if len(approved) > 20:
            preview += "\n" + t("... und {n} weitere").format(n=len(approved) - 20)
        warn = t("\n\nACHTUNG: Mindestens eine Datei wurde kuerzlich genutzt -\n"
                 "evtl. ein aktives Spiel/Programm!") if recent else ""
        if not messagebox.askyesno(
                t("In den Papierkorb verschieben?"),
                t("{n} Dateien -> PAPIERKORB (wiederherstellbar).\nFrei werden: "
                  "{size}.\n\n{preview}{warn}\n\nFortfahren?").format(
                    n=len(approved), size=human_size(total), preview=preview,
                    warn=warn)):
            self.status.set(t("Abgebrochen."))
            return
        if not messagebox.askyesno(
                t("Sind Sie sicher?"),
                t("Wirklich {n} Dateien ({size}) in den Papierkorb?").format(
                    n=len(approved), size=human_size(total)),
                icon="warning", default="no"):
            self.status.set(t("Nicht bestaetigt."))
            return
        freed, ok, done = 0, 0, set()
        for b in approved:
            res = trash_path(b.path, b.size_bytes)
            if res.success:
                ok += 1
                freed += b.size_bytes
                done.add(str(b.path))
        self.big = [b for b in self.big if str(b.path) not in done]
        self.b_tree.delete(*self.b_tree.get_children())
        self._big_done(self.big)
        self.status.set(t("{ok} Dateien in den Papierkorb verschoben, {size} frei.")
                        .format(ok=ok, size=human_size(freed)))

    # ================================================ TAB 4: Windows-Update
    def _build_update_tab(self) -> None:
        tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(tab, text=t("  Windows-Update  "))

        bar = tk.Frame(tab, bg=BG_DARK)
        bar.pack(fill="x", padx=12, pady=(10, 0))
        self.u_scan = ttk.Button(bar, text=t("Update-Cache scannen"),
                                 style="Marine.TButton", command=self.scan_update)
        self.u_scan.pack(side="left")
        self.u_clean = ttk.Button(bar, text=t("Update-Cache leeren"),
                                  style="Marine.TButton", state="disabled",
                                  command=self.clean_update)
        self.u_clean.pack(side="left", padx=(10, 0))

        tk.Label(tab, text=t("Heruntergeladene Windows-Update-Pakete "
                             "(SoftwareDistribution\\Download) sind nach der "
                             "Installation nutzlos. Sie werden ENDGUELTIG geloescht "
                             "und von Windows bei Bedarf neu angelegt."),
                 bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(fill="x", padx=14, pady=(10, 4))

        self.u_info = tk.StringVar(value="")
        info_box = tk.Frame(tab, bg=BG_INPUT)
        info_box.pack(fill="x", padx=12, pady=8)
        tk.Label(info_box, textvariable=self.u_info, bg=BG_INPUT, fg=MARINE_TEXT,
                 font=("Segoe UI", 11), justify="left", anchor="w").pack(
            fill="x", padx=16, pady=14)

        self.u_admin = tk.StringVar(value="")
        admin_row = tk.Frame(tab, bg=BG_DARK)
        admin_row.pack(fill="x", padx=14)
        tk.Label(admin_row, textvariable=self.u_admin, bg=BG_DARK, fg=AMBER,
                 font=("Segoe UI", 9), justify="left").pack(side="left")
        self.u_elevate = ttk.Button(admin_row, text=t("Als Administrator neu starten"),
                                    style="Marine.TButton",
                                    command=self.restart_as_admin)
        if not is_admin():
            self.u_admin.set(t("Hinweis: Zum Leeren werden Administrator-Rechte "
                               "benoetigt. "))
            self.u_elevate.pack(side="left", padx=(6, 0), pady=6)

        # --- DISM: Komponentenspeicher (WinSxS) ---------------------------
        tk.Label(tab, text=t("Komponentenspeicher (WinSxS) - DISM"), bg=BG_DARK,
                 fg=MARINE_BRIGHT, font=("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=16, pady=(20, 0))
        tk.Label(tab, text=t("Raeumt alte, durch Updates ersetzte Windows-"
                             "Komponenten gruendlicher auf als die "
                             "Datentraegerbereinigung. '/ResetBase' entfernt auch "
                             "ersetzte Versionen endgueltig - danach lassen sich "
                             "installierte Updates aber NICHT mehr deinstallieren. "
                             "Braucht Admin und kann einige Minuten dauern."),
                 bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(anchor="w", padx=16, pady=(2, 4))
        tk.Label(tab, text=t("WICHTIG: WinSxS bleibt IMMER mehrere GB gross (vieles "
                             "ist mit Windows geteilt) - das ist normal. Und "
                             "'empfohlen: Ja' steht schon ab 1 ersetzten Paket - auf "
                             "einem aktuellen Windows fast immer. Massgeblich ist die "
                             "Anzahl 'bereinigbarer Pakete' (0-2 = gesund), NICHT die "
                             "'empfohlen'-Zeile."),
                 bg=BG_DARK, fg=AMBER, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(anchor="w", padx=16, pady=(0, 4))

        dbar = tk.Frame(tab, bg=BG_DARK)
        dbar.pack(fill="x", padx=14)
        self.dism_analyze_btn = ttk.Button(dbar, text=t("Analysieren"),
                                           style="Marine.TButton",
                                           command=self.dism_analyze)
        self.dism_analyze_btn.pack(side="left")
        self.dism_clean_btn = ttk.Button(dbar, text=t("Bereinigen"),
                                         style="Marine.TButton",
                                         command=self.dism_clean)
        self.dism_clean_btn.pack(side="left", padx=(10, 0))
        self.dism_reset = tk.BooleanVar(value=False)
        tk.Checkbutton(dbar, text=t("ResetBase (gruendlicher)"),
                       variable=self.dism_reset, bg=BG_DARK, fg=MARINE_TEXT,
                       selectcolor=BG_INPUT, activebackground=BG_DARK,
                       activeforeground=MARINE_BRIGHT,
                       font=("Segoe UI", 9)).pack(side="left", padx=(16, 0))

        self.dism_prog_frame = tk.Frame(tab, bg=BG_DARK)
        self.dism_prog_label = tk.Label(
            self.dism_prog_frame,
            text=t("Vorgang laeuft - bitte warten (die Anzeige bewegt sich):"),
            bg=BG_DARK, fg=MARINE_BRIGHT, font=("Segoe UI", 9, "bold"), anchor="w")
        self.dism_prog_label.pack(fill="x", padx=2, pady=(0, 2))
        self.dism_progress = ttk.Progressbar(
            self.dism_prog_frame, mode="indeterminate",
            style="Marine.Horizontal.TProgressbar")
        self.dism_progress.pack(fill="x")

        out_wrap = tk.Frame(tab, bg=BG_DARK)
        out_wrap.pack(fill="both", expand=True, padx=14, pady=8)
        self.dism_out = tk.Text(out_wrap, height=8, bg=BG_INPUT, fg=MARINE_TEXT,
                                insertbackground=MARINE_TEXT, borderwidth=0,
                                font=("Consolas", 9), wrap="word", state="disabled")
        dvsb = ttk.Scrollbar(out_wrap, orient="vertical", command=self.dism_out.yview)
        self.dism_out.configure(yscrollcommand=dvsb.set)
        self.dism_out.pack(side="left", fill="both", expand=True)
        dvsb.pack(side="right", fill="y")

    def _set_dism_output(self, text: str) -> None:
        self.dism_out.config(state="normal")
        self.dism_out.delete("1.0", "end")
        self.dism_out.insert("1.0", text)
        self.dism_out.config(state="disabled")

    def _dism_running(self, active: bool) -> None:
        state = "disabled" if active else "normal"
        self.dism_analyze_btn.config(state=state)
        self.dism_clean_btn.config(state=state)
        if active:
            self.dism_prog_frame.pack(fill="x", padx=16, pady=(6, 2),
                                      before=self.dism_out.master)
            self.dism_progress.start(12)
        else:
            self.dism_progress.stop()
            self.dism_prog_frame.pack_forget()

    def dism_analyze(self) -> None:
        if not self._require_admin():
            return
        self._dism_running(True)
        self._set_dism_output(
            t("Analysiere Komponentenspeicher ... bitte warten.\n\nSolange die "
              "blaue Anzeige sich bewegt, laeuft der Vorgang - das Fenster bitte "
              "NICHT schliessen."))
        self._run_bg(analyze_component_store, self._dism_done,
                     t("DISM analysiert den Komponentenspeicher ..."))

    def dism_clean(self) -> None:
        if not self._require_admin():
            return
        reset = self.dism_reset.get()
        extra = (t("\n\nACHTUNG ResetBase: installierte Updates lassen sich danach "
                   "NICHT mehr deinstallieren.") if reset else "")
        if not messagebox.askyesno(
                t("Komponentenspeicher bereinigen?"),
                t("DISM raeumt jetzt den WinSxS-Speicher auf.\n\nWICHTIG: Das kann "
                  "10-20 Minuten dauern und zeigt KEINEN Fortschritt in Prozent. "
                  "Das Fenster bitte offen lassen und warten - es ist nicht "
                  "eingefroren.{extra}\n\nFortfahren?").format(extra=extra),
                icon="warning", default="no"):
            self.status.set(t("Abgebrochen."))
            return
        self._dism_running(True)
        self._set_dism_output(
            t("Bereinige Komponentenspeicher ... das kann 10-20 Minuten dauern."
              "\n\nSolange die blaue Anzeige sich bewegt, laeuft der Vorgang - das "
              "Fenster bitte NICHT schliessen und warten. Es ist NICHT eingefroren."))
        self._run_bg(lambda: start_component_cleanup(reset_base=reset),
                     self._dism_done, t("DISM bereinigt den Komponentenspeicher ..."))

    def _dism_done(self, result) -> None:
        self._dism_running(False)
        if result is None:
            return
        ok, output = result
        output = output or (t("Erfolgreich.") if ok else t("Fehler."))
        self._set_dism_output(summarize_analysis(output) + output)
        self.status.set(t("DISM fertig.") if ok else t("DISM meldete einen Fehler."))

    def _require_admin(self) -> bool:
        if is_admin():
            return True
        if messagebox.askyesno(
                t("Administrator noetig"),
                t("DISM braucht Administrator-Rechte.\n\nJetzt als Administrator "
                  "neu starten?")):
            self.restart_as_admin()
        return False

    def scan_update(self) -> None:
        self.u_scan.config(state="disabled")
        self.u_clean.config(state="disabled")
        self._run_bg(scan_update_cache, self._update_done,
                     t("Scanne Windows-Update-Cache ..."))

    def _update_done(self, info) -> None:
        self.u_scan.config(state="normal")
        if info is None:
            return
        if not info.exists:
            self.u_info.set(t("Ordner nicht vorhanden:\n{path}").format(path=info.path))
            return
        admin_txt = t("ja") if is_admin() else t("nein (zum Leeren noetig)")
        self.u_info.set(
            t("Groesse:  {size}   ({n} Dateien)\nOrdner:   {path}\nAdmin:    {admin}")
            .format(size=human_size(info.size_bytes), n=info.file_count,
                    path=info.path, admin=admin_txt))
        can_clean = info.size_bytes > 0 and is_admin()
        self.u_clean.config(state="normal" if can_clean else "disabled")
        self.status.set(t("Update-Cache: {size}.").format(
            size=human_size(info.size_bytes)))

    def clean_update(self) -> None:
        if not is_admin():
            messagebox.showwarning(
                t("Administrator noetig"),
                t("Zum Leeren des Update-Caches sind Administrator-Rechte noetig.\n"
                  "Bitte 'Als Administrator neu starten' verwenden."))
            return
        if not messagebox.askyesno(
                t("Update-Cache leeren?"),
                t("Heruntergeladene Update-Pakete werden ENDGUELTIG geloescht.\nDie "
                  "Update-Dienste werden kurz angehalten und danach wieder "
                  "gestartet.\n\nFortfahren?"), icon="warning", default="no"):
            self.status.set(t("Abgebrochen."))
            return
        if not messagebox.askyesno(t("Sind Sie sicher?"),
                                   t("Update-Cache wirklich endgueltig leeren?"),
                                   icon="warning", default="no"):
            self.status.set(t("Nicht bestaetigt."))
            return
        self.u_clean.config(state="disabled")
        self.u_scan.config(state="disabled")
        self._run_bg(lambda: clean_update_cache(manage_services=True),
                     self._update_cleaned, t("Stoppe Dienste und leere Cache ..."))

    def _update_cleaned(self, result) -> None:
        self.u_scan.config(state="normal")
        if result is None:
            return
        if result.admin_required:
            messagebox.showwarning(
                t("Administrator noetig"),
                t("Es fehlten Administrator-Rechte. Bitte als Administrator neu "
                  "starten."))
            return
        svc = (t("Dienste wurden gestoppt und neu gestartet.")
               if result.services_stopped else
               t("Hinweis: Dienste konnten nicht gestoppt werden - gesperrte "
                 "Dateien wurden uebersprungen."))
        messagebox.showinfo(
            t("Fertig"),
            t("{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen."
              "\n\n{svc}").format(n=result.deleted_files,
                                  size=human_size(result.freed_bytes),
                                  skip=result.skipped_files, svc=svc))
        self.scan_update()

    def restart_as_admin(self) -> None:
        if is_admin():
            messagebox.showinfo(t("Bereits Administrator"),
                                t("Das Programm laeuft bereits mit Admin-Rechten."))
            return
        if relaunch_as_admin():
            self.root.destroy()
            sys.exit(0)
        else:
            messagebox.showerror(
                t("Fehlgeschlagen"),
                t("Neustart als Administrator wurde abgebrochen oder ist "
                  "fehlgeschlagen."))

    # ==================================================== TAB 5: Windows.old
    def _build_winold_tab(self) -> None:
        tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(tab, text=t("  Windows.old  "))

        bar = tk.Frame(tab, bg=BG_DARK)
        bar.pack(fill="x", padx=12, pady=(10, 0))
        self.w_scan = ttk.Button(bar, text=t("Windows.old pruefen"),
                                 style="Marine.TButton", command=self.scan_winold)
        self.w_scan.pack(side="left")
        self.w_clean = ttk.Button(
            bar, text=t("Datenträgerbereinigung oeffnen (Windows.old u.a. "
                        "Systemreste)"),
            style="Marine.TButton", state="disabled", command=self.remove_winold)
        self.w_clean.pack(side="left", padx=(10, 0))
        self.w_settings = ttk.Button(bar, text=t("Speicher-Einstellungen"),
                                     style="Marine.TButton",
                                     command=lambda: open_storage_settings())
        self.w_settings.pack(side="left", padx=(10, 0))

        tk.Label(tab, text=t("'Windows.old' enthaelt die vorherige Windows-Version "
                             "nach einem Upgrade (oft 20-70 GB). Es laesst sich "
                             "NICHT normal loeschen, weil es dem System gehoert "
                             "(TrustedInstaller-Sperre). Der sichere Weg ist die "
                             "Windows-Datenträgerbereinigung: dort 'Vorherige "
                             "Windows-Installation(en)' anhaken."),
                 bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(fill="x", padx=14, pady=(10, 4))

        self.w_info = tk.StringVar(value="")
        info_box = tk.Frame(tab, bg=BG_INPUT)
        info_box.pack(fill="x", padx=12, pady=8)
        tk.Label(info_box, textvariable=self.w_info, bg=BG_INPUT, fg=MARINE_TEXT,
                 font=("Segoe UI", 11), justify="left", anchor="w").pack(
            fill="x", padx=16, pady=14)

    def scan_winold(self) -> None:
        self.w_scan.config(state="disabled")
        self.w_clean.config(state="disabled")
        self._run_bg(scan_windows_old, self._winold_done,
                     t("Pruefe Windows.old (Groesse berechnen kann dauern) ..."))

    def _winold_done(self, result) -> None:
        self.w_scan.config(state="normal")
        if result is None:
            return
        exists, size = result
        if not exists:
            self.w_info.set(t("Kein 'Windows.old' vorhanden - nichts zu tun. :)"))
            self.status.set(t("Kein Windows.old gefunden."))
            return
        self.w_info.set(
            t("Windows.old gefunden:  {size}\nPfad:  {drive}\\Windows.old\n\nKlicke "
              "'Mit Datenträgerbereinigung entfernen' und hake dort\n'Vorherige "
              "Windows-Installation(en)' an.").format(
                size=human_size(size), drive=os.environ.get("SystemDrive", "C:")))
        self.w_clean.config(state="normal")
        self.status.set(t("Windows.old: {size} - ueber die Datenträgerbereinigung "
                          "entfernbar.").format(size=human_size(size)))

    def remove_winold(self) -> None:
        if not messagebox.askyesno(
                t("Datenträgerbereinigung starten?"),
                t("Es wird die Windows-Datenträgerbereinigung (cleanmgr) mit "
                  "Administrator-Rechten gestartet.\n\nDort 'Vorherige Windows-"
                  "Installation(en)' anhaken und auf OK klicken - Windows entfernt "
                  "Windows.old dann sicher selbst.\n\nTipp: Hier lassen sich auch "
                  "weitere Systemreste anhaken (Absturz-Dumps, Delivery-"
                  "Optimization, Update-Bereinigung).\n\nFortfahren?")):
            self.status.set(t("Abgebrochen."))
            return
        if launch_disk_cleanup():
            self.status.set(t("Datenträgerbereinigung gestartet - bitte dort "
                              "'Vorherige Windows-Installation(en)' anhaken."))
        else:
            messagebox.showerror(
                t("Fehlgeschlagen"),
                t("Konnte die Datenträgerbereinigung nicht starten (evtl. UAC "
                  "abgebrochen). Alternativ ueber 'Speicher-Einstellungen'."))

    # ========================================================= TAB 6: Caches
    def _build_caches_tab(self) -> None:
        tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(tab, text=t("  Caches  "))

        bar = tk.Frame(tab, bg=BG_DARK)
        bar.pack(fill="x", padx=12, pady=(10, 0))
        self.c_scan = ttk.Button(bar, text=t("Caches suchen"), style="Marine.TButton",
                                 command=self.scan_caches_ui)
        self.c_scan.pack(side="left")
        self.c_clean = ttk.Button(bar, text=t("Auswahl leeren (endgueltig)"),
                                  style="Marine.TButton", state="disabled",
                                  command=self.clean_caches_ui)
        self.c_clean.pack(side="left", padx=(10, 0))

        tk.Label(tab, text=t("Cache-Ordner von Browsern und Apps. Werden "
                             "automatisch neu aufgebaut und daher ENDGUELTIG "
                             "geleert. Fuer das beste Ergebnis die jeweilige App "
                             "vorher schliessen (gesperrte Dateien werden sonst "
                             "uebersprungen)."),
                 bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(fill="x", padx=14, pady=(8, 0))

        self.c_tree = self._make_tree(tab, [
            ("size", t("Groesse"), 110, "e"),
            ("count", t("Anzahl"), 80, "center"),
            ("app", t("Programm"), 220, "w"),
            ("path", t("Beispielpfad"), 520, "w"),
        ])

    def scan_caches_ui(self) -> None:
        self.c_scan.config(state="disabled")
        self.c_clean.config(state="disabled")
        self.c_tree.delete(*self.c_tree.get_children())
        self._run_bg(scan_caches, self._caches_done, t("Suche Cache-Ordner ..."))

    def _caches_done(self, result) -> None:
        self.c_scan.config(state="normal")
        if result is None:
            return
        self.caches = result
        total = sum(c.size_bytes for c in result)
        for i, c in enumerate(result):
            example = str(c.paths[0]) if c.paths else ""
            self.c_tree.insert("", "end", iid=str(i), values=(
                human_size(c.size_bytes), f"{len(c.paths)}", c.app, example))
        self.c_clean.config(state="normal" if result else "disabled")
        self.status.set(t("{n} Programme mit Cache  |  zusammen {size}. Zeilen "
                          "auswaehlen (Strg/Shift).").format(
                            n=len(result), size=human_size(total)))

    def clean_caches_ui(self) -> None:
        ids = self.c_tree.selection()
        if not ids:
            messagebox.showinfo(t("Keine Auswahl"), t("Bitte zuerst Zeilen auswaehlen."))
            return
        chosen = [self.caches[int(i)] for i in ids]
        total = sum(c.size_bytes for c in chosen)
        names = ", ".join(c.app for c in chosen)
        if not messagebox.askyesno(
                t("Caches endgueltig leeren?"),
                t("Caches von: {names}\n\nbis zu {size} werden ENDGUELTIG geleert "
                  "(nicht in den Papierkorb).\n\nFortfahren?").format(
                    names=names, size=human_size(total)),
                icon="warning", default="no"):
            self.status.set(t("Abgebrochen."))
            return
        if not messagebox.askyesno(t("Sind Sie sicher?"),
                                   t("Ausgewaehlte Caches wirklich leeren?"),
                                   icon="warning", default="no"):
            self.status.set(t("Nicht bestaetigt."))
            return
        self.c_clean.config(state="disabled")
        self.c_scan.config(state="disabled")
        self._run_bg(lambda: clean_caches(chosen), self._caches_cleaned,
                     t("Leere Caches ..."))

    def _caches_cleaned(self, result) -> None:
        self.c_scan.config(state="normal")
        if result is None:
            return
        messagebox.showinfo(
            t("Fertig"),
            t("{n} Dateien geloescht, {size} freigegeben.\n{skip} uebersprungen "
              "(gesperrt - App offen?).").format(
                n=result.deleted_files, size=human_size(result.freed_bytes),
                skip=result.skipped_files))
        self.scan_caches_ui()

    # ========================================================= TAB 7: System
    def _build_system_tab(self) -> None:
        tab = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(tab, text=t("  System  "))

        # --- Papierkorb ---
        tk.Label(tab, text=t("Papierkorb"), bg=BG_DARK, fg=MARINE_BRIGHT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=16, pady=(14, 0))
        tk.Label(tab, text=t("CleanSweep verschiebt Ordner/Dateien in den "
                             "Papierkorb. Der Platz wird erst frei, wenn er geleert "
                             "wird."), bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(anchor="w", padx=16)
        rb_box = tk.Frame(tab, bg=BG_INPUT)
        rb_box.pack(fill="x", padx=14, pady=8)
        self.rb_info = tk.StringVar(value="")
        tk.Label(rb_box, textvariable=self.rb_info, bg=BG_INPUT, fg=MARINE_TEXT,
                 font=("Segoe UI", 11), anchor="w").pack(side="left", padx=16, pady=12)
        rb_bar = tk.Frame(tab, bg=BG_DARK)
        rb_bar.pack(fill="x", padx=14)
        ttk.Button(rb_bar, text=t("Papierkorb pruefen"), style="Marine.TButton",
                   command=self.check_recycle).pack(side="left")
        self.rb_empty = ttk.Button(rb_bar, text=t("Papierkorb leeren"),
                                   style="Marine.TButton", state="disabled",
                                   command=self.empty_recycle)
        self.rb_empty.pack(side="left", padx=(10, 0))

        # --- Ruhezustand ---
        tk.Label(tab, text=t("Ruhezustand (hiberfil.sys)"), bg=BG_DARK,
                 fg=MARINE_BRIGHT, font=("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=16, pady=(22, 0))
        tk.Label(tab, text=t("Der Ruhezustand belegt eine Datei so gross wie dein "
                             "RAM (oft 8-32 GB). Abschalten gibt diesen Platz frei - "
                             "danach gibt es keinen Ruhezustand/Schnellstart mehr "
                             "(jederzeit umkehrbar). Braucht Admin-Rechte."),
                 bg=BG_DARK, fg=TEXT_DIM, font=("Segoe UI", 9),
                 wraplength=980, justify="left").pack(anchor="w", padx=16)
        hb_box = tk.Frame(tab, bg=BG_INPUT)
        hb_box.pack(fill="x", padx=14, pady=8)
        self.hb_info = tk.StringVar(value="")
        tk.Label(hb_box, textvariable=self.hb_info, bg=BG_INPUT, fg=MARINE_TEXT,
                 font=("Segoe UI", 11), anchor="w").pack(side="left", padx=16, pady=12)
        hb_bar = tk.Frame(tab, bg=BG_DARK)
        hb_bar.pack(fill="x", padx=14)
        ttk.Button(hb_bar, text=t("Status pruefen"), style="Marine.TButton",
                   command=self.check_hibernation).pack(side="left")
        self.hb_toggle = ttk.Button(hb_bar, text=t("Ruhezustand abschalten"),
                                    style="Marine.TButton", state="disabled",
                                    command=self.toggle_hibernation)
        self.hb_toggle.pack(side="left", padx=(10, 0))

    def check_recycle(self) -> None:
        info = query_recycle_bin()
        self.rb_info.set(t("Papierkorb: {size} in {n} Objekten").format(
            size=human_size(info.size_bytes), n=info.num_items))
        self.rb_empty.config(state="normal" if info.size_bytes > 0 else "disabled")
        self.status.set(t("Papierkorb: {size}.").format(
            size=human_size(info.size_bytes)))

    def empty_recycle(self) -> None:
        if not messagebox.askyesno(
                t("Papierkorb leeren?"),
                t("Der gesamte Papierkorb wird ENDGUELTIG geleert (alle Laufwerke). "
                  "Danach ist eine Wiederherstellung nicht mehr moeglich.\n\n"
                  "Fortfahren?"), icon="warning", default="no"):
            self.status.set(t("Abgebrochen."))
            return
        ok = empty_recycle_bin()
        self.check_recycle()
        self.status.set(t("Papierkorb geleert.") if ok
                        else t("Papierkorb war leer oder konnte nicht geleert werden."))

    def check_hibernation(self) -> None:
        if hibernation_enabled():
            self.hb_info.set(t("Ruhezustand: AKTIV  (hiberfil.sys: {size})").format(
                size=human_size(hiberfile_size())))
            self.hb_toggle.config(text=t("Ruhezustand abschalten"), state="normal")
        else:
            self.hb_info.set(t("Ruhezustand: AUS (keine hiberfil.sys)"))
            self.hb_toggle.config(text=t("Ruhezustand einschalten"), state="normal")
        self.status.set(t("Ruhezustand-Status geprueft."))

    def toggle_hibernation(self) -> None:
        if not is_admin():
            if messagebox.askyesno(
                    t("Administrator noetig"),
                    t("Diese Aktion braucht Administrator-Rechte.\n\nJetzt als "
                      "Administrator neu starten?")):
                self.restart_as_admin()
            return
        if hibernation_enabled():
            if not messagebox.askyesno(
                    t("Ruhezustand abschalten?"),
                    t("hiberfil.sys ({size}) wird geloescht. Ruhezustand und "
                      "Schnellstart sind danach aus (umkehrbar).\n\nFortfahren?")
                    .format(size=human_size(hiberfile_size())),
                    icon="warning", default="no"):
                self.status.set(t("Abgebrochen."))
                return
            ok, msg = disable_hibernation()
            done = (t("Ruhezustand abgeschaltet, Platz freigegeben.") if ok
                    else t("Fehler: {msg}").format(msg=msg))
        else:
            ok, msg = enable_hibernation()
            done = (t("Ruhezustand wieder eingeschaltet.") if ok
                    else t("Fehler: {msg}").format(msg=msg))
        if ok:
            messagebox.showinfo(t("Fertig"), done)
        else:
            messagebox.showerror(t("Fehlgeschlagen"), done)
        self.check_hibernation()
        self.status.set(done)


def main() -> None:
    # Sprache bestimmen: '--lang xx' (z.B. vom Installer) hat Vorrang,
    # sonst die zuletzt gespeicherte Wahl, sonst Standard (Deutsch).
    if "--lang" in sys.argv:
        try:
            i18n.set_language(sys.argv[sys.argv.index("--lang") + 1])
        except (IndexError, ValueError):
            pass
    else:
        i18n.load_saved_language()

    root = tk.Tk()
    CleanSweepGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
