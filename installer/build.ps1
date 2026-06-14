# ===========================================================================
# build.ps1 - Baut CleanSweep zur Setup.exe (PyInstaller + Inno Setup)
#             und signiert optional App + Installer (Code Signing).
# ===========================================================================
# Schritt 0: Icon erzeugen
# Schritt 1: App in eigenstaendige CleanSweep.exe packen (PyInstaller)  -> signieren
# Schritt 2: Installer CleanSweep-Setup.exe kompilieren (Inno Setup)    -> signieren
#
# Aufruf:  powershell -ExecutionPolicy Bypass -File build.ps1
# Ergebnis: installer\out\CleanSweep-Setup.exe
# ===========================================================================

# ===========================================================================
# >>> CODE-SIGNING-KONFIGURATION <<<
# Leer lassen ($SignMode = "") -> es wird NICHT signiert (Build laeuft normal).
# Sobald das Zertifikat da ist, hier eintragen - sonst nichts aendern.
#
#   $SignMode = "pfx"        -> Zertifikat als .pfx-Datei
#       $SignCert     = "C:\Pfad\zertifikat.pfx"
#       $SignPassword = "PFX-Passwort"
#
#   $SignMode = "thumbprint" -> Zertifikat liegt im Windows-Zertifikatsspeicher
#       $SignCert     = "AB12CD...."   (SHA1-Fingerabdruck, ohne Leerzeichen)
#                                       (typisch bei Hardware-Token / EV)
#
#   $SignMode = "subject"    -> Zertifikat ueber den Anzeigenamen waehlen
#       $SignCert     = "Alexander Cross"   (Aussteller/Antragsteller-Name)
#
# Zeitstempel (WICHTIG: damit die Signatur nach Ablauf des Zertifikats
# gueltig bleibt) - Standard ok lassen:
# ===========================================================================
$SignMode     = ""
$SignCert     = ""
$SignPassword = ""
$TimestampUrl = "http://timestamp.digicert.com"
# ===========================================================================

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot          # Projektwurzel (E:\Claude)
$py   = "$env:LocalAppData\Programs\Python\Python312\python.exe"
$iscc = "$env:LocalAppData\Programs\Inno Setup 6\ISCC.exe"


function Find-SignTool {
    # signtool.exe kommt mit dem Windows SDK. Neueste Version suchen.
    $cmd = Get-Command signtool.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $candidates = Get-ChildItem `
        "C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe",
        "C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe" `
        -ErrorAction SilentlyContinue | Sort-Object FullName -Descending
    if ($candidates) { return $candidates[0].FullName }
    return $null
}

function Sign-File($file) {
    # Signiert $file - oder ueberspringt es, wenn kein Zertifikat konfiguriert ist.
    if ([string]::IsNullOrWhiteSpace($SignMode)) {
        Write-Host "      (nicht signiert - kein Zertifikat konfiguriert)" -ForegroundColor DarkGray
        return
    }
    $signtool = Find-SignTool
    if (-not $signtool) {
        throw "signtool.exe nicht gefunden. Bitte das Windows SDK installieren " +
              "(winget install Microsoft.WindowsSDK.10) oder signtool in den PATH legen."
    }

    $common = @("sign", "/fd", "SHA256", "/tr", $TimestampUrl, "/td", "SHA256", "/v")
    switch ($SignMode) {
        "pfx"        { $args = $common + @("/f", $SignCert, "/p", $SignPassword, $file) }
        "thumbprint" { $args = $common + @("/sha1", $SignCert, $file) }
        "subject"    { $args = $common + @("/n", $SignCert, $file) }
        default      { throw "Unbekannter `$SignMode: '$SignMode' (erlaubt: pfx, thumbprint, subject)" }
    }
    Write-Host "      Signiere $([System.IO.Path]::GetFileName($file)) ..." -ForegroundColor Cyan
    & $signtool @args
    if ($LASTEXITCODE -ne 0) { throw "Signieren fehlgeschlagen ($file)." }
}


Write-Host "[0/2] Erzeuge Icon ..." -ForegroundColor Cyan
& $py "$root\installer\make_icon.py"

Write-Host "[1/2] Baue eigenstaendige CleanSweep.exe (PyInstaller) ..." -ForegroundColor Cyan
& $py -m PyInstaller --noconfirm --onefile --windowed --name CleanSweep `
    --icon "$root\installer\cleansweep.ico" `
    --add-data "$root\installer\cleansweep.ico;." `
    --distpath "$root\installer\dist" `
    --workpath "$root\build" `
    --specpath "$root\build" `
    --paths "$root\src" `
    "$root\src\gui.py"

if (-not (Test-Path "$root\installer\dist\CleanSweep.exe")) {
    throw "PyInstaller-Build fehlgeschlagen."
}
# App-exe signieren (damit auch das INSTALLIERTE Programm signiert ist).
Sign-File "$root\installer\dist\CleanSweep.exe"

Write-Host "[2/2] Kompiliere Installer (Inno Setup) ..." -ForegroundColor Cyan
& $iscc "$root\installer\CleanSweep.iss"

$setup = "$root\installer\out\CleanSweep-Setup.exe"
if (-not (Test-Path $setup)) {
    throw "Inno-Setup-Kompilierung fehlgeschlagen."
}
# Den fertigen Installer signieren.
Sign-File $setup

Write-Host "FERTIG: $setup" -ForegroundColor Green
if (-not [string]::IsNullOrWhiteSpace($SignMode)) {
    Write-Host "        (App + Installer signiert)" -ForegroundColor Green
}
