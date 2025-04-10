#define MyVersion "0.0.2"

[Setup]
AppName=H_WindSpeedConvertor
AppVersion={#MyVersion}
WizardStyle=modern
; DefaultDirName={pf}\H_BimNote
DefaultDirName={autopf}\H_WindSpeedConvertor
DefaultGroupName=H_WindSpeedConvertor
OutputDir=.\installer
OutputBaseFilename=H_WindSpeedConvertor_Setup_{#MyVersion}
Compression=lzma
SolidCompression=yes

[Languages]
Name: "ko"; MessagesFile: "compiler:Languages\Korean.isl"

[Files]
; 앱 실행파일
Source: "..\dist\H_WindSpeedConvertor.exe"; DestDir: "{app}"; Flags: ignoreversion

; resource 폴더 전체 복사
Source: "..\dist\resource\*"; DestDir: "{app}\resource"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\H_WindSpeedConvertor"; Filename: "{app}\H_WindSpeedConvertor.exe"
Name: "{group}\Uninstall H_WindSpeedConvertor"; Filename: "{uninstallexe}"

