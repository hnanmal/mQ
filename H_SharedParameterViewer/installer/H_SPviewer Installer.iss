#define MyVersion "0.0.0"

[Setup]
AppName=H_RevitSharedParameterViewer
AppVersion={#MyVersion}
WizardStyle=modern
; DefaultDirName={pf}\H_RevitSharedParameterViewer
DefaultDirName={autopf}\H_RevitSharedParameterViewer
DefaultGroupName=H_RevitSharedParameterViewer
OutputDir=.\installer
OutputBaseFilename=H_RevitSharedParameterViewer_Setup_{#MyVersion}
Compression=lzma
SolidCompression=yes

[Languages]
Name: "ko"; MessagesFile: "compiler:Languages\Korean.isl"

[Files]
; 앱 실행파일
Source: "..\dist\SharedParameterViewer.exe"; DestDir: "{app}"; Flags: ignoreversion

; resource 폴더 전체 복사
Source: "..\dist\resource\*"; DestDir: "{app}\resource"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\H_RevitSharedParameterViewer"; Filename: "{app}\SharedParameterViewer.exe"
Name: "{group}\Uninstall H_RevitSharedParameterViewer"; Filename: "{uninstallexe}"

