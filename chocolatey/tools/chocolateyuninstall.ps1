$ErrorActionPreference = 'Stop'

# Inno-Setup-Deinstallation: der Uninstaller liegt im Installationsordner.
$uninst = Join-Path $env:LOCALAPPDATA 'Programs\CleanSweep\unins000.exe'
if (Test-Path $uninst) {
    $packageArgs = @{
        packageName  = 'cleansweep'
        fileType     = 'exe'
        file         = $uninst
        silentArgs   = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART'
        validExitCodes = @(0)
    }
    Uninstall-ChocolateyPackage @packageArgs
} else {
    Write-Warning "CleanSweep-Deinstallationsprogramm nicht gefunden - evtl. bereits entfernt."
}
