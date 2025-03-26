# -*- coding: utf-8 -*-
import os
import subprocess

# 1. 상대경로 설정
revit_folder = "InputFiles"
filelist_path = "revit_file_list.txt"
rbp_exe = "Resources/RBP/BatchRvt.exe"
rbp_script = "Scripts/my_task.py"
rbp_settings = "Resources/rbp_settings.json"
revit_version = "2025"

# 2. Revit 파일 리스트 생성
revit_files = [
    os.path.join(revit_folder, f)
    for f in os.listdir(revit_folder)
    if f.lower().endswith(".rvt")
]

with open(filelist_path, "w", encoding="utf-8") as f:
    for fpath in revit_files:
        f.write(fpath + "\n")

print("✅ Revit 파일 리스트 작성 완료 ({}개):".format(len(revit_files)))
for f in revit_files:
    print(" -", f)

# 3. 명령어 실행
cmd = [
    os.path.abspath(rbp_exe),
    "--task_script",
    os.path.abspath(rbp_script),
    "--file_list",
    os.path.abspath(filelist_path),
    "--settings_file",
    os.path.abspath(rbp_settings),
    "--revit_version",
    revit_version,
]

print("🔧 실행 명령어 (전체):")
for arg in cmd:
    print("  ", arg)
print("🚀 명령어 실행 중...\n")

subprocess.run(cmd)

print("✅ 작업 완료!")
