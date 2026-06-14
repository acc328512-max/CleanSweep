$ErrorActionPreference = 'Stop'

$packageArgs = @{
    packageName    = 'cleansweep'
    fileType       = 'exe'
    url64bit       = 'https://github.com/acc328512-max/CleanSweep/releases/download/v1.0/CleanSweep-Setup.exe'
    checksum64     = '212FB041329E738A2A3ED5334470FE3813A32606C01FB3A53700B7C52D40AFED'
    checksumType64 = 'sha256'
    # Inno-Setup-Schalter fuer stille Installation:
    silentArgs     = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART'
    validExitCodes = @(0)
}

Install-ChocolateyPackage @packageArgs
