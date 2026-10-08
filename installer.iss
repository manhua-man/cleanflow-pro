; Inno Setup Script for CleanFlow Pro
; Strict Zero Emoji

[Setup]
AppId={{9F570F28-0954-4D4B-A6FA-E5F2284C8FE5}
AppName=CleanFlow Pro
AppVersion=0.1.0
AppPublisher=CleanFlow Team
AppPublisherURL=https://github.com/manhua-man/cleanflow-pro
DefaultDirName={autopf}\CleanFlow-Pro
DefaultGroupName=CleanFlow Pro
OutputDir=dist
OutputBaseFilename=CleanFlow-Pro-v0.1.0-Setup
Compression=lzma2/ultra64
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\CleanFlow-Pro-v0.1.0-win64\cleanflow.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\CleanFlow-Pro-v0.1.0-win64\rules.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\CleanFlow-Pro-v0.1.0-win64\start-cleanflow.cmd"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CleanFlow Pro"; Filename: "{app}\cleanflow.exe"
Name: "{group}\卸载 CleanFlow Pro"; Filename: "{uninstallexe}"
Name: "{autodesktop}\CleanFlow Pro"; Filename: "{app}\cleanflow.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\cleanflow.exe"; Description: "{cm:LaunchProgram,CleanFlow Pro}"; Flags: nowait postinstall skipifsilent
