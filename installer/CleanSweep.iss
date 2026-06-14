; ===========================================================================
; CleanSweep - Inno-Setup-Installationsskript
; ===========================================================================
; Erzeugt eine Setup.exe, die:
;   * beim Start einen SPRACHAUSWAHL-Dialog zeigt (dieselben 6 Sprachen wie
;     die App: Deutsch, Englisch, Franzoesisch, Spanisch, Polnisch, Ukrainisch)
;   * CleanSweep nach Programme installiert (ohne Admin: ins Benutzerprofil)
;   * Startmenue- und (optional) Desktop-Verknuepfung anlegt
;   * die gewaehlte Sprache merkt, damit die App gleich darin startet
;
; Kompilieren:  ISCC.exe CleanSweep.iss   ->  out\CleanSweep-Setup.exe
; ===========================================================================

#define AppName "CleanSweep"
#define AppVersion "1.0"
#define AppPublisher "CleanSweep"
#define AppExe "CleanSweep.exe"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
; Ohne Admin installieren (ins Benutzerprofil) - die App holt sich Admin-Rechte
; selbst, wenn sie sie braucht (z.B. DISM/Update-Cache).
PrivilegesRequired=lowest
OutputDir=out
OutputBaseFilename=CleanSweep-Setup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=yes
DisableProgramGroupPage=yes
UninstallDisplayName={#AppName}
; Eigenes Icon fuer die Setup.exe und fuer den Eintrag in "Programme & Features".
SetupIconFile=cleansweep.ico
UninstallDisplayIcon={app}\{#AppExe}

[Languages]
; Der Name (links) entspricht dem Sprachcode der App -> wird so uebernommen.
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "pl"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "uk"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#AppExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent

[Code]
{ Nach der Installation die im Installer gewaehlte Sprache merken,        }
{ damit CleanSweep beim ersten Start direkt in dieser Sprache erscheint.  }
procedure CurStepChanged(CurStep: TSetupStep);
var
  LangDir, LangFile: string;
begin
  if CurStep = ssPostInstall then
  begin
    LangDir := ExpandConstant('{localappdata}\CleanSweep');
    if not DirExists(LangDir) then
      CreateDir(LangDir);
    LangFile := LangDir + '\lang.txt';
    SaveStringToFile(LangFile, ActiveLanguage(), False);
  end;
end;
