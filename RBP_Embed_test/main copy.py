# -*- coding: utf-8 -*-
"""
main.py
- 특정 폴더에서 Revit 파일 목록 자동 수집
- RBP 설정 파일(.json) 사용
- Revit Batch Processor (RBP)를 앱 내부에서 실행
"""

import os
import subprocess

# 1. 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))

revit_folder = os.path.join(base_dir, "InputFiles")
filelist_path = os.path.join(base_dir, "revit_file_list.txt")
rbp_exe = os.path.join(base_dir, "Resources", "RBP", "BatchRvt.exe")
rbp_script = os.path.join(base_dir, "Scripts", "my_task.py")
rbp_settings = os.path.join(base_dir, "Resources", "rbp_settings.json")
# rbp_settings = os.path.join(base_dir, "Resources", "rbp_settings.xml")
revit_version = "2025"  # 사용자의 Revit 버전에 맞게 설정

# 2. .rvt 파일 목록 수집 및 file list 작성
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

# 3. RBP 실행
print("\n🚀 RBP 실행 중...")

# subprocess.run(
#     [
#         rbp_exe,
#         "-script",
#         rbp_script,
#         "-filelist",
#         filelist_path,
#         "-settings",
#         rbp_settings,
#         "-version",
#         revit_version,
#     ]
# )

# subprocess.run(
#     [
#         rbp_exe,
#         "-script",
#         rbp_script,
#         "-filelist",
#         filelist_path,
#         "-settings",
#         rbp_settings,  # ❗ 큰따옴표 빼야 함
#         "-version",
#         revit_version,
#     ],
#     # shell=True,
# )

cmd = (
    f'"{os.path.abspath(rbp_exe)}" '
    f'-script "{os.path.abspath(rbp_script)}" '
    f'-filelist "{os.path.abspath(filelist_path)}" '
    f'-settings "{os.path.abspath(rbp_settings)}" '
    f"-version {revit_version}"
)

# .bat 파일로 저장
bat_path = os.path.join(base_dir, "run_rbp.bat")
with open(bat_path, "w", encoding="utf-8") as bat:
    bat.write(cmd)

print("🔧 실행 배치파일:", bat_path)
print("📁 명령어 내용:", cmd)

# 실행
subprocess.run(f'"{bat_path}"', shell=True)

print("✅ 작업 완료!")

print("📁 명령:", cmd)
print("📁 설정 파일 경로:", rbp_settings)
print("📄 설정 파일 존재:", os.path.exists(rbp_settings))
