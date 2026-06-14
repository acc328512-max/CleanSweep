"""
cache_cleaner.py
================
Findet und leert Cache-Ordner bekannter Programme (Browser, Chat-Apps, ...).

Caches sind Wegwerf-Daten: die Programme bauen sie bei Bedarf neu auf. Deshalb
loeschen wir sie - wie Temp-Dateien - ENDGUELTIG (nicht in den Papierkorb),
damit der Platz wirklich frei wird. Gesperrte Dateien (z.B. wenn der Browser
gerade laeuft) werden uebersprungen.

Tipp: Fuer das beste Ergebnis die betroffene App vorher schliessen.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


# (Anzeigename, Basis "local"/"roaming", [relative Glob-Pfade zu Cache-Ordnern])
# Das '*' steht z.B. fuer mehrere Browser-Profile.
_CACHE_DEFS: list[tuple[str, str, list[str]]] = [
    ("Google Chrome", "local", [
        r"Google\Chrome\User Data\*\Cache",
        r"Google\Chrome\User Data\*\Code Cache",
        r"Google\Chrome\User Data\*\GPUCache",
        r"Google\Chrome\User Data\*\Service Worker\CacheStorage",
    ]),
    ("Microsoft Edge", "local", [
        r"Microsoft\Edge\User Data\*\Cache",
        r"Microsoft\Edge\User Data\*\Code Cache",
        r"Microsoft\Edge\User Data\*\GPUCache",
    ]),
    ("Mozilla Firefox", "local", [
        r"Mozilla\Firefox\Profiles\*\cache2",
    ]),
    ("Discord", "roaming", [
        r"discord\Cache", r"discord\Code Cache", r"discord\GPUCache",
    ]),
    ("Spotify", "local", [
        r"Spotify\Storage", r"Spotify\Data",
    ]),
    ("Microsoft Teams", "roaming", [
        r"Microsoft\Teams\Cache", r"Microsoft\Teams\Code Cache",
        r"Microsoft\Teams\GPUCache",
        r"Microsoft\Teams\Service Worker\CacheStorage",
    ]),
    ("Slack", "roaming", [
        r"Slack\Cache", r"Slack\Code Cache", r"Slack\GPUCache",
    ]),
    ("NVIDIA Shader-Cache", "local", [
        r"NVIDIA\DXCache", r"NVIDIA\GLCache",
    ]),
    ("DirectX Shader-Cache", "local", [
        r"D3DSCache",
    ]),
]


@dataclass
class CacheItem:
    """Cache eines Programms, ueber evtl. mehrere Ordner verteilt."""
    app: str
    size_bytes: int = 0
    paths: list[Path] = field(default_factory=list)


def _base_dir(base: str) -> str:
    return os.environ.get("LOCALAPPDATA" if base == "local" else "APPDATA", "")


def _dir_size(path: Path) -> int:
    total = 0
    stack = [path]
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(cur) as it:
                for e in it:
                    try:
                        if e.is_dir(follow_symlinks=False):
                            stack.append(Path(e.path))
                        elif e.is_file(follow_symlinks=False):
                            total += e.stat(follow_symlinks=False).st_size
                    except OSError:
                        continue
        except OSError:
            continue
    return total


def scan_caches() -> list[CacheItem]:
    """Ermittelt vorhandene Cache-Ordner samt Groesse (read-only)."""
    items: list[CacheItem] = []
    for app, base, patterns in _CACHE_DEFS:
        root = _base_dir(base)
        if not root:
            continue
        item = CacheItem(app=app)
        for pattern in patterns:
            # glob loest '*' (z.B. Profile) auf.
            for match in Path(root).glob(pattern):
                if match.is_dir():
                    item.size_bytes += _dir_size(match)
                    item.paths.append(match)
        if item.paths:
            items.append(item)
    items.sort(key=lambda c: c.size_bytes, reverse=True)
    return items


@dataclass
class CacheCleanResult:
    deleted_files: int
    freed_bytes: int
    skipped_files: int


def clean_caches(items: list[CacheItem]) -> CacheCleanResult:
    """Leert die uebergebenen Cache-Ordner (Inhalt), endgueltig.

    Gesperrte Dateien werden uebersprungen; die Cache-Ordner selbst bleiben
    bestehen (die Programme fuellen sie wieder).
    """
    deleted, freed, skipped = 0, 0, 0
    for item in items:
        for cache_dir in item.paths:
            d, f, s = _delete_contents(cache_dir)
            deleted += d
            freed += f
            skipped += s
    return CacheCleanResult(deleted, freed, skipped)


def _delete_contents(root: Path) -> tuple[int, int, int]:
    """Loescht alle Dateien unterhalb von root; leere Unterordner werden entfernt."""
    deleted, freed, skipped = 0, 0, 0
    for dirpath, _dirs, filenames in os.walk(root, topdown=False):
        for name in filenames:
            fp = Path(dirpath) / name
            try:
                size = fp.stat().st_size
                fp.unlink()
                deleted += 1
                freed += size
            except OSError:
                skipped += 1
        if Path(dirpath) != root:
            try:
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
            except OSError:
                pass
    return deleted, freed, skipped


if __name__ == "__main__":
    from folder_scan import human_size
    items = scan_caches()
    total = sum(i.size_bytes for i in items)
    print(f"Gefundene Caches ({human_size(total)} gesamt):\n")
    for i in items:
        print(f"  {human_size(i.size_bytes):>10}  {i.app}  ({len(i.paths)} Ordner)")
