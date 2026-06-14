# Verbreitung / Promotion – fertige Texte & Checkliste

Download-Link (Setup.exe):
https://github.com/acc328512-max/CleanSweep/releases/download/v1.0/CleanSweep-Setup.exe

Projektseite:
https://github.com/acc328512-max/CleanSweep

---

## 1. Paketmanager (technische Nutzer)

- [x] **winget** – PR eingereicht: https://github.com/microsoft/winget-pkgs/pull/387856
- [ ] **Scoop** – Manifest liegt im Repo (`bucket/cleansweep.json`).
      Nutzer installieren mit:
      ```
      scoop bucket add cleansweep https://github.com/acc328512-max/CleanSweep
      scoop install cleansweep
      ```
      Optional: Manifest zusätzlich beim offiziellen „Extras"-Bucket einreichen
      (PR an https://github.com/ScoopInstaller/Extras).
- [ ] **Chocolatey** – Paket liegt im Repo (`chocolatey/`). Veröffentlichen:
      1. Account auf https://community.chocolatey.org/ anlegen, API-Key holen
      2. `cd chocolatey; choco pack`
      3. `choco apikey --key <DEIN_KEY> --source https://push.chocolatey.org/`
      4. `choco push cleansweep.1.0.0.nupkg --source https://push.chocolatey.org/`
      (Danach Moderation durch Chocolatey.)

> Bonus: Sobald der winget-PR gemergt ist, erscheint CleanSweep automatisch auch
> auf **winget.run** und **winstall.app** – ohne weiteres Zutun.

---

## 2. Entdeckungs-/Listen-Seiten (Account nötig → nur einfügen)

### AlternativeTo.net  (https://alternativeto.net/manage/submit-app/)
**Name:** CleanSweep
**Kategorie:** System & Disk / Cleaner
**Lizenz:** Open Source (Free)
**Plattform:** Microsoft Windows
**Beschreibung (EN):**
> CleanSweep is a free, open-source Windows tool to reclaim disk space. It finds
> orphaned program leftovers, large unused files, temp files, browser/app caches,
> Windows Update leftovers and Windows.old, and removes them safely (to the
> Recycle Bin, reversible). Dark mode, six languages, Beginner/Expert mode.
**Als Alternative zu:** CCleaner, BleachBit, BCUninstaller

### Product Hunt  (https://www.producthunt.com/posts/new)
**Tagline (EN, max 60 Zeichen):**
> Free, open-source disk cleanup for Windows
**Beschreibung (EN):**
> CleanSweep frees up disk space on Windows: it finds orphaned program leftovers,
> big unused files, caches, Windows Update leftovers and Windows.old — and removes
> them safely to the Recycle Bin. Open source, 6 languages, dark mode.

---

## 3. Community-Posts (fertig zum Posten)

### Reddit – r/opensource, r/coolgithubprojects, r/Windows10, r/software
**Titel (EN):** CleanSweep – a free, open-source disk cleanup tool for Windows (6 languages)
**Text (EN):**
> I built CleanSweep, a free and open-source Windows tool to free up disk space.
> It finds orphaned program leftovers, large unused files, temp/cache files,
> Windows Update leftovers and Windows.old, and removes them safely (Recycle Bin,
> reversible). Dark mode, 6 languages, Beginner/Expert mode.
>
> Code & download: https://github.com/acc328512-max/CleanSweep
> Feedback welcome!

### Deutsche Foren – ComputerBase, Dr. Windows, Computerbild-Forum
**Titel (DE):** CleanSweep – kostenloses Open-Source-Tool zum Aufräumen von Windows-Speicher
**Text (DE):**
> Ich habe CleanSweep entwickelt – ein kostenloses, quelloffenes Windows-Tool,
> das Speicherplatz freigibt: verwaiste Programmreste, große ungenutzte Dateien,
> Temp-/Cache-Dateien, Windows-Update-Reste und Windows.old. Gelöscht wird sicher
> in den Papierkorb (umkehrbar). Dark Mode, 6 Sprachen, Beginner/Expert-Modus.
>
> Code & Download: https://github.com/acc328512-max/CleanSweep
> Über Feedback freue ich mich!

> Hinweis: Bei Reddit/Foren die jeweiligen Regeln zur Eigenwerbung beachten
> (oft eigener „Show & Tell"-/Projekte-Bereich).

---

## 4. Seriöse Download-Portale (kein Adware-Wrapper)

- [ ] **FOSSHub** – https://www.fosshub.com/ (für Open Source, kein Bundling)
- [ ] **SourceForge** – https://sourceforge.net/ (Projekt anlegen, Release spiegeln)
- [ ] **Softpedia** – https://www.softpedia.com/ („Submit software")
- [ ] **MajorGeeks** – https://www.majorgeeks.com/content/page/contact.html

## 5. Awesome-Listen (GitHub-PR, optional)

- [ ] **Awesome-Windows** – https://github.com/Awesome-Windows/Awesome
      (Hinweis: Kuratoren bevorzugen etablierte Tools – evtl. erst mit ein paar
      Sternen/Downloads einreichen.)
