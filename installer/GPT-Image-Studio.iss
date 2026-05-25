#define AppName "GPT-Image Studio"
#ifndef AppVersion
#define AppVersion "0.1.0"
#endif
#define AppExeName "GPT-Image-Studio.exe"
#define AppPublisher "wumingzhidewu"
#define AppURL "https://github.com/wumingzhidewu/gpt-image-studio"

[Setup]
AppId={{9D9613A5-4F30-49F5-A3C0-9C88DB0E7D09}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\GPT-Image Studio
DefaultGroupName=GPT-Image Studio
AllowNoIcons=yes
OutputDir=..\dist\installer
OutputBaseFilename=GPT-Image-Studio-Setup-{#AppVersion}
SetupIconFile=..\assets\app_logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "..\dist\GPT-Image-Studio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\GPT-Image Studio"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall GPT-Image Studio"; Filename: "{uninstallexe}"
Name: "{autodesktop}\GPT-Image Studio"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch GPT-Image Studio"; Flags: nowait postinstall skipifsilent
